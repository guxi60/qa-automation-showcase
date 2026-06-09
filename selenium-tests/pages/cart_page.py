"""Cart page object for SauceDemo — Selenium edition."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Page object for the shopping cart page."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ── locators (lazy) ─────────────────────────────────────────

    @property
    def cart_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".cart_item")

    @property
    def checkout_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="checkout"]')

    @property
    def continue_shopping(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="continue-shopping"]')

    # ── actions ─────────────────────────────────────────────────

    def goto(self) -> None:
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-test="checkout"]')))

    def get_item_count(self) -> int:
        """Return number of items in cart."""
        return len(self.cart_items)

    def get_item_names(self) -> list[str]:
        """Return the names of items in cart."""
        return [item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text.strip()
                for item in self.cart_items]

    def remove_item(self, product_name: str) -> None:
        """Remove a specific item from cart by name.

        Uses a fresh XPath lookup every time — avoids stale element
        references when the DOM mutates after removal.
        """
        btn = self.driver.find_element(
            By.XPATH,
            f"//div[@class='cart_item' and contains(.,'{product_name}')]//button"
        )
        btn.click()

    def go_to_checkout(self) -> None:
        """Click the checkout button and wait for the form."""
        self.checkout_button.click()
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-test="firstName"]')))

    def is_loaded(self) -> bool:
        """Check if cart page is loaded."""
        return self.checkout_button.is_displayed()
