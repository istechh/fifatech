import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { MatchSelector } from "./MatchSelector";

const TEAMS = ["France", "Brazil", "Germany"];

function setup(overrides: Partial<React.ComponentProps<typeof MatchSelector>> = {}) {
  const onSubmit = vi.fn<() => void>();
  const props = {
    teams: TEAMS,
    homeTeam: "France",
    awayTeam: "Brazil",
    neutral: false,
    loading: false,
    onHomeChange: vi.fn<(team: string) => void>(),
    onAwayChange: vi.fn<(team: string) => void>(),
    onNeutralChange: vi.fn<(neutral: boolean) => void>(),
    onSubmit,
    ...overrides,
  };
  render(<MatchSelector {...props} />);
  return { onSubmit, props };
}

describe("MatchSelector", () => {
  it("enables the submit button when the two teams differ", () => {
    setup();
    expect(screen.getByRole("button", { name: /lancer la prédiction/i })).toBeEnabled();
  });

  it("disables the submit button and warns when both teams are the same", () => {
    setup({ homeTeam: "France", awayTeam: "France" });
    expect(screen.getByRole("button", { name: /lancer la prédiction/i })).toBeDisabled();
    expect(screen.getByRole("alert")).toHaveTextContent(/différentes/i);
  });

  it("calls onSubmit when the button is clicked with two different teams", async () => {
    const { onSubmit } = setup();
    await userEvent.click(screen.getByRole("button", { name: /lancer la prédiction/i }));
    expect(onSubmit).toHaveBeenCalledOnce();
  });

  it("does not call onSubmit when the same team is selected on both sides", async () => {
    const { onSubmit } = setup({ homeTeam: "France", awayTeam: "France" });
    await userEvent.click(screen.getByRole("button", { name: /lancer la prédiction/i }));
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("disables the submit button while a prediction is loading", () => {
    setup({ loading: true });
    expect(screen.getByRole("button", { name: /lancer la prédiction/i })).toBeDisabled();
  });
});
