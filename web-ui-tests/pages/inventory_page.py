"""Inventory / Products page object for SauceDemo."""

from playwright.sync_api import Page, Locator, expect


class InventoryPage:
    """Page object for the inventory/products listing page."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".header_secondary_container .title")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.product_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.burger_menu = page.locator("#react-burger-menu-btn")

    def goto(self) -> None:
        self.page.goto(self.URL)

    def get_product_count(self) -> int:
        """Return the number of displayed product items."""
        return self.product_items.count()

    def get_product_names(self) -> list[str]:
        """Return all product names currently displayed."""
        return self.product_items.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self) -> list[float]:
        """Return all product prices as floats."""
        price_texts = self.product_items.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in price_texts]

    def add_item_to_cart(self, product_name: str) -> None:
        """Click 'Add to cart' for the given product by name."""
        self.product_items.filter(has_text=product_name) \
            .locator('button:text("Add to cart")').click()

    def remove_item(self, product_name: str) -> None:
        """Click 'Remove' for the given product by name."""
        self.product_items.filter(has_text=product_name) \
            .locator('button:text("Remove")').click()

    def get_cart_count(self) -> int:
        """Return the cart badge count. Returns 0 if badge not visible."""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content() or "0")
        return 0

    def sort_by(self, option: str) -> None:
        """Select a sort option. e.g. 'Name (A to Z)', 'Price (low to high)'."""
        self.sort_dropdown.select_option(option)

    def go_to_cart(self) -> None:
        """Navigate to the cart page."""
        self.cart_link.click()

    def is_loaded(self) -> bool:
        """Check if the inventory page has loaded."""
        return self.title.is_visible() and self.title.text_content() == "Products"
