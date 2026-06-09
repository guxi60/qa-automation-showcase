"""Cart tests — Selenium edition, Allure-native, DDT-driven."""

import allure
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from qa_report import load_data, set_meta, step, action, note


def _go_to_cart_with(driver, items: list[str]) -> CartPage:
    """Log in, clean cart, add each item from *items*, navigate to cart."""
    login = LoginPage(driver)
    login.goto()
    login.login("standard_user", "secret_sauce")
    inv = InventoryPage(driver)
    inv.remove_all_items()   # reset cart from any previous test
    for item in items:
        inv.add_item_to_cart(item)
    inv.go_to_cart()
    return CartPage(driver)


# ═══════════════════════════════════════════════════════════════

@allure.feature("Cart")
@pytest.mark.parametrize("tc", [
    t for t in load_data("cart.json")["cart"]
    if t["id"] != "TC-CART-003"  # persistence handled separately
])
def test_cart(driver, tc: dict):
    """DDT-driven cart tests: display, removal, empty, button."""
    set_meta(tc)

    add_items: list[str] = tc.get("add_items", [])
    remove_item: str = tc.get("remove_item", "")
    single_add: str = tc.get("add_item", "")

    if single_add:
        add_items = [single_add]

    with step("Log in and add items to cart"):
        cart = _go_to_cart_with(driver, add_items)
    action(f"Cart contains {cart.get_item_count()} item(s)")

    if remove_item:
        with step(f"Remove {remove_item!r} from cart"):
            before = cart.get_item_count()
            cart.remove_item(remove_item)
        action(f"Clicked [Remove] — count {before} → {cart.get_item_count()}")
        assert cart.get_item_count() == before - 1
        assert remove_item not in cart.get_item_names()

    elif add_items:
        with step("Verify cart contents"):
            assert cart.is_loaded()
            assert cart.get_item_count() == len(add_items)
            names = cart.get_item_names()
            for item in add_items:
                assert item in names, f"{item!r} not found in cart"
            for i, name in enumerate(names, 1):
                note(f"[{i}] {name}")

    else:
        with step("Verify empty cart state"):
            assert cart.get_item_count() == 0
            note("Cart is empty — no items added")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-003 — State persistence (needs its own flow)
# ═══════════════════════════════════════════════════════════════

@allure.feature("Cart")
def test_cart_persists_after_navigation(driver):
    """Cart badge survives navigating to cart and back."""
    tc_data = load_data("cart.json")["cart"]
    tc = next(t for t in tc_data if t["id"] == "TC-CART-003")
    set_meta(tc)

    item = tc["add_item"]

    with step("Log in and add item to cart"):
        login = LoginPage(driver)
        login.goto()
        login.login("standard_user", "secret_sauce")
        inv = InventoryPage(driver)
        inv.add_item_to_cart(item)
    action(f"Added {item!r}")

    with step("Verify badge = 1 on inventory page"):
        assert inv.get_cart_count() == 1
    note("Badge shows '1'")

    with step("Navigate to cart, then back to inventory"):
        inv.go_to_cart()
        CartPage(driver).continue_shopping.click()
    action("Cart → Continue Shopping → back to inventory")

    with step("Verify badge still = 1"):
        assert "inventory" in driver.current_url, (
            f"Not on inventory page: {driver.current_url}"
        )
        inv2 = InventoryPage(driver)
        assert inv2.get_cart_count() == 1
    note("Cart badge persisted across navigation")


# ═══════════════════════════════════════════════════════════════
#  TC-CART-005 — Checkout button
# ═══════════════════════════════════════════════════════════════

@allure.feature("Cart")
def test_checkout_button_exists(driver):
    """Checkout button is visible and enabled when cart has items."""
    tc_data = load_data("cart.json")["cart"]
    tc = next(t for t in tc_data if t["id"] == "TC-CART-005")
    set_meta(tc)

    with step("Add items and go to cart"):
        cart = _go_to_cart_with(driver, tc.get("add_items", []))

    with step("Verify checkout button state"):
        assert cart.checkout_button.is_displayed()
        assert cart.checkout_button.is_enabled()
    action("Checkout button is ready")
