import { Alert } from "../ui/Alert";
import { Button } from "../ui/Button";
import { TeamSelect } from "./TeamSelect";

interface MatchSelectorProps {
  teams: string[];
  homeTeam: string;
  awayTeam: string;
  neutral: boolean;
  loading: boolean;
  onHomeChange: (team: string) => void;
  onAwayChange: (team: string) => void;
  onNeutralChange: (neutral: boolean) => void;
  onSubmit: () => void;
}

export function MatchSelector({
  teams,
  homeTeam,
  awayTeam,
  neutral,
  loading,
  onHomeChange,
  onAwayChange,
  onNeutralChange,
  onSubmit,
}: MatchSelectorProps) {
  const sameTeam = homeTeam === awayTeam;

  return (
    <form
      className="mt-5"
      onSubmit={(e) => {
        e.preventDefault();
        if (!sameTeam) onSubmit();
      }}
    >
      <div className="grid grid-cols-1 items-end gap-4 sm:grid-cols-[1fr_auto_1fr]">
        <TeamSelect
          id="home-team"
          label="🏠 Équipe Domicile"
          teams={teams}
          value={homeTeam}
          onChange={onHomeChange}
        />

        <div className="flex justify-center py-1 sm:py-0" aria-hidden="true">
          <span className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] px-3.5 py-1.5 font-mono text-sm font-bold text-[var(--text-dim)]">
            VS
          </span>
        </div>

        <TeamSelect
          id="away-team"
          label="✈️ Équipe Extérieur"
          teams={teams}
          value={awayTeam}
          onChange={onAwayChange}
        />
      </div>

      <label className="mt-4 flex items-center gap-2 text-sm text-[var(--text-secondary)]">
        <input
          type="checkbox"
          checked={neutral}
          onChange={(e) => onNeutralChange(e.target.checked)}
          className="h-4 w-4 accent-[var(--color-blue)]"
        />
        🏟️ Match sur terrain neutre
      </label>

      {sameTeam && (
        <div className="mt-4">
          <Alert variant="warning">Choisissez deux équipes différentes pour lancer une prédiction.</Alert>
        </div>
      )}

      <div className="mt-5 flex justify-center">
        <Button type="submit" disabled={sameTeam || loading} className="w-full max-w-sm">
          🔮 Lancer la Prédiction
        </Button>
      </div>
    </form>
  );
}
