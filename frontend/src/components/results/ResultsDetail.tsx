import type { ReactNode } from "react";

interface ResultsDetailProps {
  children: ReactNode;
}

/** Native <details>/<summary> disclosure — keeps the prediction + key stats
 * as the immediately visible "essential" answer, with the heavier
 * comparison/charts/history moved behind one explicit click. Using the
 * native element means keyboard and screen-reader support come for free. */
export function ResultsDetail({ children }: ResultsDetailProps) {
  return (
    <details className="group mt-6">
      <summary className="flex cursor-pointer list-none items-center gap-2 rounded-xl border border-[var(--border)] bg-[var(--bg-card)] px-5 py-3.5 text-sm font-semibold text-[var(--text-primary)] transition-colors hover:border-[var(--border-active)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-blue)]">
        <span aria-hidden="true">📊</span>
        Voir l'analyse détaillée (comparatif, profil, forme, historique)
        <span className="ml-auto transition-transform group-open:rotate-180" aria-hidden="true">
          ⌄
        </span>
      </summary>
      <div className="mt-5 space-y-8">{children}</div>
    </details>
  );
}
