"""Cart — SauceDemo shopping cart operations."""

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from qa_report import testcase, TestLog


@pytest.fixture
def cart_with_items(page: Page) -> CartPage:
    """Log in, add 2 items, go to cart."""
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.add_item_to_cart("Sauce Labs Backpack")
    inv.add_item_to_cart("Sauce Labs Onesie")
    inv.go_to_cart()
    return CartPage(page)


# ═══════════════════════════════════════════════════════════════
#  TC-CART-001  ·  Cart shows added items
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CART-001",
    title="Cart page must display all items added from inventory",
    module="Cart",
    feature="Item Management",
    level="System",
    priority="P0",
    tags=["smoke"],
    precondition=[
        "Logged in as standard_user.",
        "2 items added to cart: Sauce Labs Backpack, Sauce Labs Onesie.",
        "On cart page.",
    ],
    test_data={"items": ["Sauce Labs Backpack", "Sauce Labs Onesie"]},
    expected="Cart shows exactly 2 items with correct names.",
)
def test_cart_shows_added_items(cart_with_items: CartPage):
    log = TestLog()

    log.step("Verify cart page is loaded")
    log.check("Cart page is loaded", cart_with_items.is_loaded(), True)
    assert cart_with_items.is_loaded()

    log.step("Verify item count and contents")
    log.check("Item count is 2", cart_with_items.get_item_count(), 2)
    assert cart_with_items.get_item_count() == 2

    names = cart_with_items.get_item_names()
    log.verify("Contains 'Sauce Labs Backpack'",
               actual="Sauce Labs Backpack" in names, expected=True)
    log.verify("Contains 'Sauce Labs Onesie'",
               actual="Sauce Labs Onesie" in names, expected=True)
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Onesie" in names

    log.finish(True, "Cart correctly displays both added items.")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-002  ·  Remove item from cart
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CART-002",
    title="Removing an item from cart must decrement count and remove from list",
    module="Cart",
    feature="Item Management",
    level="System",
    priority="P1",
    precondition=["Cart contains 2 items.", "On cart page."],
    test_data={"remove": "Sauce Labs Backpack"},
    expected="Cart count decreases to 1; removed item no longer listed.",
)
def test_remove_item_from_cart(cart_with_items: CartPage):
    log = TestLog()

    log.step("Confirm initial state")
    log.check("Initial item count", cart_with_items.get_item_count(), 2)
    assert cart_with_items.get_item_count() == 2

    log.step("Remove 'Sauce Labs Backpack' from cart")
    cart_with_items.remove_item("Sauce Labs Backpack")
    log.action("Clicked [Remove] on 'Sauce Labs Backpack'")

    log.step("Verify cart state after removal")
    log.check("Item count decreased to 1", cart_with_items.get_item_count(), 1)
    assert cart_with_items.get_item_count() == 1
    log.verify("Removed item no longer in list",
               actual="Sauce Labs Backpack" not in cart_with_items.get_item_names(),
               expected=True)

    log.finish(True, "Item removed correctly; cart state updated.")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-003  ·  Cart persists across navigation
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CART-003",
    title="Cart badge count must survive navigation away from and back to inventory",
    module="Cart",
    feature="State Persistence",
    level="System",
    priority="P1",
    precondition=["Logged in as standard_user.", "No items in cart."],
    test_data={"add": "Sauce Labs Backpack"},
    expected="Badge shows '1' before and after navigating to cart and back.",
)
def test_cart_persists_after_navigation(page: Page):
    log = TestLog()

    log.step("Log in and add an item")
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.add_item_to_cart("Sauce Labs Backpack")
    log.action("Added 'Sauce Labs Backpack'")
    log.check("Cart badge = 1", inv.get_cart_count(), 1)
    assert inv.get_cart_count() == 1

    log.step("Navigate to cart then back to inventory")
    inv.go_to_cart()
    cart = CartPage(page)
    cart.continue_shopping.click()
    log.action("Cart → Continue Shopping → back to inventory")

    log.step("Verify badge still shows 1")
    log.check("Cart badge still = 1", inv.get_cart_count(), 1)
    assert inv.get_cart_count() == 1

    log.finish(True, "Cart state persisted across navigation.")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-004  ·  Empty cart
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CART-004",
    title="Navigating to cart without adding items should show an empty cart",
    module="Cart",
    feature="State — Empty",
    level="System",
    priority="P1",
    precondition=["Logged in as standard_user.", "No items in cart."],
    test_data=None,
    expected="Cart item count = 0.",
)
def test_cart_empty_by_default(page: Page):
    log = TestLog()

    log.step("Log in without adding anything")
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.go_to_cart()
    log.action("Directly navigated to cart page")

    log.step("Verify cart is empty")
    cart = CartPage(page)
    log.check("Item count is 0", cart.get_item_count(), 0)
    assert cart.get_item_count() == 0

    log.finish(True, "Cart is empty when no items have been added.")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-005  ·  Checkout button available
# ═══════════════════════════════════════════════════════════════

@testcase(
    id="TC-CART-005",
    title="Checkout button must be visible and enabled when cart has items",
    module="Cart",
    feature="Navigation",
    level="System",
    priority="P1",
    precondition=["Cart contains 2 items.", "On cart page."],
    test_data=None,
    expected="[Checkout] button is visible and enabled.",
)
def test_checkout_button_exists(cart_with_items: CartPage):
    log = TestLog()

    log.step("Verify checkout button state")
    log.check("Checkout button is visible",
              cart_with_items.checkout_button.is_visible(), True)
    log.check("Checkout button is enabled",
              cart_with_items.checkout_button.is_enabled(), True)
    assert cart_with_items.checkout_button.is_visible()
    assert cart_with_items.checkout_button.is_enabled()

    log.finish(True, "Checkout button is ready for user interaction.")
