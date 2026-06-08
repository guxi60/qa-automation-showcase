"""Login tests — SauceDemo authentication scenarios."""

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import TestLog, testcase, get_metadata


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-001",
    category="Functional / Authentication",
    priority="P0 (Smoke)",
    precondition="SauceDemo login page is accessible. User 'standard_user' exists.",
    test_data="standard_user / secret_sauce",
)
def test_login_with_valid_credentials(page: Page):
    """Standard user can log in with valid credentials."""

    log = TestLog()

    log.step("Navigate to SauceDemo login page")
    login = LoginPage(page)
    login.goto()
    log.detail("Opened https://www.saucedemo.com/")

    log.step("Enter valid credentials and submit")
    login.login("standard_user", "secret_sauce")
    log.detail("Username: standard_user", "Password: ********")

    log.step("Verify login succeeded")
    on_inventory = page.url == InventoryPage.URL
    log.verify("Redirected to /inventory.html", on_inventory)
    expect(page).to_have_url(InventoryPage.URL)

    inventory = InventoryPage(page)
    log.verify("Page title shows 'Products'", inventory.is_loaded())
    log.check("Number of products displayed", inventory.get_product_count(), 6)

    log.passed("Valid credentials successfully grant access to the inventory")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-002",
    category="Functional / Authentication",
    priority="P1",
    precondition="SauceDemo login page is accessible.",
    test_data="standard_user / wrong_password (invalid)",
)
def test_login_with_wrong_password(page: Page):
    """User sees clear error when password is incorrect."""

    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Enter valid username + wrong password")
    login.login("standard_user", "wrong_password")
    log.detail("Username: standard_user", "Password: wrong_password")

    log.step("Observe error feedback")
    log.verify("Error message is displayed", login.is_error_visible())
    error = login.get_error_text()
    log.check("Error text mentions 'do not match'", "do not match" in error, True)
    log.detail(f"Displayed message: \"{error}\"")
    # Real assertion
    assert "do not match" in error, f"Unexpected error text: {error}"

    still_on_login = page.url == LoginPage.URL
    log.verify("Still on login page (no redirect)", still_on_login)
    expect(page).to_have_url(LoginPage.URL)

    log.passed("Wrong password correctly rejected with descriptive error")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-003",
    category="Functional / Input Validation",
    priority="P1",
    precondition="SauceDemo login page is accessible.",
    test_data="[empty] / secret_sauce",
)
def test_login_with_empty_username(page: Page):
    """Submitting empty username shows validation error."""

    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Leave username empty, fill password, click Login")
    login.login("", "secret_sauce")
    log.detail("Username: [empty]", "Password: secret_sauce")

    log.step("Verify validation error appears")
    error = login.get_error_text()
    log.check("Error text matches expected", "Username is required" in error, True)
    log.detail(f"Displayed message: \"{error}\"")
    assert "Username is required" in error, f"Unexpected error: {error}"

    log.passed("Empty username field is properly validated")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-004",
    category="Functional / Input Validation",
    priority="P1",
    precondition="SauceDemo login page is accessible.",
    test_data="standard_user / [empty]",
)
def test_login_with_empty_password(page: Page):
    """Submitting empty password shows validation error."""

    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Fill username, leave password empty, click Login")
    login.login("standard_user", "")
    log.detail("Username: standard_user", "Password: [empty]")

    log.step("Verify validation error appears")
    error = login.get_error_text()
    log.check("Error text matches expected", "Password is required" in error, True)
    log.detail(f"Displayed message: \"{error}\"")
    assert "Password is required" in error, f"Unexpected error: {error}"

    log.passed("Empty password field is properly validated")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-005",
    category="Functional / Access Control",
    priority="P1",
    precondition="SauceDemo login page is accessible. User 'locked_out_user' exists.",
    test_data="locked_out_user / secret_sauce",
)
def test_locked_out_user_cannot_login(page: Page):
    """Locked-out user is blocked with appropriate message."""

    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Attempt login as locked-out user")
    login.login("locked_out_user", "secret_sauce")
    log.detail("Username: locked_out_user")

    log.step("Verify access is denied")
    error = login.get_error_text()
    log.check("Error mentions 'locked out'", "locked out" in error.lower(), True)
    log.detail(f"Displayed message: \"{error}\"")
    assert "locked out" in error.lower(), f"Unexpected error: {error}"

    still_on_login = page.url == LoginPage.URL
    log.verify("Still on login page", still_on_login)
    expect(page).to_have_url(LoginPage.URL)

    log.passed("Locked-out user correctly denied access")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-006",
    category="GUI / Smoke",
    priority="P0 (Smoke)",
    precondition="SauceDemo login page is accessible.",
    test_data="N/A — no interaction required",
)
def test_login_page_elements_visible(page: Page):
    """Login page renders all required form elements on initial load."""

    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Verify all form controls are visible and correct")
    log.check("Username input field visible",
              login.username_input.is_visible(), True)
    log.check("Password input field visible",
              login.password_input.is_visible(), True)
    log.check("Login button visible",
              login.login_button.is_visible(), True)
    log.check("Login button text",
              login.login_button.input_value(), "Login")

    # Real assertions
    expect(login.username_input).to_be_visible()
    expect(login.password_input).to_be_visible()
    expect(login.login_button).to_be_visible()
    expect(login.login_button).to_have_value("Login")

    log.passed("All login page elements render correctly on initial load")
