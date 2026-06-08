"""Login — SauceDemo authentication scenarios."""

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import testcase, TestLog


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-001  ·  Happy path — valid credentials
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-001",
    title="Valid credentials should grant access to the product inventory",
    module="Authentication",
    feature="Login",
    level="System",
    priority="P0",
    tags=["smoke", "happy-path"],
    precondition=[
        "SauceDemo login page is reachable.",
        "User 'standard_user' exists in the system.",
    ],
    test_data={"username": "standard_user", "password": "secret_sauce"},
    expected="Redirect to /inventory.html; 'Products' heading visible; 6 products listed.",
)
def test_login_with_valid_credentials(page: Page):
    log = TestLog()

    # ── Step 1 ──
    log.step("Navigate to SauceDemo login page")
    login = LoginPage(page)
    login.goto()
    log.action("Opened https://www.saucedemo.com/")
    log.check("Login button is visible", login.login_button.is_visible(), True)
    log.check("Username field is visible", login.username_input.is_visible(), True)
    log.check("Password field is visible", login.password_input.is_visible(), True)
    # assertions
    expect(login.login_button).to_be_visible()

    # ── Step 2 ──
    log.step("Enter valid credentials and submit")
    login.login("standard_user", "secret_sauce")
    log.action('Filled "standard_user" / "********" → clicked [Login]')

    # ── Step 3 ──
    log.step("Verify successful authentication")
    log.verify("URL is /inventory.html",
               actual=page.url, expected=InventoryPage.URL)
    expect(page).to_have_url(InventoryPage.URL)

    inventory = InventoryPage(page)
    log.verify("Page heading is 'Products'",
               actual=inventory.is_loaded(), expected=True)
    log.check("Product count", inventory.get_product_count(), 6)
    assert inventory.get_product_count() == 6

    log.finish(True, "User authenticated and landed on inventory page.")


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-002  ·  Wrong password
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-002",
    title="Wrong password should be rejected with a descriptive error",
    module="Authentication",
    feature="Login",
    level="System",
    priority="P1",
    tags=["negative", "validation"],
    precondition=["Login page is reachable."],
    test_data={"username": "standard_user", "password": "wrong_password"},
    expected="Error banner: 'Username and password do not match…'; stay on login page.",
)
def test_login_with_wrong_password(page: Page):
    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Submit valid username with an incorrect password")
    login.login("standard_user", "wrong_password")
    log.action('Filled "standard_user" / "wrong_password" → clicked [Login]')

    log.step("Verify error feedback")
    log.check("Error banner is displayed", login.is_error_visible(), True)
    error = login.get_error_text()
    log.verify("Error mentions credentials mismatch",
               actual="do not match" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "do not match" in error

    log.verify("Still on login page (no redirect)",
               actual=page.url, expected=LoginPage.URL)
    expect(page).to_have_url(LoginPage.URL)

    log.finish(True, "Wrong password correctly rejected.")


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-003  ·  Empty username
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-003",
    title="Empty username should trigger client-side validation",
    module="Authentication",
    feature="Login",
    level="System",
    priority="P1",
    tags=["negative", "validation", "boundary"],
    precondition=["Login page is reachable."],
    test_data={"username": "", "password": "secret_sauce"},
    expected="Error banner: 'Username is required'; stay on login page.",
)
def test_login_with_empty_username(page: Page):
    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Submit with empty username field")
    login.login("", "secret_sauce")
    log.action('Filled "" / "secret_sauce" → clicked [Login]')

    log.step("Verify validation error")
    error = login.get_error_text()
    log.verify("Error says 'Username is required'",
               actual="Username is required" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "Username is required" in error

    log.finish(True, "Empty username correctly validated.")


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-004  ·  Empty password
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-004",
    title="Empty password should trigger client-side validation",
    module="Authentication",
    feature="Login",
    level="System",
    priority="P1",
    tags=["negative", "validation", "boundary"],
    precondition=["Login page is reachable."],
    test_data={"username": "standard_user", "password": ""},
    expected="Error banner: 'Password is required'; stay on login page.",
)
def test_login_with_empty_password(page: Page):
    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Submit with empty password field")
    login.login("standard_user", "")
    log.action('Filled "standard_user" / "" → clicked [Login]')

    log.step("Verify validation error")
    error = login.get_error_text()
    log.verify("Error says 'Password is required'",
               actual="Password is required" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "Password is required" in error

    log.finish(True, "Empty password correctly validated.")


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-005  ·  Locked-out user
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-005",
    title="Locked-out user must be denied access with a clear explanation",
    module="Authentication",
    feature="Login",
    level="System",
    priority="P1",
    tags=["negative", "access-control"],
    precondition=[
        "Login page is reachable.",
        "Account 'locked_out_user' exists in locked state.",
    ],
    test_data={"username": "locked_out_user", "password": "secret_sauce"},
    expected="Error banner: '…this user has been locked out'; stay on login page.",
)
def test_locked_out_user_cannot_login(page: Page):
    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Attempt login as locked-out user")
    login.login("locked_out_user", "secret_sauce")
    log.action('Filled "locked_out_user" / "********" → clicked [Login]')

    log.step("Verify access is denied")
    error = login.get_error_text()
    log.verify("Error mentions 'locked out'",
               actual="locked out" in error.lower(), expected=True)
    log.note(f"Displayed: {error!r}")
    assert "locked out" in error.lower()

    log.verify("Still on login page",
               actual=page.url, expected=LoginPage.URL)
    expect(page).to_have_url(LoginPage.URL)

    log.finish(True, "Locked-out user correctly denied access.")


# ═══════════════════════════════════════════════════════════════
#  TC-LOGIN-006  ·  Element integrity on page load
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-LOGIN-006",
    title="Login page must render all required form elements on initial load",
    module="GUI",
    feature="Login",
    level="System",
    priority="P0",
    tags=["smoke", "gui", "static"],
    precondition=["Login page is reachable."],
    test_data=None,
    expected="Username input, password input, and Login button are all visible. Login button text = 'Login'.",
)
def test_login_page_elements_visible(page: Page):
    log = TestLog()

    log.step("Navigate to login page")
    login = LoginPage(page)
    login.goto()

    log.step("Verify all form controls are present and visible")
    log.check("Username input", login.username_input.is_visible(), True)
    log.check("Password input", login.password_input.is_visible(), True)
    log.check("Login button",   login.login_button.is_visible(), True)
    log.verify("Login button text",
               actual=login.login_button.input_value(),
               expected="Login")

    # assertions
    expect(login.username_input).to_be_visible()
    expect(login.password_input).to_be_visible()
    expect(login.login_button).to_be_visible()
    expect(login.login_button).to_have_value("Login")

    log.finish(True, "All login form elements render correctly.")
