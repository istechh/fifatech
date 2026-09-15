import { Card } from "../ui/Card";
import { fmt } from "../../lib/format";
import type { TeamStats } from "../../types/api";

interface StatCardsProps {
  homeStats: TeamStats;
  awayStats: TeamStats;
  homeTeam: string;
  awayTeam: string;
}

interface Tile {
  icon: string;
  label: string;
  value: string;
}

function buildTiles(stats: TeamStats): Tile[] {
  return [
    { icon: "🏆", label: "Classement FIFA", value: fmt(stats.rank) },
    { icon: "⭐", label: "Points FIFA", value: fmt(stats.total_points) },
    { icon: "📈", label: "Forme récente", value: fmt(stats.avg_outcome) },
  ];
}

export function StatCards({ homeStats, awayStats, homeTeam, awayTeam }: StatCardsProps) {
  const groups: { team: string; icon: string; tone: string; tiles: Tile[] }[] = [
    { team: homeTeam, icon: "🏠", tone: "text-[var(--color-blue)]", tiles: buildTiles(homeStats) },
    { team: awayTeam, icon: "✈️", tone: "text-[var(--color-green)]", tiles: buildTiles(awayStats) },
  ];

  return (
    <div className="mt-6 grid grid-cols-1 gap-4 min-[480px]:grid-cols-2 sm:grid-cols-3">
      {groups.flatMap(({ team, icon, tone, tiles }) =>
        tiles.map((tile) => (
          <Card key={`${team}-${tile.label}`} className="p-5 text-center">
            <span className="mb-2 block text-2xl" aria-hidden="true">
              {tile.icon}
            </span>
            <div className="mb-2 text-xs font-semibold tracking-wide text-[var(--text-secondary)] uppercase">
              {tile.label}
            </div>
            <div className={`font-mono text-2xl leading-none font-bold ${tone}`}>{tile.value}</div>
            <div className="mt-2 text-sm text-[var(--text-secondary)]">
              {icon} {team}
            </div>
          </Card>
        )),
      )}
    </div>
  );
}
