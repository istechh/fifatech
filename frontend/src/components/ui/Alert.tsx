import { clsx } from "clsx";
import type { ReactNode } from "react";

type AlertVariant = "error" | "warning" | "info";

const VARIANT_STYLES: Record<AlertVariant, string> = {
  error: "border-[var(--color-red)]/30 bg-red-50 text-red-800",
  warning: "border-[var(--color-gold)]/30 bg-amber-50 text-amber-900",
  info: "border-[var(--color-blue)]/30 bg-blue-50 text-blue-900",
};

const ICON: Record<AlertVariant, string> = {
  error: "⚠️",
  warning: "⚠️",
  info: "ℹ️",
};

interface AlertProps {
  variant: AlertVariant;
  children: ReactNode;
}

export function Alert({ variant, children }: AlertProps) {
  return (
    <div
      // "alert" interrupts (errors, blocking validation warnings) —
      // "status" is a polite, non-interrupting update (info banners).
      role={variant === "info" ? "status" : "alert"}
      className={clsx(
        "flex items-start gap-2 rounded-xl border px-4 py-3 text-sm font-medium",
        VARIANT_STYLES[variant],
      )}
    >
      <span aria-hidden="true">{ICON[variant]}</span>
      <span>{children}</span>
    </div>
  );
}
