import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";
import { ApiError } from "./lib/api";
import { __resetTeamsCache } from "./hooks/useTeams";
import { __resetStatsCache } from "./hooks/usePrediction";
import type { PredictResponse, TeamStats, TeamsResponse } from "./types/api";

const getTeams = vi.fn<() => Promise<TeamsResponse>>();
const getTeamStats = vi.fn<(team: string) => Promise<TeamStats>>();
const predict = vi.fn<() => Promise<PredictResponse>>();

vi.mock("./lib/api", async () => {
  const actual = await vi.importActual<typeof import("./lib/api")>("./lib/api");
  return {
    ...actual,
    api: {
      getTeams: () => getTeams(),
      getTeamStats: (team: string) => getTeamStats(team),
      predict: () => predict(),
    },
  };
});

const TEAMS: TeamsResponse = { teams: ["France", "Brazil", "Germany"], count: 3 };

function statsFor(team: string): TeamStats {
  const isHome = team === "France";
  return {
    team,
    rank: isHome ? 2 : 4,
    total_points: isHome ? 1837.47 : 1791.85,
    avg_goals_scored: 2.8,
    avg_goals_conceded: 1.0,
    avg_outcome: 0,
    avg_goal_diff: 1.8,
    recent_matches: isHome
      ? [
          { date: "2026-06-08", opponent: "Norway", goals_for: 3, goals_against: 0, outcome: "W" },
          { date: "2026-06-30", opponent: "Sweden", goals_for: 4, goals_against: 1, outcome: "W" },
        ]
      : [
          { date: "2026-06-10", opponent: "Argentina", goals_for: 1, goals_against: 1, outcome: "D" },
          { date: "2026-06-28", opponent: "Uruguay", goals_for: 2, goals_against: 0, outcome: "W" },
        ],
  };
}

const PREDICTION: PredictResponse = {
  home_team: "France",
  away_team: "Brazil",
  neutral: false,
  prediction: "Victoire Domicile",
  probabilities: { Domicile: 76, Nul: 11.1, Extérieur: 12.9 },
  home_rank: 2,
  away_rank: 4,
  home_points: 1837.47,
  away_points: 1791.85,
};

beforeEach(() => {
  __resetTeamsCache();
  __resetStatsCache();
  getTeams.mockReset().mockResolvedValue(TEAMS);
  getTeamStats.mockReset().mockImplementation((team: string) => Promise.resolve(statsFor(team)));
  predict.mockReset().mockResolvedValue(PREDICTION);
});

describe("App", () => {
  it("loads the team list and pre-selects France vs Brazil", async () => {
    render(<App />);
    expect(await screen.findByDisplayValue("France")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Brazil")).toBeInTheDocument();
  });

  it("shows a friendly error if the team list fails to load", async () => {
    getTeams.mockReset().mockRejectedValue(new ApiError("Backend non disponible. Réessayez plus tard."));
    render(<App />);
    expect(await screen.findByRole("alert")).toHaveTextContent(/backend non disponible/i);
  });

  it("runs a prediction end-to-end and shows the essential result immediately", async () => {
    render(<App />);
    await screen.findByDisplayValue("France");

    await userEvent.click(screen.getByRole("button", { name: /lancer la prédiction/i }));

    expect(await screen.findByText("Victoire Domicile")).toBeInTheDocument();
    expect(screen.getByLabelText(/probabilités : france 76%/i)).toBeInTheDocument();
    // Stat cards are visible right away (not behind the disclosure).
    expect(screen.getAllByText("Classement FIFA").length).toBeGreaterThan(0);
  });

  it("keeps the detailed analysis collapsed by default, with the opponent visible once opened", async () => {
    render(<App />);
    await screen.findByDisplayValue("France");
    await userEvent.click(screen.getByRole("button", { name: /lancer la prédiction/i }));
    await screen.findByText("Victoire Domicile");

    // Collapsed: native <details> keeps its content in the DOM but hidden —
    // assert on visibility, not mere presence.
    expect(screen.getByText(/vs Sweden/)).not.toBeVisible();

    await userEvent.click(screen.getByText(/voir l'analyse détaillée/i));
    expect(await screen.findByText(/vs Sweden/)).toBeVisible();
  });

  it("disables the submit button and shows a warning for a same-team matchup", async () => {
    render(<App />);
    await screen.findByDisplayValue("France");

    await userEvent.selectOptions(screen.getByLabelText(/équipe extérieur/i), "France");

    expect(screen.getByRole("button", { name: /lancer la prédiction/i })).toBeDisabled();
    expect(await screen.findByRole("alert")).toHaveTextContent(/différentes/i);
    expect(predict).not.toHaveBeenCalled();
  });

  it("shows a clear error message if the prediction call fails", async () => {
    predict.mockReset().mockRejectedValue(new ApiError("Équipe domicile 'France' introuvable"));
    render(<App />);
    await screen.findByDisplayValue("France");

    await userEvent.click(screen.getByRole("button", { name: /lancer la prédiction/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/introuvable/i);
  });
});
