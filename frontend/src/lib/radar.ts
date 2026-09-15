import type { TeamStats } from "../types/api";

export interface RadarPoint {
  category: string;
  home: number;
  away: number;
}

function normalize(value: number, max: number): number {
  return max ? Math.min((value / max) * 10, 10) : 0;
}

/** Builds the 5-axis attack/defense/form/rank/points comparison used by the
 * radar chart, scaled 0-10 against whichever of the two teams is stronger
 * on each axis. Mirrors the normalization previously used in the Streamlit
 * version so predictions read the same way. */
export function buildRadarData(home: TeamStats, away: TeamStats): RadarPoint[] {
  const homeRank = home.rank ?? 100;
  const awayRank = away.rank ?? 100;
  const homePoints = home.total_points ?? 0;
  const awayPoints = away.total_points ?? 0;

  const maxScored = Math.max(home.avg_goals_scored ?? 0, away.avg_goals_scored ?? 0, 1);
  const maxConceded = Math.max(home.avg_goals_conceded ?? 0, away.avg_goals_conceded ?? 0, 1);
  const maxRank = Math.max(homeRank, awayRank, 1);
  const maxPoints = Math.max(homePoints, awayPoints, 1);

  const axis = (
    scored: number | null,
    conceded: number | null,
    outcome: number | null,
    rank: number,
    points: number,
  ) => ({
    attaque: normalize(scored ?? 0, maxScored),
    defense: 10 - normalize(conceded ?? 0, maxConceded),
    forme: normalize((outcome ?? 0) + 1, 2),
    classement: 10 - normalize(rank, maxRank),
    points: normalize(points, maxPoints),
  });

  const h = axis(home.avg_goals_scored, home.avg_goals_conceded, home.avg_outcome, homeRank, homePoints);
  const a = axis(away.avg_goals_scored, away.avg_goals_conceded, away.avg_outcome, awayRank, awayPoints);

  return [
    { category: "Attaque", home: h.attaque, away: a.attaque },
    { category: "Défense", home: h.defense, away: a.defense },
    { category: "Forme", home: h.forme, away: a.forme },
    { category: "Classement", home: h.classement, away: a.classement },
    { category: "Points", home: h.points, away: a.points },
  ];
}
