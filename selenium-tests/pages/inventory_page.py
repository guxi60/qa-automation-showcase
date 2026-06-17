"""Inventory / Products page object for SauceDemo — Selenium edition."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def _js_click(driver, element) -> None:
    """Click via JavaScript — reliable on Linux headless WebDriver."""
    driver.execute_script("arguments[0].click();", element)


class InventoryPage:
    """Page object for the inventory/products listing page."""

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ── locators (lazy — re-queried each access) ────────────────

    @property
    def title(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".header_secondary_container .title")

    @property
    def sort_dropdown(self):
        return Select(self.driver.find_element(
            By.CSS_SELECTOR, '[data-test="product-sort-container"]'))

    @property
    def product_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item")

    @property
    def cart_badge(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge")

    @property
    def cart_link(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link")

    # ── actions ─────────────────────────────────────────────────

    def goto(self) -> None:
        self.driver.get(self.URL)

    def get_product_count(self) -> int:
        """Return the number of displayed product items."""
        return len(self.product_items)

    def get_product_names(self) -> list[str]:
        """Return all product names currently displayed."""
        return [item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text.strip()
                for item in self.product_items]

    def get_product_prices(self) -> list[float]:
        """Return all product prices as floats."""
        prices = []
        for item in self.product_items:
            text = item.find_element(By.CSS_SELECTOR, ".inventory_item_price").text
            prices.append(float(text.replace("$", "")))
        return prices

    def add_item_to_cart(self, product_name: str) -> None:
        """Click 'Add to cart' for the given product by name.

        Uses a fresh XPath lookup every time — avoids stale element
        references that occur when iterating cached find_elements results.
        Button text is intentionally not checked — the same method may need
        to click either 'Add to cart' or 'Remove' depending on page state.
        """
        btn = self.driver.find_element(
            By.XPATH,
            f"//div[@class='inventory_item' and contains(.,'{product_name}')]//button"
        )
        _js_click(self.driver, btn)

    def remove_item(self, product_name: str) -> None:
        """Click 'Remove' for the given product by name.

        Uses a fresh XPath lookup every time.
        """
        btn = self.driver.find_element(
            By.XPATH,
            f"//div[@class='inventory_item' and contains(.,'{product_name}')]//button"
        )
        _js_click(self.driver, btn)

    def get_cart_count(self) -> int:
        """Return the cart badge count. Returns 0 if badge not visible."""
        try:
            badge = self.cart_badge
            if badge.is_displayed():
                return int(badge.text.strip() or "0")
        except NoSuchElementException:
            pass
        return 0

    def sort_by(self, option: str) -> None:
        """Select a sort option. e.g. 'Name (A to Z)', 'Price (low to high)'."""
        self.sort_dropdown.select_by_visible_text(option)

    def go_to_cart(self) -> None:
        """Navigate to the cart page and wait for it to load."""
        _js_click(self.driver, self.cart_link)
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-test="checkout"]')))

    def is_loaded(self) -> bool:
        """Check if the inventory page has loaded."""
        return self.title.is_displayed() and self.title.text.strip() == "Products"

    def remove_all_items(self) -> None:
        """Remove every item currently in the cart (for state cleanup)."""
        # Click "Remove" on every item that shows the Remove button
        btns = self.driver.find_elements(
            By.XPATH, "//div[@class='inventory_item']//button[contains(text(),'Remove')]")
        for btn in btns:
            _js_click(self.driver, btn)
