export function Hero() {
  return (
    <div className="px-2 py-10 text-center sm:px-4">
      <span className="mb-5 inline-flex items-center gap-1.5 rounded-full border border-[var(--border)] bg-[var(--bg-card)] px-3.5 py-1.5 text-xs font-semibold tracking-wide text-[var(--text-secondary)] uppercase before:text-[0.5rem] before:text-[var(--color-blue)] before:content-['●']">
        Prédiction par Intelligence Artificielle
      </span>
      <h1 className="font-display text-[clamp(1.8rem,4vw,2.8rem)] leading-tight font-extrabold tracking-tight text-[var(--text-primary)]">
        Prédisez le <span className="text-[var(--color-blue)]">résultat</span> avant le coup de sifflet
      </h1>
    </div>
  );
}
