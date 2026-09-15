/**
 * Types mirroring the FastAPI/Pydantic models in app/api.py.
 * Keep these in sync with the backend if its schemas change.
 */

export interface TeamsResponse {
  teams: string[];
  count: number;
}

export interface RecentMatch {
  date: string;
  opponent: string;
  goals_for: number;
  goals_against: number;
  outcome: "W" | "D" | "L";
}

export interface TeamStats {
  team: string;
  rank: number | null;
  total_points: number | null;
  avg_goals_scored: number | null;
  avg_goals_conceded: number | null;
  avg_outcome: number | null;
  avg_goal_diff: number | null;
  recent_matches: RecentMatch[];
}

export interface PredictRequest {
  home_team: string;
  away_team: string;
  neutral: boolean;
}

export interface PredictResponse {
  home_team: string;
  away_team: string;
  neutral: boolean;
  prediction: string;
  probabilities: Record<string, number>;
  home_rank: number | null;
  away_rank: number | null;
  home_points: number | null;
  away_points: number | null;
}

export interface ApiErrorBody {
  detail?: string;
}
