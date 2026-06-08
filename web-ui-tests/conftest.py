"""Playwright + pytest fixtures — Allure report integration."""

from __future__ import annotations

import pytest
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser

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


# ── Allure: screenshot on failure ─────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        pg = item.funcargs.get("page")
        if pg:
            try:
                SCREENSHOT_DIR.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = str(SCREENSHOT_DIR / f"{item.name}_{ts}.png")
                pg.screenshot(path=path, full_page=True, timeout=10000)
                allure.attach.file(path, name="Failure Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass  # page may be closed or unreachable


# ── Allure: environment info ──────────────────────────────────

def pytest_sessionfinish(session):
    """Write environment.properties for the Allure report."""
    env_dir = Path("allure-results")
    env_dir.mkdir(exist_ok=True)
    (env_dir / "environment.properties").write_text(
        "Browser=Chromium (Playwright)\n"
        "Viewport=1280×720\n"
        "Base.URL=https://www.saucedemo.com\n"
        "Language=Python 3\n"
        "Framework=Pytest + Playwright\n"
    )


# ── Markers ───────────────────────────────────────────────────

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: P0 critical-path")
    config.addinivalue_line("markers", "regression: regression suite")
    config.addinivalue_line("markers", "e2e: end-to-end flow")


# ── Post-report patches (pytest-html 4.2.0, for html fallback)

def pytest_unconfigure(config):
    for rp in Path(__file__).parent.glob("report*.html"):
        c = rp.read_text(encoding="utf-8")
        b1 = "findAll('.collapsible td:not(.col-links', row)"
        f1 = "findAll('.collapsible td:not(.col-links)', row)"
        if b1 in c:
            c = c.replace(b1, f1)
        b2 = "(function(){function r(e,n,t)"
        f2 = ("(function(){if(location.protocol==='file:'){"
              "history.pushState=history.replaceState="
              "function(){return arguments[2]}}"
              "})();(function(){function r(e,n,t)")
        if b2 in c:
            c = c.replace(b2, f2)
        rp.write_text(c, encoding="utf-8")
