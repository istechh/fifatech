import type { ApiErrorBody, PredictRequest, PredictResponse, TeamStats, TeamsResponse } from "../types/api";

const API_URL = (import.meta.env.VITE_API_URL ?? "http://localhost:8000").replace(/\/+$/, "");
const DEFAULT_TIMEOUT_MS = 120_000; // Render free tier cold starts can take up to ~2 minutes.

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  timeoutMs = DEFAULT_TIMEOUT_MS,
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(`${API_URL}${path}`, {
      ...options,
      signal: controller.signal,
      headers: { "Content-Type": "application/json", ...options.headers },
    });

    if (!res.ok) {
      // The response body isn't guaranteed to be JSON: a reverse proxy
      // (e.g. Render waking a sleeping service) can return an HTML error
      // page instead of our API's JSON. Never assume — always fall back.
      let detail: string | undefined;
      try {
        detail = ((await res.json()) as ApiErrorBody).detail;
      } catch {
        /* non-JSON error body, use the generic message below */
      }
      throw new ApiError(
        detail ?? `Le serveur a répondu de façon inattendue (HTTP ${res.status}).`,
        res.status,
      );
    }

    return (await res.json()) as T;
  } catch (err) {
    if (err instanceof ApiError) throw err;
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new ApiError("Le serveur met trop de temps à répondre. Réessayez dans quelques instants.");
    }
    // fetch() rejects with a TypeError on network failure (DNS, connection refused, CORS…)
    if (err instanceof TypeError) {
      throw new ApiError("Backend non disponible. Réessayez plus tard.");
    }
    throw new ApiError("Une erreur inattendue est survenue.");
  } finally {
    clearTimeout(timeoutId);
  }
}

export const api = {
  getTeams: () => request<TeamsResponse>("/teams"),
  getTeamStats: (team: string) => request<TeamStats>(`/team_stats/${encodeURIComponent(team)}`),
  predict: (payload: PredictRequest) =>
    request<PredictResponse>("/predict", { method: "POST", body: JSON.stringify(payload) }),
};
