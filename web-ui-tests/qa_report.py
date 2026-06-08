"""
Lightweight test helpers — Allure integration + DDT data loading.

Design
──────
- Metadata lives in Allure-native decorators  (@allure.feature, @allure.story,
  @allure.severity, @allure.title, @allure.tag, @allure.label).
- Test data is externalised to JSON files under test_data/.
- This module provides one convenience:  load_data(file) and a thin step()
  wrapper that prints to terminal while delegating to allure.step.
"""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import allure

# ═══════════════════════════════════════════════════════════════
#  DDT — data loading
# ═══════════════════════════════════════════════════════════════

_DATA_DIR = Path(__file__).parent / "test_data"


def load_data(filename: str) -> dict:
    """Load a JSON test-data file from test_data/."""
    path = _DATA_DIR / filename
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
