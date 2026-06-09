"""
Lightweight test helpers — Allure integration + DDT data loading.

Design
──────
- Metadata lives in Allure-native decorators  (@allure.feature, @allure.story,
  @allure.severity, @allure.title, @allure.tag, @allure.label).
- Test data is shared with Playwright: loads from web-ui-tests/test_data/.
- step() prints to terminal while delegating to allure.step for the report.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, TYPE_CHECKING

import allure

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

# ═══════════════════════════════════════════════════════════════
#  DDT — data loading (shared test_data with Playwright)
# ═══════════════════════════════════════════════════════════════

_PROJECT_ROOT = Path(__file__).parent.parent
_SHARED_DATA = _PROJECT_ROOT / "web-ui-tests" / "test_data"


def load_data(filename: str) -> dict:
    """Load a JSON test-data file from the shared test_data/ directory."""
    path = _SHARED_DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════
#  Console + Allure dual-output step
# ═══════════════════════════════════════════════════════════════

@contextmanager
def step(title: str):
    """
    Context manager that prints *title* to stdout and also wraps
    the block in an allure.step() so it appears in the Allure report.
    """
    print(f"\n  ▸ {title}")
    with allure.step(title):
        yield


def action(*descriptions: str):
    """Log a UI action (click, fill, navigate) to both console and Allure."""
    for d in descriptions:
        print(f"    ▶ {d}")


def note(*lines: str):
    """Log an informational note."""
    for ln in lines:
        print(f"    · {ln}")


def capture(driver: "WebDriver", name: str = ""):
    """
    Take a full-page screenshot and attach it to the Allure report.

    Usage from any test:

        from qa_report import capture
        capture(driver, "After login")
    """
    try:
        png = driver.get_screenshot_as_png()
        display = f"Screenshot: {name}" if name else "Screenshot"
        allure.attach(png, name=display, attachment_type=allure.attachment_type.PNG)
        if name:
            print(f"    📷 {name}")
    except Exception:
        pass  # driver may be closed or unreachable


# ═══════════════════════════════════════════════════════════════
#  Dynamic Allure metadata from parametrized data
# ═══════════════════════════════════════════════════════════════

def set_meta(tc: dict):
    """
    Apply Allure dynamic metadata from a test-case dictionary.

    Expected keys (all optional):
        id, title, severity, tags, level, story
    """
    if tc.get("id"):
        allure.dynamic.title(f"{tc['id']}: {tc.get('title', '')}")
    elif tc.get("title"):
        allure.dynamic.title(tc["title"])

    sev = tc.get("severity", "")
    sev_map = {
        "BLOCKER":  allure.severity_level.BLOCKER,
        "CRITICAL": allure.severity_level.CRITICAL,
        "NORMAL":   allure.severity_level.NORMAL,
        "MINOR":    allure.severity_level.MINOR,
        "TRIVIAL":  allure.severity_level.TRIVIAL,
    }
    if sev in sev_map:
        allure.dynamic.severity(sev_map[sev])

    for tag in tc.get("tags", []):
        allure.dynamic.tag(tag)

    if tc.get("story"):
        allure.dynamic.story(tc["story"])

    if tc.get("level"):
        allure.dynamic.label("test_level", tc["level"])
