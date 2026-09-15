import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";
import type { RecentMatch, TeamStats } from "../../types/api";

interface RecentFormProps {
  homeTeam: string;
  awayTeam: string;
  homeStats: TeamStats;
  awayStats: TeamStats;
}

const TONE_BY_OUTCOME = { W: "win", D: "draw", L: "loss" } as const;
const LABEL_BY_OUTCOME = { W: "Victoire", D: "Match nul", L: "Défaite" } as const;

function TeamForm({ team, matches, dotColor }: { team: string; matches: RecentMatch[]; dotColor: string }) {
  // recent_matches arrives oldest → newest; show the most recent match first.
  const ordered = [...matches].reverse().slice(0, 5);

  return (
    <Card className="p-4.5">
      <div className="mb-4 flex items-center gap-2.5 border-b border-[var(--border)] pb-3 font-semibold text-[var(--text-primary)]">
        <span className={`h-2.5 w-2.5 rounded-full ${dotColor}`} aria-hidden="true" />
        {team}
      </div>
      {ordered.length === 0 ? (
        <p className="py-4 text-center text-sm text-[var(--text-dim)]">Aucun match disponible</p>
      ) : (
        <ul className="space-y-2">
          {ordered.map((m, i) => (
            <li
              key={`${m.date}-${i}`}
              className="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-[var(--bg-card)] px-4 py-3 text-sm"
            >
              <Badge tone={TONE_BY_OUTCOME[m.outcome]} label={LABEL_BY_OUTCOME[m.outcome]}>
                {m.outcome}
              </Badge>
              <span className="flex-1 truncate text-[var(--text-primary)]">vs {m.opponent}</span>
              <span className="text-xs text-[var(--text-dim)]">{m.date}</span>
              <span className="font-mono font-semibold text-[var(--text-primary)]">
                {m.goals_for.toFixed(0)} – {m.goals_against.toFixed(0)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

export function RecentForm({ homeTeam, awayTeam, homeStats, awayStats }: RecentFormProps) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <TeamForm team={homeTeam} matches={homeStats.recent_matches} dotColor="bg-[var(--color-blue)]" />
      <TeamForm team={awayTeam} matches={awayStats.recent_matches} dotColor="bg-[var(--color-green)]" />
    </div>
  );
}
