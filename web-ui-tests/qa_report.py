"""
Lightweight test helpers — Allure integration + DDT data loading.

Design
──────
- Metadata lives in Allure-native decorators  (@allure.feature, @allure.story,
  @allure.severity, @allure.title, @allure.tag, @allure.label).
- Test data is externalised to YAML files under test_data/.
- This module provides one convenience:  load_data(file) and a thin step()
  wrapper that prints to terminal while delegating to allure.step.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, TYPE_CHECKING

import allure
import yaml

if TYPE_CHECKING:
    from playwright.sync_api import Page

# ═══════════════════════════════════════════════════════════════
#  DDT — data loading
# ═══════════════════════════════════════════════════════════════

_DATA_DIR = Path(__file__).parent / "test_data"


def load_data(filename: str) -> dict:
    """Load a YAML test-data file from test_data/."""
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


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


def capture(page: "Page", name: str = ""):
    """Full-page screenshot with cart-icon <img> injection.

    Usage from any test:

        from qa_report import capture
        capture(page, "After login")
    """
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    page.evaluate("window.scrollTo(0, 0)")

    page.evaluate("""
        () => {
          if (document.querySelector('.qa-cart-icon-fix')) return;
          const link = document.querySelector('.shopping_cart_link');
          if (!link) return;
          const bg = getComputedStyle(link).backgroundImage;
          if (bg === 'none') return;
          const start = bg.indexOf('url(');
          if (start === -1) return;
          const rest = bg.substring(start + 4).trim();
          const quote = rest.charAt(0);
          const url = (quote === '"' || quote === "'")
            ? rest.substring(1, rest.indexOf(quote, 1))
            : rest.substring(0, rest.indexOf(')'));
          if (!url) return;
          const img = document.createElement('img');
          img.src = url;
          img.className = 'qa-cart-icon-fix';
          img.style.cssText = 'display:inline-block;width:26px;height:26px;vertical-align:middle;margin-right:0.25rem;';
          link.insertBefore(img, link.firstChild);
        }
    """)
    try:
        page.wait_for_function(
            "() => { const i = document.querySelector('.qa-cart-icon-fix'); return i && i.complete && i.naturalWidth > 0; }",
            timeout=8000,
        )
    except Exception:
        pass
    page.evaluate(
        "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
    )

    png = page.screenshot(full_page=True, timeout=10000)
    display = f"Screenshot: {name}" if name else "Screenshot"
    allure.attach(png, name=display, attachment_type=allure.attachment_type.PNG)
    page.evaluate("() => { const i = document.querySelector('.qa-cart-icon-fix'); if (i) i.remove(); }")
    if name:
        print(f"    📷 {name}")


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

    if tc.get("req"):
        allure.dynamic.label("requirement", tc["req"])


# ═══════════════════════════════════════════════════════════════
#  Dynamic pytest markers from YAML tags
# ═══════════════════════════════════════════════════════════════

def register_tags_as_markers(items: list) -> None:
    """Map YAML ``tags`` fields to pytest markers (for -m filtering).

    Only adds markers already declared in ``pytest.ini`` — undeclared
    tags are still attached to Allure via ``set_meta()``.
    """
    import pytest as _pytest

    for item in items:
        if not hasattr(item, "callspec"):
            continue
        tc = item.callspec.params.get("tc")
        if not isinstance(tc, dict):
            continue
        for tag in tc.get("tags", []):
            safe = tag.replace(" ", "_").replace("-", "_")
            if not safe:
                continue
            # Only add markers that pytest already knows about (avoids
            # --strict-markers rejecting undeclared tags like "functional")
            if safe in item.config.getini("markers"):
                item.add_marker(_pytest.mark.__getattr__(safe))
