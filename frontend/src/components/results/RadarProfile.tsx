import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Card } from "../ui/Card";
import { buildRadarData } from "../../lib/radar";
import type { TeamStats } from "../../types/api";

interface RadarProfileProps {
  homeStats: TeamStats;
  awayStats: TeamStats;
  homeTeam: string;
  awayTeam: string;
}

export function RadarProfile({ homeStats, awayStats, homeTeam, awayTeam }: RadarProfileProps) {
  const data = buildRadarData(homeStats, awayStats).map((point) => ({
    category: point.category,
    [homeTeam]: point.home,
    [awayTeam]: point.away,
  }));

  return (
    <Card className="p-3">
      <div className="h-[380px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data} outerRadius="70%">
            <PolarGrid stroke="rgba(0,0,0,0.06)" />
            <PolarAngleAxis dataKey="category" tick={{ fill: "#475569", fontSize: 12 }} />
            <PolarRadiusAxis angle={90} domain={[0, 10]} tick={{ fill: "#64748b", fontSize: 9 }} />
            <Radar name={homeTeam} dataKey={homeTeam} stroke="#4f8cff" fill="#4f8cff" fillOpacity={0.15} />
            <Radar name={awayTeam} dataKey={awayTeam} stroke="#22c55e" fill="#22c55e" fillOpacity={0.15} />
            <Legend wrapperStyle={{ fontSize: 12, color: "#0f172a" }} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
