"""Inventory / product listing tests for SauceDemo."""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def inventory(page: Page) -> InventoryPage:
    """Log in with standard_user and return InventoryPage."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)  # gentle spacing to avoid rate limits
    return InventoryPage(page)


# ── Page load & content ───────────────────────────────────────

@pytest.mark.smoke
def test_inventory_page_loads(inventory: InventoryPage):
    """Inventory page shows products after login."""
    assert inventory.is_loaded()
    assert inventory.get_product_count() == 6, "SauceDemo should have 6 products"


def test_all_products_have_name_and_price(inventory: InventoryPage):
    """Every product has a non-empty name and a price > 0."""
    names = inventory.get_product_names()
    prices = inventory.get_product_prices()

    assert len(names) == 6
    assert len(prices) == 6
    for name in names:
        assert len(name) > 0, "Product name should not be empty"
    for price in prices:
        assert price > 0, f"Price should be > 0, got {price}"


def test_product_images_load(inventory: InventoryPage):
    """Every product has a valid, non-broken image src."""
    images = inventory.product_items.locator("img.inventory_item_img")
    for i in range(images.count()):
        img = images.nth(i)
        img.scroll_into_view_if_needed()
        expect(img).to_be_visible(timeout=10000)
        src = img.get_attribute("src")
        assert src and len(src) > 0, f"Image {i} has empty src"
        assert src.startswith("/static/media/") or src.startswith("http"), \
            f"Image {i} has unexpected src format: {src}"


# ── Sorting ───────────────────────────────────────────────────

@pytest.mark.parametrize("sort_option,first_expected", [
    ("Name (A to Z)", "Sauce Labs Backpack"),
    ("Name (Z to A)", "Test.allTheThings() T-Shirt (Red)"),
    ("Price (low to high)", "Sauce Labs Onesie"),
    ("Price (high to low)", "Sauce Labs Fleece Jacket"),
])
def test_sorting(inventory: InventoryPage, sort_option, first_expected):
    """Sort products and verify the first item matches expectation."""
    inventory.sort_by(sort_option)

    names = inventory.get_product_names()
    assert names[0] == first_expected, \
        f"After '{sort_option}', first item should be '{first_expected}', got '{names[0]}'"


def test_price_sort_is_numerical(inventory: InventoryPage):
    """Price (low to high) should produce non-decreasing prices."""
    inventory.sort_by("Price (low to high)")
    prices = inventory.get_product_prices()
    assert prices == sorted(prices), f"Prices not sorted: {prices}"


# ── Cart badge ────────────────────────────────────────────────

def test_cart_badge_starts_empty(inventory: InventoryPage):
    """Cart badge is hidden when cart is empty."""
    assert inventory.get_cart_count() == 0


def test_cart_badge_updates_after_add(inventory: InventoryPage):
    """Adding items increments the cart badge."""
    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 1

    inventory.add_item_to_cart("Sauce Labs Bike Light")
    assert inventory.get_cart_count() == 2


# ── Add / Remove ──────────────────────────────────────────────

def test_add_and_remove_item(inventory: InventoryPage):
    """After adding then removing an item, cart badge returns to 0."""
    inventory.add_item_to_cart("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 1

    inventory.remove_item("Sauce Labs Backpack")
    assert inventory.get_cart_count() == 0
