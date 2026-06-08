"""Checkout flow tests for SauceDemo — E2E and error scenarios."""

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


@pytest.fixture
def cart_ready(page: Page) -> CartPage:
    """Log in, add 1 item, go to cart."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.go_to_cart()
    return CartPage(page)


# ── E2E happy path ────────────────────────────────────────────

@pytest.mark.smoke
def test_complete_checkout_e2e(cart_ready: CartPage, page: Page):
    """Full end-to-end checkout: login → add → cart → fill info → overview → finish."""
    cart_ready.go_to_checkout()

    # Step 1: fill info
    step1 = CheckoutStepOnePage(page)
    step1.fill_info("Gu", "Xiang", "201318")
    step1.continue_checkout()

    # Step 2: overview
    step2 = CheckoutStepTwoPage(page)
    expect(page).to_have_url(CheckoutStepTwoPage.URL)
    assert step2.get_item_count() == 1
    assert "Total" in step2.get_total_text()
    print(f"✓ Checkout overview: 1 item, {step2.get_total_text()}")
    step2.finish()

    # Complete
    complete = CheckoutCompletePage(page)
    expect(page).to_have_url(CheckoutCompletePage.URL)
    assert "Thank you" in complete.get_header_text()
    print(f"✓ Order complete: {complete.get_header_text()}")

    # Back home works
    complete.back_home()
    expect(page).to_have_url(InventoryPage.URL)


# ── Checkout form validation ──────────────────────────────────

def test_checkout_empty_first_name(cart_ready: CartPage, page: Page):
    """Error shown when first name is missing."""
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)
    step1.fill_info("", "Xiang", "201318")
    step1.continue_checkout()

    error = step1.get_error_text()
    assert "First Name" in error, f"Unexpected error: {error}"


def test_checkout_empty_last_name(cart_ready: CartPage, page: Page):
    """Error shown when last name is missing."""
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)
    step1.fill_info("Gu", "", "201318")
    step1.continue_checkout()

    error = step1.get_error_text()
    assert "Last Name" in error, f"Unexpected error: {error}"


def test_checkout_empty_postal_code(cart_ready: CartPage, page: Page):
    """Error shown when postal code is missing."""
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)
    step1.fill_info("Gu", "Xiang", "")
    step1.continue_checkout()

    error = step1.get_error_text()
    assert "Postal Code" in error, f"Unexpected error: {error}"


def test_checkout_cancel_returns_to_cart(cart_ready: CartPage, page: Page):
    """Cancel on step one returns to cart page."""
    cart_ready.go_to_checkout()
    step1 = CheckoutStepOnePage(page)
    step1.cancel_button.click()

    expect(page).to_have_url(CartPage.URL)
