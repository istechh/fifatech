import { clsx } from "clsx";
import type { ReactNode } from "react";

type BadgeTone = "win" | "draw" | "loss";

const TONE_STYLES: Record<BadgeTone, string> = {
  win: "bg-emerald-100 text-[var(--color-green)]",
  draw: "bg-amber-100 text-[var(--color-gold)]",
  loss: "bg-red-100 text-[var(--color-red)]",
};

interface BadgeProps {
  tone: BadgeTone;
  children: ReactNode;
  label: string;
}

export function Badge({ tone, children, label }: BadgeProps) {
  return (
    <span
      role="img"
      aria-label={label}
      className={clsx(
        "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-xs font-bold",
        TONE_STYLES[tone],
      )}
    >
      {children}
    </span>
  );
}
