import { describe, expect, it } from "vitest";
import { fmt } from "./format";

describe("fmt", () => {
  it("returns the em-dash placeholder for null", () => {
    expect(fmt(null)).toBe("—");
  });

  it("returns the em-dash placeholder for undefined", () => {
    expect(fmt(undefined)).toBe("—");
  });

  it("renders 0 as a real value, not as missing", () => {
    // Regression guard: a naive `value || '—'` check would treat a
    // legitimate 0 (e.g. neutral recent form) as "missing data".
    expect(fmt(0)).toBe("0");
  });

  it("renders a positive number as-is", () => {
    expect(fmt(42)).toBe("42");
  });

  it("supports a custom empty placeholder", () => {
    expect(fmt(null, "N/A")).toBe("N/A");
  });
});
