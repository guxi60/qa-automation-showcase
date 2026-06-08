"""Quick smoke test to verify Playwright environment is working."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_saucedemo_homepage_loads(page: Page):
    """Verify SauceDemo homepage loads correctly."""
    page.goto("https://www.saucedemo.com/")

    # Check key elements are visible
    expect(page.locator('[data-test="login-button"]')).to_be_visible()
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()


@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page):
    """Verify a standard user can log in successfully."""
    page.goto("https://www.saucedemo.com/")

    page.fill('[data-test="username"]', "standard_user")
    page.fill('[data-test="password"]', "secret_sauce")
    page.click('[data-test="login-button"]')

    # Should redirect to inventory page
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")
