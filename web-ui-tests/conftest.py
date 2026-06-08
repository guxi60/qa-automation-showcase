"""Playwright + pytest fixtures and configuration."""

from __future__ import annotations

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser
from qa_report import get_metadata

BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"

# ── fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    ctx = browser.new_context(viewport={"width": 1280, "height": 720},
                              locale="en-US")
    pg = ctx.new_page()
    pg.set_default_navigation_timeout(60000)
    yield pg
    ctx.close()


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    page.goto(BASE_URL)
    page.fill('[data-test="username"]', "standard_user")
    page.fill('[data-test="password"]', "secret_sauce")
    page.click('[data-test="login-button"]')
    page.wait_for_url("**/inventory.html")
    return page


# ── Custom report columns ─────────────────────────────────────

_stored: dict[str, dict] = {}

COLS = [
    ("tc_id",    "Test ID"),
    ("module",   "Module"),
    ("feature",  "Feature"),
    ("level",    "Level"),
    ("priority", "Priority"),
]


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        name = item.originalname if hasattr(item, "originalname") else item.name
        meta = get_metadata(name)
        if meta:
            _stored[item.nodeid] = meta


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    cells.pop()
    for _k, label in COLS:
        cells.append(f"<th>{label}</th>")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.pop()
    meta = _stored.get(report.nodeid, {})
    for key, _label in COLS:
        val = meta.get(key, "-") or "-"
        cells.append(f"<td>{val}</td>")


# ── Screenshots on failure ────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        pg = item.funcargs.get("page")
        if pg:
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            pg.screenshot(path=str(SCREENSHOT_DIR / f"{item.name}_{ts}.png"),
                          full_page=True)


# ── Markers ───────────────────────────────────────────────────

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: P0 critical-path test")
    config.addinivalue_line("markers", "regression: regression suite")
    config.addinivalue_line("markers", "e2e: end-to-end flow")


# ── Post-report patches (pytest-html 4.2.0) ──────────────────

def pytest_unconfigure(config):
    """Fix two pytest-html 4.2.0 bugs for local file:// viewing."""
    for rp in Path(__file__).parent.glob("report*.html"):
        c = rp.read_text(encoding="utf-8")

        # Fix 1: syntax error in findAll selector
        b1 = "findAll('.collapsible td:not(.col-links', row)"
        f1 = "findAll('.collapsible td:not(.col-links)', row)"
        if b1 in c:
            c = c.replace(b1, f1)

        # Fix 2: pushState on file:// aborts JS init
        b2 = "(function(){function r(e,n,t)"
        f2 = ("(function(){if(location.protocol==='file:'){"
              "history.pushState=history.replaceState="
              "function(){return arguments[2]}}"
              "})();(function(){function r(e,n,t)")
        if b2 in c:
            c = c.replace(b2, f2)

        rp.write_text(c, encoding="utf-8")
