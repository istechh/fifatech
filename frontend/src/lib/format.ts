/** Format a stat for display, treating 0 as a real value — never fall back
 * to "missing" just because a number happens to be falsy. */
export function fmt(value: number | null | undefined, empty = "—"): string {
  return value === null || value === undefined ? empty : String(value);
}
