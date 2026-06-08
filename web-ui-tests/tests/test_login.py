"""Login tests — Allure-native, DDT-driven."""

import allure
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import load_data, set_meta, step, action, note


@allure.feature("Authentication")
@pytest.mark.parametrize("tc", load_data("login.json")["login"])
def test_login(page: Page, tc: dict):
    """
    Data-driven login test.

    Each JSON entry drives one test case.  The *tc* dict carries
    id, title, story, severity, tags, username, password, and
    optionally expected_error (for negative cases).
    """
    set_meta(tc)

    # ── Navigate ──
    with step("Navigate to SauceDemo login page"):
        login = LoginPage(page)
        login.goto()
    action("Opened https://www.saucedemo.com/")

    # ── Act ──
    with step(f"Submit credentials  |  user={tc.get('username')!r}"):
        login.login(tc["username"], tc["password"])
    action(f"Filled username={tc['username']!r}  password={'***' if tc['password'] else '[empty]'}  → clicked [Login]")

    # ── Assert ──
    expected_error = tc.get("expected_error", "")
    if expected_error:
        with step(f"Verify error message contains {expected_error!r}"):
            error = login.get_error_text()
            assert expected_error in error, (
                f"Expected error containing {expected_error!r}, got {error!r}"
            )
            note(f"Displayed: {error!r}")
            expect(page).to_have_url(LoginPage.URL)
    else:
        # TC-LOGIN-001 etc. — success path
        with step(f"Verify redirect to inventory page"):
            expect(page).to_have_url(InventoryPage.URL)
        inventory = InventoryPage(page)
        with step("Verify inventory is populated"):
            assert inventory.is_loaded(), "Page title should be 'Products'"
            assert inventory.get_product_count() == 6


@allure.feature("Authentication")
def test_login_page_elements_visible(page: Page):
    """TC-LOGIN-006 — Static GUI check (not parametrized — no interaction)."""
    tc = {
        "id": "TC-LOGIN-006",
        "title": "Login page renders all required form elements on initial load",
        "story": "Page layout",
        "severity": "BLOCKER",
        "tags": ["smoke", "gui"],
        "level": "System",
    }
    set_meta(tc)

    with step("Navigate to login page"):
        login = LoginPage(page)
        login.goto()

    with step("Verify all form controls are present and visible"):
        expect(login.username_input).to_be_visible()
        expect(login.password_input).to_be_visible()
        expect(login.login_button).to_be_visible()
        expect(login.login_button).to_have_value("Login")

    action("Username input ✓", "Password input ✓", "Login button ✓")
