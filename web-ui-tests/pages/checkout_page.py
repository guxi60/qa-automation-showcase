"""Checkout page objects for SauceDemo — step one, step two, and complete."""

from playwright.sync_api import Page


class CheckoutStepOnePage:
    """Checkout: Your Information form."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.error_message = page.locator('[data-test="error"]')

    def fill_info(self, first: str, last: str, postal: str) -> None:
        """Fill in all checkout fields."""
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_checkout(self) -> None:
        self.continue_button.click()

    def get_error_text(self) -> str:
        self.error_message.wait_for(state="visible", timeout=3000)
        return self.error_message.text_content() or ""

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()


class CheckoutStepTwoPage:
    """Checkout: Overview / confirmation page."""

    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.finish_button = page.locator('[data-test="finish"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.total_label = page.locator(".summary_total_label")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_total_text(self) -> str:
        return self.total_label.text_content() or ""

    def finish(self) -> None:
        self.finish_button.click()


class CheckoutCompletePage:
    """Checkout: Complete / Thank You page."""

    URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator(".complete-header")
        self.back_home_button = page.locator('[data-test="back-to-products"]')

    def get_header_text(self) -> str:
        return self.header.text_content() or ""

    def back_home(self) -> None:
        self.back_home_button.click()
