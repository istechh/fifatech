import "@testing-library/jest-dom/vitest";

// jsdom has no ResizeObserver — Recharts' <ResponsiveContainer> needs one.
class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
(globalThis as any).ResizeObserver = ResizeObserverMock;
