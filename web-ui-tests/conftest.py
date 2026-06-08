"""Playwright + pytest fixtures and configuration — with custom report columns."""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser
from qa_report import get_metadata

BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"

# ----- fixtures -----

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
    page.set_default_navigation_timeout(60000)
    yield page
    context.close()


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Pre-authenticated page (standard_user on inventory)."""
    page.goto(BASE_URL)
    page.fill('[data-test="username"]', "standard_user")
    page.fill('[data-test="password"]', "secret_sauce")
    page.click('[data-test="login-button"]')
    page.wait_for_url("**/inventory.html")
    return page


# ----- Custom report columns via pytest-html hooks -----

_stored_meta: dict[str, dict] = {}

QA_COLUMNS = [
    ("tc_id",     "Test ID"),
    ("category",  "Category"),
    ("priority",  "Priority"),
    ("precond",   "Precondition"),
    ("testdata",  "Test Data"),
]


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    """Copy @testcase metadata so it's accessible during report generation."""
    for item in items:
        func_name = item.originalname if hasattr(item, "originalname") else item.name
        meta = get_metadata(func_name)
        if meta:
            _stored_meta[item.nodeid] = meta


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    """Add QA-specific column headers to the report table."""
    cells.pop()  # drop unused "Links" column
    for _key, label in QA_COLUMNS:
        cells.append(f"<th>{label}</th>")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    """Populate QA-specific columns per test row."""
    cells.pop()
    meta = _stored_meta.get(report.nodeid, {})
    for key, _label in QA_COLUMNS:
        val = meta.get(key, "-") or "-"
        cells.append(f"<td>{val}</td>")


# ----- other pytest hooks -----

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
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
    config.addinivalue_line("markers", "smoke: fast critical path test")
    config.addinivalue_line("markers", "regression: regression test")
    config.addinivalue_line("markers", "e2e: end-to-end flow test")


def pytest_unconfigure(config):
    """Patch pytest-html 4.2.0 for local file:// viewing.

    - Fix 1: findAll :not() CSS selector syntax error
    - Fix 2: history.pushState throws SecurityError on file:// → JS init aborts
    """
    report_candidates = list(Path(__file__).parent.glob("report*.html"))
    for rp in report_candidates:
        content = rp.read_text(encoding="utf-8")

        # Fix 1: findAll missing )
        b1 = "findAll('.collapsible td:not(.col-links', row)"
        f1 = "findAll('.collapsible td:not(.col-links)', row)"
        if b1 in content:
            content = content.replace(b1, f1)

        # Fix 2: pushState on file:// kills init before bindEvents()
        b2 = "(function(){function r(e,n,t)"
        f2 = (
            "(function(){if(location.protocol==='file:'){"
            "history.pushState=history.replaceState=function(){return arguments[2]}}"
            "})();(function(){function r(e,n,t)"
        )
        if b2 in content:
            content = content.replace(b2, f2)

        rp.write_text(content, encoding="utf-8")
