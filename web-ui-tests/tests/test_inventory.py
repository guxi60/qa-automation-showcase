"""Inventory — SauceDemo product listing and sorting."""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from qa_report import testcase, TestLog


@pytest.fixture
def inventory(page: Page) -> InventoryPage:
    """Log in and return an InventoryPage object."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    page.wait_for_load_state("networkidle")
    return InventoryPage(page)


# ═══════════════════════════════════════════════════════════════
#  TC-INV-001  ·  Inventory page loads
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-001",
    title="Inventory page must display exactly 6 products after login",
    module="Inventory",
    feature="Product Display",
    level="System",
    priority="P0",
    tags=["smoke"],
    precondition=["Logged in as standard_user.", "On inventory page."],
    test_data=None,
    expected=(
        "Page heading = 'Products'. 6 items listed. "
        "Names: Sauce Labs Backpack, Sauce Labs Bike Light, "
        "Sauce Labs Bolt T-Shirt, Sauce Labs Fleece Jacket, "
        "Sauce Labs Onesie, Test.allTheThings() T-Shirt (Red)."
    ),
)
def test_inventory_page_loads(inventory: InventoryPage):
    log = TestLog()

    log.step("Verify page heading")
    log.check("Page is loaded (title visible)", inventory.is_loaded(), True)
    assert inventory.is_loaded()

    log.step("Verify product count")
    count = inventory.get_product_count()
    log.check("Product count = 6", count, 6)
    assert count == 6

    log.step("List all products")
    names = inventory.get_product_names()
    for i, name in enumerate(names, 1):
        log.note(f"  [{i}] {name}")

    log.finish(True, f"Inventory loaded with {count} products.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-002  ·  Each product has name and price
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-002",
    title="Every product tile must show a non-empty name and a price greater than zero",
    module="Inventory",
    feature="Product Display",
    level="System",
    priority="P1",
    precondition=["Logged in as standard_user.", "On inventory page."],
    test_data=None,
    expected="6 product names (non-empty) and 6 prices (> $0.00).",
)
def test_all_products_have_name_and_price(inventory: InventoryPage):
    log = TestLog()

    log.step("Collect names and prices")
    names = inventory.get_product_names()
    prices = inventory.get_product_prices()
    log.check("6 names collected", len(names), 6)
    log.check("6 prices collected", len(prices), 6)
    assert len(names) == 6
    assert len(prices) == 6

    log.step("Validate each product")
    all_ok = True
    for i, (name, price) in enumerate(zip(names, prices), 1):
        name_ok = len(name) > 0
        price_ok = price > 0
        if not name_ok or not price_ok:
            all_ok = False
        status = "✓" if (name_ok and price_ok) else "✗"
        log.note(f"  [{i}] {status} {name!r} — ${price:.2f}")
        assert name_ok, f"Product {i} name is empty"
        assert price_ok, f"Product {i} price is not > 0: {price}"

    log.verify("All 6 products have valid name + price", all_ok)
    log.finish(True, "All products have valid names and prices.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-003  ·  Product images
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-003",
    title="Every product tile must display a visible image with a valid src",
    module="Inventory",
    feature="Product Display",
    level="System",
    priority="P1",
    tags=["gui"],
    precondition=["Logged in.", "On inventory page."],
    test_data=None,
    expected="6 visible images, each src starts with '/static/media/' or 'http'.",
)
def test_product_images_load(inventory: InventoryPage):
    log = TestLog()

    log.step("Inspect each product image")
    images = inventory.product_items.locator("img.inventory_item_img")
    log.check("Image count", images.count(), 6)

    all_ok = True
    for i in range(images.count()):
        img = images.nth(i)
        img.scroll_into_view_if_needed()
        try:
            expect(img).to_be_visible(timeout=10000)
        except Exception:
            all_ok = False
            log.note(f"  ✗ Image {i} is not visible")

        src = img.get_attribute("src") or ""
        valid = src.startswith("/static/media/") or src.startswith("http")
        if not valid:
            all_ok = False
        mark = "✓" if valid else "✗"
        log.note(f"  [{i}] {mark} src={src[:70]}...")
        assert src, f"Image {i} has empty src"
        assert valid, f"Image {i} src format unexpected: {src}"

    log.verify("All images visible with valid src", all_ok)
    log.finish(True, "All product images load correctly.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-004..007  ·  Sorting (parametrized)
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-004",
    title="Product sorting must correctly reorder the first item for each sort criterion",
    module="Inventory",
    feature="Sorting",
    level="System",
    priority="P1",
    precondition=["Logged in.", "On inventory page."],
    test_data={"sort_options": [
        "Name (A to Z)", "Name (Z to A)",
        "Price (low to high)", "Price (high to low)",
    ]},
    expected="First item after sort matches known reference values for each option.",
)
@pytest.mark.parametrize("sort_option,first_expected", [
    ("Name (A to Z)",        "Sauce Labs Backpack"),
    ("Name (Z to A)",        "Test.allTheThings() T-Shirt (Red)"),
    ("Price (low to high)",  "Sauce Labs Onesie"),
    ("Price (high to low)",  "Sauce Labs Fleece Jacket"),
])
def test_sorting(inventory: InventoryPage, sort_option, first_expected):
    log = TestLog()

    log.step(f"Apply sort: '{sort_option}'")
    inventory.sort_by(sort_option)
    log.action(f"Selected '{sort_option}' from sort dropdown")

    log.step("Verify first item matches expectation")
    names = inventory.get_product_names()
    log.verify(f"First item = {first_expected!r}",
               actual=names[0], expected=first_expected)
    assert names[0] == first_expected

    log.finish(True, f"Sort '{sort_option}' returned correct first item.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-008  ·  Price sort is numerical
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-008",
    title="Price (low to high) sort must produce a non-decreasing price sequence",
    module="Inventory",
    feature="Sorting",
    level="System",
    priority="P1",
    precondition=["Logged in.", "On inventory page."],
    test_data={"sort": "Price (low to high)"},
    expected="Prices are sorted in ascending numerical order (not lexicographic).",
)
def test_price_sort_is_numerical(inventory: InventoryPage):
    log = TestLog()

    log.step("Sort by Price (low to high)")
    inventory.sort_by("Price (low to high)")
    prices = inventory.get_product_prices()

    log.step("Verify price ordering")
    expected_sorted = sorted(prices)
    for i, (actual, exp) in enumerate(zip(prices, expected_sorted)):
        log.note(f"  [{i}] ${actual:.2f}")

    log.verify("Prices are in non-decreasing order",
               actual=prices, expected=expected_sorted)
    assert prices == expected_sorted

    log.finish(True, "Price sorting is numerically correct.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-009  ·  Cart badge starts empty
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-009",
    title="Cart badge must be hidden when no items have been added",
    module="Cart",
    feature="Badge Indicator",
    level="System",
    priority="P1",
    precondition=["Logged in.", "No items added."],
    test_data=None,
    expected="get_cart_count() returns 0 (badge not visible).",
)
def test_cart_badge_starts_empty(inventory: InventoryPage):
    log = TestLog()

    log.step("Check cart badge state on inventory page")
    log.check("Cart badge count = 0", inventory.get_cart_count(), 0)
    assert inventory.get_cart_count() == 0

    log.finish(True, "Cart badge correctly hidden when cart is empty.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-010  ·  Cart badge increments
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-010",
    title="Cart badge must increment as items are added",
    module="Cart",
    feature="Badge Indicator",
    level="System",
    priority="P1",
    precondition=["Logged in.", "On inventory page."],
    test_data={"add": ["Sauce Labs Backpack", "Sauce Labs Bike Light"]},
    expected="Badge shows 1 after first add, 2 after second add.",
)
def test_cart_badge_updates_after_add(inventory: InventoryPage):
    log = TestLog()

    log.step("Add first item")
    inventory.add_item_to_cart("Sauce Labs Backpack")
    log.action("Added 'Sauce Labs Backpack'")
    log.check("Badge = 1", inventory.get_cart_count(), 1)
    assert inventory.get_cart_count() == 1

    log.step("Add second item")
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    log.action("Added 'Sauce Labs Bike Light'")
    log.check("Badge = 2", inventory.get_cart_count(), 2)
    assert inventory.get_cart_count() == 2

    log.finish(True, "Cart badge correctly increments with each addition.")


# ═══════════════════════════════════════════════════════════════
#  TC-INV-011  ·  Add-then-remove
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-INV-011",
    title="Adding then removing the same item must return cart count to zero",
    module="Cart",
    feature="Badge Indicator",
    level="System",
    priority="P2",
    precondition=["Logged in.", "On inventory page."],
    test_data={"add_then_remove": "Sauce Labs Backpack"},
    expected="Badge: 0 → 1 → 0.",
)
def test_add_and_remove_item(inventory: InventoryPage):
    log = TestLog()

    log.step("Add item")
    inventory.add_item_to_cart("Sauce Labs Backpack")
    log.check("Badge = 1", inventory.get_cart_count(), 1)
    assert inventory.get_cart_count() == 1

    log.step("Remove the same item")
    inventory.remove_item("Sauce Labs Backpack")
    log.action("Clicked [Remove] on 'Sauce Labs Backpack'")
    log.check("Badge = 0", inventory.get_cart_count(), 0)
    assert inventory.get_cart_count() == 0

    log.finish(True, "Add-then-remove returns cart to empty state.")
