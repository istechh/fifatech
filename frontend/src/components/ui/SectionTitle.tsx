import type { ReactNode } from "react";

export function SectionTitle({ children }: { children: ReactNode }) {
  return (
    <h2 className="mb-3 flex items-center gap-2.5 text-base font-bold text-[var(--text-primary)]">
      <span className="h-2 w-2 shrink-0 rounded-full bg-[var(--color-blue)]" aria-hidden="true" />
      {children}
    </h2>
  );
}
