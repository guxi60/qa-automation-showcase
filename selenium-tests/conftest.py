"""Selenium + pytest fixtures and configuration."""

import pytest
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


@pytest.fixture(scope="session")
def driver():
    """Create a Chrome WebDriver instance for the entire session."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Return a WebDriver that is already logged in."""
    driver.get(BASE_URL)
    driver.find_element("css selector", '[data-test="username"]').send_keys("standard_user")
    driver.find_element("css selector", '[data-test="password"]').send_keys("secret_sauce")
    driver.find_element("css selector", '[data-test="login-button"]').click()
    return driver


# ----- pytest hooks -----

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            driver.save_screenshot(str(SCREENSHOT_DIR / filename))


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: fast critical path test")
    config.addinivalue_line("markers", "regression: regression test")
