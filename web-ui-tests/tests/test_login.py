"""Login tests for SauceDemo — normal, error, boundary, and locked user."""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# ── Normal login ──────────────────────────────────────────────

@pytest.mark.smoke
def test_login_with_valid_credentials(page: Page):
    """Standard user can log in and land on inventory page."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    expect(page).to_have_url(InventoryPage.URL)
    inventory = InventoryPage(page)
    assert inventory.is_loaded(), "Inventory page should show 'Products' title"


# ── Login errors ──────────────────────────────────────────────

def test_login_with_wrong_password(page: Page):
    """Error message shown when password is incorrect."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "wrong_password")

    assert login.is_error_visible(), "Error message should be displayed"
    error = login.get_error_text()
    assert "do not match" in error, f"Unexpected error text: {error}"
    expect(page).to_have_url(LoginPage.URL)  # still on login page


def test_login_with_empty_username(page: Page):
    """Error message shown when username is empty."""
    login = LoginPage(page)
    login.goto()
    login.login("", "secret_sauce")

    error = login.get_error_text()
    assert "Username is required" in error, f"Unexpected error text: {error}"


def test_login_with_empty_password(page: Page):
    """Error message shown when password is empty."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "")

    error = login.get_error_text()
    assert "Password is required" in error, f"Unexpected error text: {error}"


# ── Locked out user ───────────────────────────────────────────

def test_locked_out_user_cannot_login(page: Page):
    """Locked-out user sees appropriate error and cannot proceed."""
    login = LoginPage(page)
    login.goto()
    login.login("locked_out_user", "secret_sauce")

    error = login.get_error_text()
    assert "locked out" in error.lower(), f"Unexpected error: {error}"
    expect(page).to_have_url(LoginPage.URL)


# ── UI elements presence ──────────────────────────────────────

def test_login_page_elements_visible(page: Page):
    """All required login form elements are visible on page load."""
    login = LoginPage(page)
    login.goto()

    expect(login.username_input).to_be_visible()
    expect(login.password_input).to_be_visible()
    expect(login.login_button).to_be_visible()
    expect(login.login_button).to_have_value("Login")
