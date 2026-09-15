import { afterEach, describe, expect, it, vi } from "vitest";
import { api, ApiError } from "./api";

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function htmlResponse(status: number): Response {
  // Mirrors what Render's proxy can return while a service is waking up:
  // an HTML error page instead of the API's JSON.
  return new Response("<html><body>502 Bad Gateway</body></html>", {
    status,
    headers: { "Content-Type": "text/html" },
  });
}

describe("api client", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns parsed JSON on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ teams: ["France", "Brazil"], count: 2 })),
    );
    const res = await api.getTeams();
    expect(res.teams).toEqual(["France", "Brazil"]);
  });

  it("surfaces the backend's JSON `detail` message on an HTTP error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(jsonResponse({ detail: "Équipe 'X' introuvable" }, 404)),
    );
    await expect(api.getTeamStats("X")).rejects.toMatchObject({
      message: "Équipe 'X' introuvable",
    });
  });

  it("does not crash on a non-JSON error body (e.g. a proxy's HTML 502 page)", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(htmlResponse(502)));
    await expect(api.getTeams()).rejects.toBeInstanceOf(ApiError);
    await expect(api.getTeams()).rejects.toMatchObject({
      message: expect.stringContaining("502"),
    });
  });

  it("reports a friendly message on a network failure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
    await expect(api.getTeams()).rejects.toMatchObject({
      message: expect.stringContaining("non disponible"),
    });
  });

  it("reports a friendly message when the request times out", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new DOMException("The operation was aborted.", "AbortError")),
    );
    await expect(api.getTeams()).rejects.toMatchObject({
      message: expect.stringContaining("trop de temps"),
    });
  });

  it("URL-encodes team names when fetching stats", async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(jsonResponse({ team: "Côte d'Ivoire" }));
    vi.stubGlobal("fetch", fetchMock);
    await api.getTeamStats("Côte d'Ivoire");
    const calledUrl = fetchMock.mock.calls[0][0] as string;
    expect(calledUrl).toContain(encodeURIComponent("Côte d'Ivoire"));
  });
});
