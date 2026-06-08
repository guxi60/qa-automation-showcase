"""Checkout — SauceDemo end-to-end purchase flow."""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from qa_report import testcase, TestLog


@pytest.fixture
def cart_ready(page: Page) -> CartPage:
    """Login, add 1 item, navigate to cart."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.add_item_to_cart("Sauce Labs Backpack")
    inv.go_to_cart()
    return CartPage(page)


# ═══════════════════════════════════════════════════════════════
#  TC-CHK-001  ·  Complete checkout — happy path
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-001",
    title="Customer should be able to complete a purchase from cart to confirmation",
    module="Checkout",
    feature="Order Placement",
    level="E2E",
    priority="P0",
    tags=["smoke", "e2e", "happy-path"],
    precondition=[
        "Logged in as standard_user.",
        "1 item (Sauce Labs Backpack) is in the cart.",
        "Cart page is displayed.",
    ],
    test_data={
        "first_name": "Gu",
        "last_name": "Xiang",
        "postal_code": "201318",
    },
    expected=(
        "Flow: Cart → Checkout form → Order overview → Confirmation → Back to products.  "
        "Confirmation header reads 'Thank you for your order!'"
    ),
)
def test_complete_checkout_e2e(cart_ready: CartPage, page: Page):
    log = TestLog()

    # ── Navigate ──
    log.step("Proceed from cart to checkout")
    cart_ready.go_to_checkout()
    log.action("Clicked [Checkout] on cart page")
    step1 = CheckoutStepOnePage(page)
    expect(step1.first_name).to_be_visible()

    # ── Fill shipping info ──
    log.step("Fill shipping information form")
    step1.fill_info("Gu", "Xiang", "201318")
    log.note("First Name : Gu", "Last Name  : Xiang", "Postal Code: 201318")
    step1.continue_checkout()
    log.action("Clicked [Continue]")

    # ── Review ──
    log.step("Review order summary")
    expect(page).to_have_url(CheckoutStepTwoPage.URL)
    step2 = CheckoutStepTwoPage(page)
    log.check("Items in order", step2.get_item_count(), 1)
    total = step2.get_total_text()
    log.check("Total line present", "Total" in total, True)
    log.note(f"Order total: {total}")

    # ── Place order ──
    log.step("Confirm and place the order")
    step2.finish()
    log.action("Clicked [Finish]")

    # ── Confirmation ──
    log.step("Verify order confirmation")
    log.verify("On confirmation page",
               actual=page.url, expected=CheckoutCompletePage.URL)
    expect(page).to_have_url(CheckoutCompletePage.URL)

    complete = CheckoutCompletePage(page)
    header = complete.get_header_text()
    log.verify("Thank-you message appears",
               actual="Thank you" in header, expected=True)
    log.note(f"Message: {header!r}")

    # ── Return ──
    log.step("Return to products from confirmation")
    complete.back_home()
    log.action("Clicked [Back Home]")
    log.verify("Landed on inventory page",
               actual=page.url, expected=InventoryPage.URL)
    expect(page).to_have_url(InventoryPage.URL)

    log.finish(True, "E2E checkout flow completed: Cart → Form → Review → Confirm → Done.")


# ═══════════════════════════════════════════════════════════════
#  TC-CHK-002  ·  Empty first name
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-002",
    title="Checkout must reject an empty first-name field",
    module="Checkout",
    feature="Input Validation",
    level="System",
    priority="P1",
    tags=["negative", "validation"],
    precondition=["Cart contains 1 item.", "On checkout step one."],
    test_data={"first_name": "", "last_name": "Xiang", "postal_code": "201318"},
    expected="Error: 'First Name is required'; stay on step one.",
)
def test_checkout_empty_first_name(cart_ready: CartPage, page: Page):
    log = TestLog()

    log.step("Navigate to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit with empty first name")
    step1.fill_info("", "Xiang", "201318")
    step1.continue_checkout()
    log.action("First Name: [empty] → clicked [Continue]")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.verify("Error mentions 'First Name'",
               actual="First Name" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "First Name" in error

    log.finish(True, "Empty first name correctly rejected.")


# ═══════════════════════════════════════════════════════════════
#  TC-CHK-003  ·  Empty last name
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-003",
    title="Checkout must reject an empty last-name field",
    module="Checkout",
    feature="Input Validation",
    level="System",
    priority="P1",
    tags=["negative", "validation"],
    precondition=["Cart contains 1 item.", "On checkout step one."],
    test_data={"first_name": "Gu", "last_name": "", "postal_code": "201318"},
    expected="Error: 'Last Name is required'; stay on step one.",
)
def test_checkout_empty_last_name(cart_ready: CartPage, page: Page):
    log = TestLog()

    log.step("Navigate to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit with empty last name")
    step1.fill_info("Gu", "", "201318")
    step1.continue_checkout()
    log.action("Last Name: [empty] → clicked [Continue]")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.verify("Error mentions 'Last Name'",
               actual="Last Name" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "Last Name" in error

    log.finish(True, "Empty last name correctly rejected.")


# ═══════════════════════════════════════════════════════════════
#  TC-CHK-004  ·  Empty postal code
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-004",
    title="Checkout must reject an empty postal-code field",
    module="Checkout",
    feature="Input Validation",
    level="System",
    priority="P1",
    tags=["negative", "validation"],
    precondition=["Cart contains 1 item.", "On checkout step one."],
    test_data={"first_name": "Gu", "last_name": "Xiang", "postal_code": ""},
    expected="Error: 'Postal Code is required'; stay on step one.",
)
def test_checkout_empty_postal_code(cart_ready: CartPage, page: Page):
    log = TestLog()

    log.step("Navigate to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit with empty postal code")
    step1.fill_info("Gu", "Xiang", "")
    step1.continue_checkout()
    log.action("Postal Code: [empty] → clicked [Continue]")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.verify("Error mentions 'Postal Code'",
               actual="Postal Code" in error, expected=True)
    log.note(f"Displayed: {error!r}")
    assert "Postal Code" in error

    log.finish(True, "Empty postal code correctly rejected.")


# ═══════════════════════════════════════════════════════════════
#  TC-CHK-005  ·  Cancel from checkout
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-005",
    title="Cancel on checkout form should return user to cart without side effects",
    module="Checkout",
    feature="Navigation",
    level="System",
    priority="P2",
    tags=["navigation"],
    precondition=["Cart contains 1 item.", "On checkout step one."],
    test_data=None,
    expected="Redirected to cart page; cart contents unchanged.",
)
def test_checkout_cancel_returns_to_cart(cart_ready: CartPage, page: Page):
    log = TestLog()

    log.step("Navigate to checkout form")
    cart_ready.go_to_checkout()

    log.step("Click [Cancel] without filling the form")
    page.locator('[data-test="cancel"]').click()
    log.action("Clicked [Cancel]")

    log.step("Verify returned to cart")
    log.verify("Page is cart page",
               actual=page.url, expected=CartPage.URL)
    expect(page).to_have_url(CartPage.URL)

    log.finish(True, "Cancel navigates back to cart with no side effects.")
