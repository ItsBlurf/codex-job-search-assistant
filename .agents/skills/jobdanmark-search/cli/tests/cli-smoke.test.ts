import { describe, expect, test } from "bun:test";
import { runCLI, parseJSON } from "./helpers";

describe("jobdanmark CLI smoke", () => {
  test("--help prints command metadata", async () => {
    const result = await runCLI(["--help"]);
    expect(result.exitCode).toBe(0);
    const payload = parseJSON<{ ok: boolean; data?: { text?: string } }>(result);
    expect(payload.ok).toBe(true);
    expect(payload.data?.text).toContain("jobdanmark-cli");
    expect(payload.data?.text).toContain("search");
  });

  test("unknown command exits nonzero", async () => {
    const result = await runCLI(["unknown"]);
    expect(result.exitCode).not.toBe(0);
    expect(`${result.stdout}\n${result.stderr}`).toContain("command-not-found");
  });
});
