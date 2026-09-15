import { Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "../ui/Card";
import type { TeamStats } from "../../types/api";

interface GoalsEvolutionProps {
  homeStats: TeamStats;
  awayStats: TeamStats;
  homeTeam: string;
  awayTeam: string;
}

export function GoalsEvolution({ homeStats, awayStats, homeTeam, awayTeam }: GoalsEvolutionProps) {
  const length = Math.max(homeStats.recent_matches.length, awayStats.recent_matches.length, 1);
  const data = Array.from({ length }, (_, i) => ({
    match: i + 1,
    [homeTeam]: homeStats.recent_matches[i]?.goals_for ?? null,
    [awayTeam]: awayStats.recent_matches[i]?.goals_for ?? null,
  }));

  return (
    <Card className="p-3">
      <div className="h-[280px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 20, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
            <XAxis dataKey="match" tick={{ fill: "#64748b", fontSize: 10 }} tickLine={false} />
            <YAxis
              tick={{ fill: "#64748b", fontSize: 10 }}
              tickLine={false}
              label={{
                value: "Buts marqués",
                angle: -90,
                position: "insideLeft",
                style: { fill: "#475569", fontSize: 11 },
              }}
            />
            <Tooltip contentStyle={{ borderRadius: 12, borderColor: "var(--border)", fontSize: 12 }} />
            <Legend wrapperStyle={{ fontSize: 11, color: "#0f172a" }} />
            <Area
              type="monotone"
              dataKey={homeTeam}
              stroke="#4f8cff"
              fill="#4f8cff"
              fillOpacity={0.07}
              strokeWidth={3}
              connectNulls
            />
            <Area
              type="monotone"
              dataKey={awayTeam}
              stroke="#22c55e"
              fill="#22c55e"
              fillOpacity={0.07}
              strokeWidth={3}
              connectNulls
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
