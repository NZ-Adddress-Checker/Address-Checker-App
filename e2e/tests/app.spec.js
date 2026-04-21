import { test, expect } from "@playwright/test";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

test.describe("Backend health", () => {
  test("health endpoint returns status ok", async ({ request }) => {
    const response = await request.get(`${BACKEND_URL}/health`);
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(body.status).toBe("ok");
  });
});

test.describe("Login page", () => {
  test("renders app title", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: "NZ Address Checker" })).toBeVisible();
  });

  test("renders login button when Cognito is configured", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("button", { name: "Login" })).toBeVisible();
  });

  test("login button is enabled", async ({ page }) => {
    await page.goto("/");
    const loginBtn = page.getByRole("button", { name: "Login" });
    await expect(loginBtn).toBeEnabled();
  });
});
