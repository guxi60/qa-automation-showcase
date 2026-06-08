"""Cart page object for SauceDemo."""

from playwright.sync_api import Page, Locator


class CartPage:
    """Page object for the shopping cart page."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping = page.locator('[data-test="continue-shopping"]')

    def goto(self) -> None:
        self.page.goto(self.URL)

    def get_item_count(self) -> int:
        """Return number of items in cart."""
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        """Return the names of items in cart."""
        return self.cart_items.locator(".inventory_item_name").all_text_contents()

    def remove_item(self, product_name: str) -> None:
        """Remove a specific item from cart by name."""
        self.cart_items.filter(has_text=product_name) \
            .locator('button:text("Remove")').click()

    def go_to_checkout(self) -> None:
        """Click the checkout button."""
        self.checkout_button.click()

    def is_loaded(self) -> bool:
        """Check if cart page is loaded."""
        return self.checkout_button.is_visible()
