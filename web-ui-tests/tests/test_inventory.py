"""Inventory tests — Allure-native, DDT-driven."""

import allure
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import load_data, set_meta, step, action, note


@pytest.fixture
def inventory(page: Page) -> InventoryPage:
    """Log in and return InventoryPage."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    page.wait_for_load_state("networkidle")
    return InventoryPage(page)


# ═══════════════════════════════════════════════════════════════
#  Display
# ═══════════════════════════════════════════════════════════════

@allure.feature("Inventory")
@pytest.mark.parametrize("tc", load_data("inventory.json")["display"])
def test_inventory_display(inventory: InventoryPage, tc: dict):
    """TC-INV-001..003 — Product listing, data integrity, images."""
    set_meta(tc)

    with step("Verify page is loaded"):
        assert inventory.is_loaded()

    if tc.get("expected_count"):
        with step(f"Verify product count = {tc['expected_count']}"):
            assert inventory.get_product_count() == tc["expected_count"]

        with step("List all product names"):
            for i, name in enumerate(inventory.get_product_names(), 1):
                note(f"[{i}] {name}")

    if tc.get("id") == "TC-INV-002":
        with step("Verify each product has valid name and price"):
            names = inventory.get_product_names()
            prices = inventory.get_product_prices()
            for i, (name, price) in enumerate(zip(names, prices), 1):
                assert len(name) > 0, f"Product {i} name is empty"
                assert price > 0, f"Product {i} price is {price} (must be > 0)"
                note(f"[{i}] {name!r} — ${price:.2f}  ✓")

    if tc.get("id") == "TC-INV-003":
        with step("Verify each product image has valid src"):
            images = inventory.product_items.locator("img.inventory_item_img")
            for i in range(images.count()):
                img = images.nth(i)
                img.scroll_into_view_if_needed()
                expect(img).to_be_visible(timeout=10000)
                src = img.get_attribute("src") or ""
                assert src.startswith(("/static/media/", "http")), f"Bad src: {src}"
                note(f"[{i}] ✓ {src[:70]}")


# ═══════════════════════════════════════════════════════════════
#  Sorting
# ═══════════════════════════════════════════════════════════════

@allure.feature("Inventory")
def test_sort_order(inventory: InventoryPage):
    """TC-INV-004 — Each sort criterion returns correct first item."""
    tc_data = load_data("inventory.json")["sorting"][0]
    set_meta(tc_data)

    for scenario in tc_data["scenarios"]:
        sort_opt = scenario["sort"]
        expected_first = scenario["first"]
        with step(f"Sort by {sort_opt!r} → expect first={expected_first!r}"):
            inventory.sort_by(sort_opt)
            actual_first = inventory.get_product_names()[0]
            assert actual_first == expected_first, (
                f"Sort {sort_opt!r}: expected {expected_first!r}, got {actual_first!r}"
            )
        action(f"First item: {actual_first!r}  ✓")


@allure.feature("Inventory")
def test_price_sort_is_numerical(inventory: InventoryPage):
    """TC-INV-005 — Price (low to high) is numerically correct."""
    tc = load_data("inventory.json")["sorting"][1]
    set_meta(tc)

    with step(f"Sort by {tc['sort']!r}"):
        inventory.sort_by(tc["sort"])

    with step("Verify prices are in non-decreasing order"):
        prices = inventory.get_product_prices()
        for i, price in enumerate(prices):
            note(f"[{i}] ${price:.2f}")
        assert prices == sorted(prices), f"Not sorted: {prices}"


# ═══════════════════════════════════════════════════════════════
#  Cart badge lifecycle
# ═══════════════════════════════════════════════════════════════

@allure.feature("Inventory")
def test_cart_badge_starts_empty(inventory: InventoryPage):
    """TC-INV-006 — Badge is hidden when cart is empty."""
    tc = load_data("inventory.json")["cart_badge"][0]
    set_meta(tc)

    with step("Check badge on fresh inventory page"):
        assert inventory.get_cart_count() == 0
    action("Cart badge is not displayed")


@allure.feature("Inventory")
def test_cart_badge_increments(inventory: InventoryPage):
    """TC-INV-007 — Badge increments with each item added."""
    tc = load_data("inventory.json")["cart_badge"][1]
    set_meta(tc)

    items = tc["add_items"]
    for i, item in enumerate(items, 1):
        with step(f"Add {item!r} (expect badge = {i})"):
            inventory.add_item_to_cart(item)
            assert inventory.get_cart_count() == i
        action(f"Added {item!r} — badge now {i}")


@allure.feature("Inventory")
def test_add_then_remove_resets_cart(inventory: InventoryPage):
    """TC-INV-008 — Add → Remove returns badge to zero."""
    tc = load_data("inventory.json")["cart_badge"][2]
    set_meta(tc)

    item = tc["add_remove"]
    with step(f"Add {item!r}"):
        inventory.add_item_to_cart(item)
        assert inventory.get_cart_count() == 1

    with step(f"Remove {item!r}"):
        inventory.remove_item(item)
    action("Clicked [Remove]")

    with step("Verify badge returns to 0"):
        assert inventory.get_cart_count() == 0
