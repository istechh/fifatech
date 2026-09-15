import { clsx } from "clsx";
import type { ComponentPropsWithoutRef } from "react";

type CardProps = ComponentPropsWithoutRef<"div">;

/** Shared card surface — every card-like block in the app (stat tiles,
 * prediction result, chart wrappers, match rows) renders on this same
 * background/border pair so the UI reads as one system. */
export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={clsx("rounded-2xl border border-[var(--border)] bg-[var(--bg-card)]", className)}
      {...props}
    />
  );
}
