"""Playwright + pytest fixtures and configuration."""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser


BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


@pytest.fixture(scope="session")
def browser():
    """Launch a persistent browser instance for the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    """Create a fresh page for each test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US",
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Return a page that is already logged in with standard_user."""
    page.goto(BASE_URL)
    page.fill('[data-test="username"]', "standard_user")
    page.fill('[data-test="password"]', "secret_sauce")
    page.click('[data-test="login-button"]')
    page.wait_for_url("**/inventory.html")
    return page


# ----- pytest hooks -----

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically capture screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            page.screenshot(path=str(SCREENSHOT_DIR / filename), full_page=True)


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as smoke test (fast, critical path)")
    config.addinivalue_line("markers", "regression: mark test as regression test")
