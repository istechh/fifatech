interface TeamSelectProps {
  id: string;
  label: string;
  teams: string[];
  value: string;
  onChange: (team: string) => void;
}

export function TeamSelect({ id, label, teams, value, onChange }: TeamSelectProps) {
  return (
    <div>
      <label
        htmlFor={id}
        className="mb-2 flex items-center gap-1.5 text-xs font-semibold tracking-wide text-[var(--text-secondary)] uppercase"
      >
        {label}
      </label>
      <select
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border border-[var(--border)] bg-white px-3 py-2.5 text-base font-medium text-[var(--text-primary)] transition-colors hover:border-[var(--color-blue)] focus:border-[var(--color-blue)] focus:outline-none"
      >
        {teams.map((team) => (
          <option key={team} value={team}>
            {team}
          </option>
        ))}
      </select>
    </div>
  );
}
