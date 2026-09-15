import { useEffect, useState } from "react";
import { api, ApiError } from "../lib/api";
import { createTtlCache } from "../lib/ttlCache";

const teamsCache = createTtlCache<string[]>(5 * 60 * 1000);
const CACHE_KEY = "teams";

/** Test-only escape hatch: the cache is a module-level singleton so it
 * survives across renders within a session, which means tests in the same
 * file must reset it between cases to stay isolated from each other. */
export const __resetTeamsCache = () => teamsCache.clear();

interface UseTeamsResult {
  teams: string[];
  loading: boolean;
  error: string | null;
}

export function useTeams(): UseTeamsResult {
  const cached = teamsCache.get(CACHE_KEY);
  const [teams, setTeams] = useState<string[]>(cached ?? []);
  const [loading, setLoading] = useState(!cached);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (cached) return;

    let cancelled = false;
    setLoading(true);
    setError(null);

    api
      .getTeams()
      .then((res) => {
        if (cancelled) return;
        teamsCache.set(CACHE_KEY, res.teams);
        setTeams(res.teams);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.message : "Une erreur inattendue est survenue.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { teams, loading, error };
}
