"""Checkout flow tests — SauceDemo end-to-end purchase scenarios."""

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
from qa_report import TestLog, testcase


@pytest.fixture
def cart_ready(page: Page) -> CartPage:
    """Log in, add 1 item, go to cart — ready for checkout."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.go_to_cart()
    return CartPage(page)


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-001",
    category="E2E / Checkout",
    priority="P0 (Smoke)",
    precondition=(
        "Logged in as standard_user. "
        "1 item (Sauce Labs Backpack) in cart. "
        "On cart page."
    ),
    test_data="First: Gu | Last: Xiang | Postal: 201318",
)
def test_complete_checkout_e2e(cart_ready: CartPage, page: Page):
    """Full checkout flow: info → review → place order → confirmation."""

    log = TestLog()

    # ── Navigate to checkout form ──
    log.step("Proceed to checkout from cart")
    cart_ready.go_to_checkout()
    log.detail("Clicked [Checkout] on cart page")

    step1 = CheckoutStepOnePage(page)
    log.verify("On checkout step one form", step1.first_name.is_visible())
    expect(step1.first_name).to_be_visible()

    # ── Fill shipping info ──
    log.step("Fill shipping / billing information")
    step1.fill_info("Gu", "Xiang", "201318")
    log.detail("First Name: Gu", "Last Name: Xiang", "Postal Code: 201318")
    step1.continue_checkout()
    log.detail("Clicked [Continue]")

    # ── Review order ──
    log.step("Review order overview before confirming")
    expect(page).to_have_url(CheckoutStepTwoPage.URL)
    step2 = CheckoutStepTwoPage(page)
    log.check("Items in order", step2.get_item_count(), 1)

    total = step2.get_total_text()
    log.check("Total amount displayed", "Total" in total, True)
    log.detail(f"Order total: {total}")

    # ── Place order ──
    log.step("Confirm and place the order")
    step2.finish()
    log.detail("Clicked [Finish]")

    # ── Verify confirmation ──
    complete = CheckoutCompletePage(page)
    log.verify("Redirected to order confirmation page",
               page.url == CheckoutCompletePage.URL)
    expect(page).to_have_url(CheckoutCompletePage.URL)

    header = complete.get_header_text()
    log.verify("Confirmation shows thank-you message",
               "Thank you" in header)
    log.detail(f"Confirmation message: \"{header}\"")

    # ── Return to products ──
    log.step("Return to products page")
    complete.back_home()
    log.verify("Back-home returns to inventory",
               page.url == InventoryPage.URL)
    expect(page).to_have_url(InventoryPage.URL)

    log.passed(
        "E2E checkout flow completed successfully: "
        "fill info → review → confirm → thank-you → back to shopping"
    )


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-002",
    category="Functional / Input Validation",
    priority="P1",
    precondition="Cart contains 1 item. On checkout step one.",
    test_data="First Name: [empty] | Last: Xiang | Postal: 201318",
)
def test_checkout_empty_first_name(cart_ready: CartPage, page: Page):
    """Submitting checkout form without first name shows error."""

    log = TestLog()

    log.step("Go to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit form with first name empty")
    step1.fill_info("", "Xiang", "201318")
    step1.continue_checkout()
    log.detail("First Name: [empty]", "Last Name: Xiang", "Postal: 201318")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.check("Error message mentions 'First Name'",
              "First Name" in error, True)
    log.detail(f"Displayed: \"{error}\"")
    assert "First Name" in error, f"Unexpected error: {error}"

    log.passed("Empty first name correctly rejected with descriptive error")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-003",
    category="Functional / Input Validation",
    priority="P1",
    precondition="Cart contains 1 item. On checkout step one.",
    test_data="First: Gu | Last Name: [empty] | Postal: 201318",
)
def test_checkout_empty_last_name(cart_ready: CartPage, page: Page):
    """Submitting checkout form without last name shows error."""

    log = TestLog()

    log.step("Go to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit form with last name empty")
    step1.fill_info("Gu", "", "201318")
    step1.continue_checkout()
    log.detail("First Name: Gu", "Last Name: [empty]", "Postal: 201318")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.check("Error message mentions 'Last Name'",
              "Last Name" in error, True)
    log.detail(f"Displayed: \"{error}\"")
    assert "Last Name" in error, f"Unexpected error: {error}"

    log.passed("Empty last name correctly rejected with descriptive error")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-004",
    category="Functional / Input Validation",
    priority="P1",
    precondition="Cart contains 1 item. On checkout step one.",
    test_data="First: Gu | Last: Xiang | Postal: [empty]",
)
def test_checkout_empty_postal_code(cart_ready: CartPage, page: Page):
    """Submitting checkout form without postal code shows error."""

    log = TestLog()

    log.step("Go to checkout form")
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    log.step("Submit form with postal code empty")
    step1.fill_info("Gu", "Xiang", "")
    step1.continue_checkout()
    log.detail("First Name: Gu", "Last Name: Xiang", "Postal Code: [empty]")

    log.step("Verify validation error")
    error = step1.get_error_text()
    log.check("Error message mentions 'Postal Code'",
              "Postal Code" in error, True)
    log.detail(f"Displayed: \"{error}\"")
    assert "Postal Code" in error, f"Unexpected error: {error}"

    log.passed("Empty postal code correctly rejected with descriptive error")


# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CHK-005",
    category="Functional / Navigation",
    priority="P2",
    precondition="Cart contains 1 item. On checkout step one.",
    test_data="N/A — no form fill required",
)
def test_checkout_cancel_returns_to_cart(cart_ready: CartPage, page: Page):
    """Clicking Cancel on checkout form returns user to cart page."""

    log = TestLog()

    log.step("Go to checkout form")
    cart_ready.go_to_checkout()

    log.step("Click [Cancel] without filling anything")
    page.locator('[data-test="cancel"]').click()
    log.detail("Clicked [Cancel]")

    log.verify("Navigated back to cart page",
               page.url == CartPage.URL)
    expect(page).to_have_url(CartPage.URL)

    log.passed("Cancel button correctly returns user to cart without changes")
