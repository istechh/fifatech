import { clsx } from "clsx";
import { Card } from "../ui/Card";
import { fmt } from "../../lib/format";
import type { TeamStats } from "../../types/api";

interface ComparisonTableProps {
  homeStats: TeamStats;
  awayStats: TeamStats;
  homeTeam: string;
  awayTeam: string;
}

interface Row {
  label: string;
  home: number | null;
  away: number | null;
  homeWins: boolean;
}

function greaterWins(a: number | null, b: number | null): boolean {
  return a !== null && b !== null && a > b;
}

function buildRows(home: TeamStats, away: TeamStats): Row[] {
  return [
    {
      label: "🏅 Classement FIFA",
      home: home.rank,
      away: away.rank,
      homeWins: greaterWins(away.rank, home.rank),
    },
    {
      label: "⭐ Points FIFA",
      home: home.total_points,
      away: away.total_points,
      homeWins: greaterWins(home.total_points, away.total_points),
    },
    {
      label: "⚽ Buts marqués (moy.)",
      home: home.avg_goals_scored,
      away: away.avg_goals_scored,
      homeWins: greaterWins(home.avg_goals_scored, away.avg_goals_scored),
    },
    {
      label: "🛡️ Buts encaissés (moy.)",
      home: home.avg_goals_conceded,
      away: away.avg_goals_conceded,
      homeWins: greaterWins(away.avg_goals_conceded, home.avg_goals_conceded),
    },
    {
      label: "📊 Diff. de buts",
      home: home.avg_goal_diff,
      away: away.avg_goal_diff,
      homeWins: greaterWins(home.avg_goal_diff, away.avg_goal_diff),
    },
    {
      label: "📈 Forme récente",
      home: home.avg_outcome,
      away: away.avg_outcome,
      homeWins: greaterWins(home.avg_outcome, away.avg_outcome),
    },
  ];
}

const valueCell = (winner: boolean, tone: string) =>
  clsx(
    "font-mono font-semibold",
    tone,
    winner && "after:ml-1.5 after:text-xs after:opacity-80 after:content-['★']",
  );

export function ComparisonTable({ homeStats, awayStats, homeTeam, awayTeam }: ComparisonTableProps) {
  const rows = buildRows(homeStats, awayStats);

  return (
    <Card className="overflow-hidden p-0">
      {/* Desktop / tablet: real table */}
      <table className="hidden w-full border-collapse sm:table">
        <thead>
          <tr>
            <th className="border-b-2 border-[var(--border)] p-4 text-left text-xs font-semibold text-[var(--text-dim)] uppercase">
              Statistique
            </th>
            <th className="border-b-2 border-[var(--border)] p-4 text-center text-xs font-semibold text-[var(--text-dim)] uppercase">
              🏠 {homeTeam}
            </th>
            <th className="border-b-2 border-[var(--border)] p-4 text-center text-xs font-semibold text-[var(--text-dim)] uppercase">
              ✈️ {awayTeam}
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.label} className="border-b border-[var(--border)] last:border-none">
              <td className="p-4 text-left text-sm text-[var(--text-secondary)]">{row.label}</td>
              <td className={clsx("p-4 text-center", valueCell(row.homeWins, "text-[var(--color-blue)]"))}>
                {fmt(row.home, "N/A")}
              </td>
              <td className={clsx("p-4 text-center", valueCell(!row.homeWins, "text-[var(--color-green)]"))}>
                {fmt(row.away, "N/A")}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile: stacked key/value rows — no horizontal scroll */}
      <dl className="divide-y divide-[var(--border)] sm:hidden">
        {rows.map((row) => (
          <div key={row.label} className="px-4 py-3">
            <dt className="mb-1.5 text-sm text-[var(--text-secondary)]">{row.label}</dt>
            <dd className="flex justify-between text-sm">
              <span
                className={clsx(
                  "flex items-center gap-1",
                  valueCell(row.homeWins, "text-[var(--color-blue)]"),
                )}
              >
                🏠 {fmt(row.home, "N/A")}
              </span>
              <span
                className={clsx(
                  "flex items-center gap-1",
                  valueCell(!row.homeWins, "text-[var(--color-green)]"),
                )}
              >
                ✈️ {fmt(row.away, "N/A")}
              </span>
            </dd>
          </div>
        ))}
      </dl>
    </Card>
  );
}
