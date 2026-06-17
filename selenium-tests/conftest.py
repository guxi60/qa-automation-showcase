"""Selenium + pytest fixtures — Allure report integration."""

import os
import re
import subprocess
import pytest
import allure
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://www.saucedemo.com"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"

# Reuse Playwright's bundled Chromium (cross-platform).
def _find_playwright_chromium() -> str | None:
    """Return the path to the newest Playwright-bundled Chromium, if any."""
    candidates = []
    # Windows
    candidates.extend(
        (Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright").glob(
            "chromium-*/chrome-win*/chrome.exe"
        )
    )
    # Linux
    candidates.extend(
        Path.home().glob(".cache/ms-playwright/chromium-*/chrome-linux*/chrome")
    )
    candidates.sort(reverse=True)  # newest first
    return str(candidates[0]) if candidates else None

_CHROME_BINARY = _find_playwright_chromium()


@pytest.fixture(scope="function")
def driver():
    """Create a Chrome WebDriver instance per test — clean state isolation.

    Uses Playwright's bundled Chromium binary when no system Chrome is present.
    """
    chrome_options = Options()
    if _CHROME_BINARY:
        chrome_options.binary_location = _CHROME_BINARY
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")

    # Resolve a ChromeDriver whose version matches our Chromium.
    def _resolve_chromedriver() -> str:
        """Return path to a compatible ChromeDriver binary."""
        # 1. Cached driver (Windows — matches Playwright's bundled Chromium)
        _cached = list(
            (Path(os.environ.get("USERPROFILE", "")) / ".wdm" / "drivers" / "chromedriver" / "win64")
            .glob("147*/chromedriver-win64/chromedriver.exe"),
        )
        if _cached:
            return str(_cached[0])

        # 2. If using Playwright's Chromium, detect its version & match ChromeDriver
        if _CHROME_BINARY:
            try:
                out = subprocess.check_output(
                    [_CHROME_BINARY, "--version"],
                    stderr=subprocess.STDOUT, text=True, timeout=15,
                )
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)", out)
                if m:
                    return ChromeDriverManager(driver_version=m.group(1)).install()
            except Exception:
                pass

        # 3. Auto-detect (matches system Chrome / Playwright Chromium)
        try:
            return ChromeDriverManager().install()
        except Exception:
            return ChromeDriverManager(driver_version="147.0.7727.15").install()

    driver_path = _resolve_chromedriver()

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=chrome_options,
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Return a WebDriver that is already logged in."""
    driver.get(BASE_URL)
    driver.find_element("css selector", '[data-test="username"]').send_keys("standard_user")
    driver.find_element("css selector", '[data-test="password"]').send_keys("secret_sauce")
    el = driver.find_element("css selector", '[data-test="login-button"]')
    driver.execute_script("arguments[0].click();", el)
    return driver


# ── Allure: screenshot capture ────────────────────────────────

def _safe_screenshot(driver, name: str):
    """Take a screenshot and attach to Allure.  Silently skip if driver is closed."""
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    drv = item.funcargs.get("driver")

    if report.when == "call" and drv:
        if report.failed:
            # Always capture on failure
            SCREENSHOT_DIR.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = str(SCREENSHOT_DIR / f"{item.name}_{ts}.png")
            try:
                drv.save_screenshot(path)
                allure.attach.file(path, name="Failure Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception:
                pass
        else:
            # Capture a final-state screenshot for passing tests
            _safe_screenshot(drv, "Final State")


# ── Allure: environment info ──────────────────────────────────

def pytest_sessionfinish(session):
    """Write environment.properties for the Allure report.

    Branded distinctly from Playwright so the two reports are
    easy to tell apart in side-by-side comparison.
    """
    env_dir = Path("allure-results")
    env_dir.mkdir(exist_ok=True)
    (env_dir / "environment.properties").write_text(
        "Browser=Chrome (Selenium WebDriver)\n"
        "Viewport=1280x720\n"
        "Base.URL=https://www.saucedemo.com\n"
        "Language=Python 3\n"
        "Framework=Selenium + pytest\n",
        encoding="utf-8",
    )


# ── Markers ───────────────────────────────────────────────────

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: P0 critical-path")
    config.addinivalue_line("markers", "regression: regression suite")
    config.addinivalue_line("markers", "e2e: end-to-end flow")


# ── Post-report patches (pytest-html 4.2.0, for html fallback) ─

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
