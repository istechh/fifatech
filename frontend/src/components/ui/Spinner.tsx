interface SpinnerProps {
  label: string;
}

export function Spinner({ label }: SpinnerProps) {
  return (
    <div role="status" aria-live="polite" className="flex items-center justify-center gap-3 py-8">
      <span
        aria-hidden="true"
        className="h-5 w-5 animate-spin rounded-full border-2 border-[var(--border)] border-t-[var(--color-blue)]"
      />
      <span className="text-sm text-[var(--text-secondary)]">{label}</span>
    </div>
  );
}
