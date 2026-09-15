import { describe, expect, it } from "vitest";
import { buildRadarData } from "./radar";
import type { TeamStats } from "../types/api";

function makeStats(overrides: Partial<TeamStats>): TeamStats {
  return {
    team: "Test",
    rank: 10,
    total_points: 1500,
    avg_goals_scored: 2,
    avg_goals_conceded: 1,
    avg_outcome: 0.5,
    avg_goal_diff: 1,
    recent_matches: [],
    ...overrides,
  };
}

describe("buildRadarData", () => {
  it("produces one point per axis, all within [0, 10]", () => {
    const home = makeStats({});
    const away = makeStats({ rank: 30, total_points: 1000 });
    const points = buildRadarData(home, away);

    expect(points).toHaveLength(5);
    for (const p of points) {
      expect(p.home).toBeGreaterThanOrEqual(0);
      expect(p.home).toBeLessThanOrEqual(10);
      expect(p.away).toBeGreaterThanOrEqual(0);
      expect(p.away).toBeLessThanOrEqual(10);
    }
  });

  it("gives the better-ranked team a higher 'Classement' score", () => {
    const strong = makeStats({ rank: 2 });
    const weak = makeStats({ rank: 80 });
    const points = buildRadarData(strong, weak);
    const rankPoint = points.find((p) => p.category === "Classement")!;
    expect(rankPoint.home).toBeGreaterThan(rankPoint.away);
  });

  it("handles missing rank/points (null) without throwing", () => {
    const home = makeStats({ rank: null, total_points: null });
    const away = makeStats({});
    expect(() => buildRadarData(home, away)).not.toThrow();
  });
});
