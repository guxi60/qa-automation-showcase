"""Checkout tests — Allure-native, DDT-driven."""

import allure
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
from qa_report import load_data, set_meta, step, action, note


@pytest.fixture
def cart_ready(page: Page) -> CartPage:
    """Log in, add 1 item, go to cart."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.add_item_to_cart("Sauce Labs Backpack")
    inv.go_to_cart()
    return CartPage(page)


# ═══════════════════════════════════════════════════════════════
#  E2E happy path
# ═══════════════════════════════════════════════════════════════

@allure.feature("Checkout")
def test_complete_checkout_e2e(cart_ready: CartPage, page: Page):
    """TC-CHK-001 — Full purchase flow."""
    tc = load_data("checkout.yaml")["checkout"][0]
    set_meta(tc)

    with step("Proceed from cart to checkout form"):
        cart_ready.go_to_checkout()
    action("Clicked [Checkout] on cart page")

    with step("Fill shipping information"):
        step1 = CheckoutStepOnePage(page)
        step1.fill_info(tc["first_name"], tc["last_name"], tc["postal_code"])
        action(
            f"First Name: {tc['first_name']}",
            f"Last Name:  {tc['last_name']}",
            f"Postal:     {tc['postal_code']}",
        )
        step1.continue_checkout()
    action("Clicked [Continue]")

    with step("Review order overview"):
        expect(page).to_have_url(CheckoutStepTwoPage.URL)
        step2 = CheckoutStepTwoPage(page)
        assert step2.get_item_count() == 1
        total = step2.get_total_text()
        assert "Total" in total
        note(f"Order total: {total}")

    with step("Place the order"):
        step2.finish()
    action("Clicked [Finish]")

    with step("Verify order confirmation"):
        expect(page).to_have_url(CheckoutCompletePage.URL)
        complete = CheckoutCompletePage(page)
        header = complete.get_header_text()
        assert "Thank you" in header
        note(f"Message: {header!r}")

    with step("Return to products"):
        complete.back_home()
    action("Clicked [Back Home]")
    expect(page).to_have_url(InventoryPage.URL)


# ═══════════════════════════════════════════════════════════════
#  Form validation (parametrized — 3 negative cases)
# ═══════════════════════════════════════════════════════════════

@allure.feature("Checkout")
@pytest.mark.parametrize("tc", load_data("checkout.yaml")["validation"])
def test_checkout_form_validation(cart_ready: CartPage, page: Page, tc: dict):
    """TC-CHK-002..004 — Empty field rejection."""
    set_meta(tc)

    with step("Navigate to checkout form"):
        cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)

    with step(f"Submit form  |  first={tc['first_name']!r}  last={tc['last_name']!r}  postal={tc['postal_code']!r}"):
        step1.fill_info(tc["first_name"], tc["last_name"], tc["postal_code"])
        step1.continue_checkout()

    with step(f"Verify error contains {tc['expected_error']!r}"):
        error = step1.get_error_text()
        assert tc["expected_error"] in error, (
            f"Expected error containing {tc['expected_error']!r}, got {error!r}"
        )
    note(f"Displayed: {error!r}")


# ═══════════════════════════════════════════════════════════════
#  Navigation — cancel
# ═══════════════════════════════════════════════════════════════

@allure.feature("Checkout")
def test_checkout_cancel_returns_to_cart(cart_ready: CartPage, page: Page):
    """TC-CHK-005 — Cancel returns to cart without side effects."""
    tc = load_data("checkout.yaml")["navigation"][0]
    set_meta(tc)

    with step("Navigate to checkout form"):
        cart_ready.go_to_checkout()

    with step("Click [Cancel] without filling the form"):
        page.locator('[data-test="cancel"]').click()
    action("Clicked [Cancel]")

    with step("Verify return to cart page"):
        expect(page).to_have_url(CartPage.URL)
