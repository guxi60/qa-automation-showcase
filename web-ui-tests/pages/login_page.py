"""Login page object for SauceDemo."""

from playwright.sync_api import Page, Locator


class LoginPage:
    """Page object for https://www.saucedemo.com/ login."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def goto(self, retries: int = 3) -> None:
        """Navigate to the login page, with retry for flaky networks."""
        for attempt in range(retries + 1):
            try:
                self.page.goto(self.URL, timeout=45000)
                return
            except Exception:
                if attempt == retries:
                    raise
                self.page.wait_for_timeout(3000 * (attempt + 1))

    def login(self, username: str, password: str) -> None:
        """Fill credentials and click login."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        """Return the error message text, or empty string if none."""
        self.error_message.wait_for(state="visible", timeout=3000)
        return self.error_message.text_content() or ""

    def is_error_visible(self) -> bool:
        """Check if the error message is displayed."""
        return self.error_message.is_visible()
