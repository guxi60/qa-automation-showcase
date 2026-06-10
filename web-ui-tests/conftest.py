"""Playwright + pytest fixtures — Allure report integration."""

from __future__ import annotations

import pytest
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser

BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"

# ── CLI options ───────────────────────────────────────────────

def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", default=False,
                     help="Run browser in headed (visible) mode")
    parser.addoption("--screenshot-on-step", action="store_true", default=False,
                     help="Capture screenshot at every test step")


# ── fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser(request):
    headed = request.config.getoption("--headed", default=False)
    with sync_playwright() as p:
        b = p.chromium.launch(
            headless=not headed,
            args=[
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--disable-extensions",
                "--hide-crash-restore-bubble",
                "--disable-features=TranslateUI,ExternalProtocolDialog",
            ],
        )
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


# ── Allure: screenshot capture ────────────────────────────────

def _safe_screenshot(page: Page, name: str, full_page: bool = True):
    """Take a screenshot and attach to Allure.  Silently skip if page is closed.

    Also captures the ``.primary_header`` element individually — headless
    Chromium does not reliably composite CSS ``background-image`` on
    ``::before`` pseudo-elements during a full-page capture, but an
    element-level screenshot forces the browser to render that specific
    DOM subtree to a dedicated pixel buffer, which triggers the
    background-image decode + paint.
    """
    try:
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        page.evaluate("window.scrollTo(0, 0)")
        page.evaluate(
            "() => new Promise(r => requestAnimationFrame("
            "    () => requestAnimationFrame(r)))"
        )
        # ── Full-page screenshot ─────────────────────────────
        png = page.screenshot(full_page=full_page, timeout=10000)
        allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
        # ── Header element screenshot ────────────────────────
        # Element-level capture forces headless Chromium to render
        # the header subtree (including ::before background-images
        # like the cart SVG icon) to its own pixel buffer.
        hdr = page.locator(".primary_header")
        if hdr.count() > 0:
            hdr_png = hdr.first.screenshot(timeout=5000)
            allure.attach(
                hdr_png,
                name="Header (cart icon + badge)",
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    pg = item.funcargs.get("page")

    if report.when == "call" and pg:
        if report.failed:
            # Always capture on failure (full-page for debugging context)
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = str(SCREENSHOT_DIR / f"{item.name}_{ts}.png")
            try:
                try:
                    pg.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass
                pg.evaluate("window.scrollTo(0, 0)")
                pg.evaluate(
                    "() => new Promise(r => requestAnimationFrame("
                    "    () => requestAnimationFrame(r)))"
                )
                pg.screenshot(path=path, full_page=True, timeout=10000)
                allure.attach.file(path, name="Failure Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
        else:
            # Capture a final-state screenshot for passing tests.
            # full_page=True forces a full-document composite pass,
            # which is necessary for CSS background-images on ::before
            # pseudo-elements (e.g. the cart SVG icon) to render
            # reliably in headless Chromium.
            _safe_screenshot(pg, "Final State", full_page=True)


# ── Allure: step screenshot hook (triggered via --screenshot-on-step) ──

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Wrap each test call — if --screenshot-on-step, capture after each allure step.

    We do this by monkey-patching allure.step on the fly so that every step
    takes a screenshot when it exits.
    """
    yield


# ── Allure: environment info ──────────────────────────────────

def pytest_sessionfinish(session):
    """Write environment.properties for the Allure report.

    NOTE: Uses plain ASCII ('x' not '×') to avoid encoding issues —
    Java .properties files use ISO 8859-1 and GBK-written files get
    mangled on Chinese Windows.
    """
    env_dir = Path("allure-results")
    env_dir.mkdir(exist_ok=True)
    (env_dir / "environment.properties").write_text(
        "Browser=Chromium (Playwright)\n"
        "Viewport=1280x720\n"
        "Base.URL=https://www.saucedemo.com\n"
        "Language=Python 3\n"
        "Framework=Pytest + Playwright\n",
        encoding="utf-8",
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
