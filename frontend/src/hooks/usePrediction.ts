import { useCallback, useState } from "react";
import { api, ApiError } from "../lib/api";
import { createTtlCache } from "../lib/ttlCache";
import type { PredictResponse, TeamStats } from "../types/api";

const statsCache = createTtlCache<TeamStats>(2 * 60 * 1000);

/** Test-only escape hatch — see useTeams.ts's __resetTeamsCache. */
export const __resetStatsCache = () => statsCache.clear();

async function getTeamStatsCached(team: string): Promise<TeamStats> {
  const cached = statsCache.get(team);
  if (cached) return cached;
  const stats = await api.getTeamStats(team);
  statsCache.set(team, stats);
  return stats;
}

export interface PredictionState {
  status: "idle" | "loading" | "error" | "success";
  error: string | null;
  result: PredictResponse | null;
  homeStats: TeamStats | null;
  awayStats: TeamStats | null;
}

const INITIAL_STATE: PredictionState = {
  status: "idle",
  error: null,
  result: null,
  homeStats: null,
  awayStats: null,
};

export function usePrediction() {
  const [state, setState] = useState<PredictionState>(INITIAL_STATE);

  const predict = useCallback(async (homeTeam: string, awayTeam: string, neutral: boolean) => {
    setState({ status: "loading", error: null, result: null, homeStats: null, awayStats: null });
    try {
      const result = await api.predict({ home_team: homeTeam, away_team: awayTeam, neutral });
      const [homeStats, awayStats] = await Promise.all([
        getTeamStatsCached(homeTeam),
        getTeamStatsCached(awayTeam),
      ]);
      setState({ status: "success", error: null, result, homeStats, awayStats });
    } catch (err) {
      setState({
        status: "error",
        error: err instanceof ApiError ? err.message : "Une erreur inattendue est survenue.",
        result: null,
        homeStats: null,
        awayStats: null,
      });
    }
  }, []);

  const reset = useCallback(() => setState(INITIAL_STATE), []);

  return { ...state, predict, reset };
}
