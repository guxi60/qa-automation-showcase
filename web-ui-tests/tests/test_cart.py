"""Shopping cart tests for SauceDemo."""

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture
def cart_with_items(page: Page) -> CartPage:
    """Log in, add 2 items, go to cart → return CartPage."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.add_item_to_cart("Sauce Labs Onesie")
    inventory.go_to_cart()

    return CartPage(page)


def test_cart_shows_added_items(cart_with_items: CartPage):
    """Cart page displays the 2 items added."""
    assert cart_with_items.is_loaded()
    assert cart_with_items.get_item_count() == 2

    names = cart_with_items.get_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Onesie" in names


def test_remove_item_from_cart(cart_with_items: CartPage):
    """Removing an item from cart reduces count and removes it from list."""
    assert cart_with_items.get_item_count() == 2

    cart_with_items.remove_item("Sauce Labs Backpack")
    assert cart_with_items.get_item_count() == 1
    assert "Sauce Labs Backpack" not in cart_with_items.get_item_names()


def test_cart_persists_after_navigation(page: Page):
    """Cart contents survive page navigation (back to inventory)."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 1

    # Navigate to cart, then back to inventory
    inventory.go_to_cart()
    cart = CartPage(page)
    cart.continue_shopping.click()

    assert inventory.is_loaded()
    assert inventory.get_cart_count() == 1, "Cart count should persist"


def test_cart_empty_by_default(page: Page):
    """Going to cart without adding anything shows 0 items."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.go_to_cart()

    cart = CartPage(page)
    assert cart.get_item_count() == 0


def test_checkout_button_exists(cart_with_items: CartPage):
    """Checkout button is visible when cart has items."""
    assert cart_with_items.checkout_button.is_visible()
    assert cart_with_items.checkout_button.is_enabled()
