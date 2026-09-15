export function Navbar() {
  return (
    <header className="flex items-center justify-between border-b border-[var(--border)] py-4">
      <div className="flex items-center gap-2.5 font-display text-lg font-extrabold text-[var(--text-primary)]">
        <span className="text-xl" aria-hidden="true">
          ⚽
        </span>
        <span>
          <span className="text-[var(--color-blue)]">ISO</span>Predict
        </span>
      </div>
      <span className="rounded-full border border-[var(--border)] bg-[var(--bg-card)] px-3 py-1 text-xs font-bold tracking-wide text-[var(--text-secondary)] uppercase max-[480px]:hidden">
        IA Football
      </span>
    </header>
  );
}
