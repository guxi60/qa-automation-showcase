"""Checkout page objects for SauceDemo — Selenium edition.

Covers three sub-pages:
- CheckoutStepOnePage: Your Information form
- CheckoutStepTwoPage: Order overview / confirmation
- CheckoutCompletePage: Thank you / complete
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CheckoutStepOnePage:
    """Checkout: Your Information form."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ── locators ────────────────────────────────────────────────

    @property
    def first_name(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="firstName"]')

    @property
    def last_name(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="lastName"]')

    @property
    def postal_code(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="postalCode"]')

    @property
    def continue_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="continue"]')

    @property
    def cancel_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="cancel"]')

    @property
    def error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')

    # ── actions ─────────────────────────────────────────────────

    def fill_info(self, first: str, last: str, postal: str) -> None:
        """Fill in all checkout fields."""
        self.first_name.clear()
        self.first_name.send_keys(first)
        self.last_name.clear()
        self.last_name.send_keys(last)
        self.postal_code.clear()
        self.postal_code.send_keys(postal)

    def continue_checkout(self) -> None:
        """Click Continue. Does NOT wait — caller should wait based on context."""
        self.continue_button.click()

    def get_error_text(self) -> str:
        """Return error text, or empty string if none visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test="error"]')))
            return self.error_message.text.strip()
        except TimeoutException:
            return ""

    def is_error_visible(self) -> bool:
        try:
            return self.error_message.is_displayed()
        except Exception:
            return False


class CheckoutStepTwoPage:
    """Checkout: Overview / confirmation page."""

    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @property
    def cart_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".cart_item")

    @property
    def finish_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="finish"]')

    @property
    def cancel_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="cancel"]')

    @property
    def total_label(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".summary_total_label")

    def get_item_count(self) -> int:
        return len(self.cart_items)

    def get_total_text(self) -> str:
        return self.total_label.text.strip()

    def finish(self) -> None:
        """Click Finish and wait for complete page."""
        self.finish_button.click()
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.complete-header')))


class CheckoutCompletePage:
    """Checkout: Complete / Thank You page."""

    URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @property
    def header(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".complete-header")

    @property
    def back_home_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="back-to-products"]')

    def get_header_text(self) -> str:
        return self.header.text.strip()

    def back_home(self) -> None:
        self.back_home_button.click()
