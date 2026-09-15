import { clsx } from "clsx";
import type { ComponentPropsWithoutRef } from "react";

type ButtonProps = ComponentPropsWithoutRef<"button">;

export function Button({ className, ...props }: ButtonProps) {
  return (
    <button
      type="button"
      className={clsx(
        "inline-flex items-center justify-center gap-2 rounded-xl px-6 py-3",
        "text-base font-semibold text-white transition-colors",
        "bg-[var(--color-blue)] hover:bg-[var(--color-blue-hover)]",
        "disabled:cursor-not-allowed disabled:border disabled:border-[var(--border)]",
        "disabled:bg-[var(--bg-card-hover)] disabled:text-[var(--text-dim)]",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-blue)]",
        className,
      )}
      {...props}
    />
  );
}
