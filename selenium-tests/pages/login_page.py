"""Login page object for SauceDemo — Selenium edition."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def _js_click(driver, element) -> None:
    """Click via JavaScript — reliable on Linux headless WebDriver."""
    driver.execute_script("arguments[0].click();", element)


def _js_input(driver, element, text: str) -> None:
    """Fill an input via JavaScript — reliable on Linux headless WebDriver."""
    driver.execute_script(
        "arguments[0].value=''; arguments[0].value=arguments[1];"
        "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
        element, text,
    )


class LoginPage:
    """Page object for https://www.saucedemo.com/ login."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ── locators ────────────────────────────────────────────────

    @property
    def username_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="username"]')

    @property
    def password_input(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="password"]')

    @property
    def login_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="login-button"]')

    @property
    def error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')

    # ── actions ─────────────────────────────────────────────────

    def goto(self, retries: int = 3) -> None:
        """Navigate to the login page, with retry for flaky networks."""
        for attempt in range(retries + 1):
            try:
                self.driver.get(self.URL)
                return
            except Exception:
                if attempt == retries:
                    raise
                import time
                time.sleep(3 * (attempt + 1))

    def login(self, username: str, password: str) -> None:
        """Fill credentials and click login.  Waits for the server response."""
        _js_input(self.driver, self.username_input, username)
        _js_input(self.driver, self.password_input, password)
        _js_click(self.driver, self.login_button)
        # Wait for either a successful redirect or an error message
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "/inventory.html" in d.current_url
                or d.find_elements(By.CSS_SELECTOR, '[data-test="error"]')
            )
        except TimeoutException:
            pass  # caller decides how to handle

    def get_error_text(self) -> str:
        """Return the error message text, or empty string if none."""
        try:
            self.wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test="error"]')))
            return self.error_message.text.strip()
        except TimeoutException:
            return ""

    def is_error_visible(self) -> bool:
        """Check if the error message is displayed."""
        try:
            return self.error_message.is_displayed()
        except Exception:
            return False
