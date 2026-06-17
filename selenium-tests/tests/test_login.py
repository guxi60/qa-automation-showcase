"""Login tests — Selenium edition, Allure-native, DDT-driven.

Shares test_data with Playwright (same JSON, same test case IDs).
"""

import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import load_data, set_meta, step, action, note


@allure.feature("Authentication")
@pytest.mark.parametrize("tc", load_data("login.json")["login"])
def test_login(driver, tc: dict):
    """
    Data-driven login test.

    Each JSON entry drives one test case.  The *tc* dict carries
    id, title, story, severity, tags, username, password, and
    optionally expected_error (for negative cases).
    """
    set_meta(tc)

    # ── Navigate ──
    with step("Navigate to SauceDemo login page"):
        login = LoginPage(driver)
        login.goto()
    action("Opened https://www.saucedemo.com/")

    # ── Act ──
    with step(f"Submit credentials  |  user={tc.get('username')!r}"):
        login.login(tc["username"], tc["password"])
    action(
        f"Filled username={tc['username']!r}  "
        f"password={'***' if tc['password'] else '[empty]'}  "
        f"→ clicked [Login]"
    )

    # ── Assert ──
    expected_error = tc.get("expected_error", "")
    if expected_error:
        with step(f"Verify error message contains {expected_error!r}"):
            error = login.get_error_text()
            assert expected_error in error, (
                f"Expected error containing {expected_error!r}, got {error!r}"
            )
            note(f"Displayed: {error!r}")
            assert driver.current_url == LoginPage.URL
    else:
        # TC-LOGIN-001 — success path
        with step("Verify redirect to inventory page"):
            assert driver.current_url == InventoryPage.URL
        inventory = InventoryPage(driver)
        with step("Verify inventory is populated"):
            assert inventory.is_loaded(), "Page title should be 'Products'"
            assert inventory.get_product_count() == 6


@allure.feature("Authentication")
@pytest.mark.smoke
def test_login_page_elements_visible(driver):
    """TC-LOGIN-006 — Static GUI check (not parametrized — no interaction)."""
    tc = {
        "id": "TC-LOGIN-006",
        "title": "Login page renders all required form elements on initial load",
        "story": "Page layout",
        "severity": "BLOCKER",
        "tags": ["smoke", "gui"],
        "level": "System",
        "req": "REQ-AUTH-006",
    }
    set_meta(tc)

    with step("Navigate to login page"):
        login = LoginPage(driver)
        login.goto()

    with step("Verify all form controls are present and visible"):
        assert login.username_input.is_displayed(), "Username input not visible"
        assert login.password_input.is_displayed(), "Password input not visible"
        assert login.login_button.is_displayed(), "Login button not visible"
        assert login.login_button.get_attribute("value") == "Login"

    action("Username input ✓", "Password input ✓", "Login button ✓")
