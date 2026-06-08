"""QA test reporting helpers: structured logging and test-case metadata.

Usage:

    from qa_report import TestLog, testcase

    @testcase(
        id="TC-LOGIN-001",
        category="Functional / Authentication",
        precondition="SauceDemo login page is accessible.",
        test_data="standard_user / secret_sauce",
        priority="P0 (Smoke)",
    )
    def test_login_with_valid_credentials(page):
        log = TestLog()          # ← auto-discovers @testcase metadata
        log.step("Navigate to login page")
        log.detail("Opened https://www.saucedemo.com/")
        ...
        log.verify("Page redirects to inventory", actual_url == expected_url)
        log.passed("Login with valid credentials works as expected")
"""

import inspect
from typing import Any

# ── Global metadata registry ───────────────────────────────────

# Keys are function short-names (e.g. "test_login_with_valid_credentials").
# Values use column keys matching conftest.py QA_COLUMNS.
_metadata_registry: dict[str, dict] = {}


def testcase(
    id: str = "",
    category: str = "",
    precondition: str = "",
    test_data: str = "",
    priority: str = "",
):
    """Decorator: attach QA metadata to a test function."""

    def decorator(func):
        _metadata_registry[func.__name__] = {
            "tc_id":     id,
            "category":  category,
            "priority":  priority,
            "precond":   precondition,
            "testdata":  test_data,
        }
        return func

    return decorator


def get_metadata(key: str = "") -> dict:
    """Return metadata dict for a function name, or the whole registry."""
    if key:
        return _metadata_registry.get(key, {})
    return dict(_metadata_registry)


# ── Structured test logger ─────────────────────────────────────

class TestLog:
    """Print structured QA test output visible in pytest-html report."""

    __test__ = False  # not a test class — prevents pytest collection warning
    DIVIDER = "─" * 60

    def __init__(self, title: str = "", meta: dict | None = None):
        # Auto-discover metadata from the calling test function
        if meta is None:
            caller = inspect.stack()[1].function
            meta = _metadata_registry.get(caller, {})

        if title:
            print(self.DIVIDER)
            print(f"TEST: {title}")

        mid  = meta.get("tc_id", "")
        cat  = meta.get("category", "")
        pri  = meta.get("priority", "")
        pre  = meta.get("precond", "")
        tdat = meta.get("testdata", "")
        if mid and cat:
            print(self.DIVIDER)
            print(f"CASE: {mid}  |  {cat}  |  {pri}")
            if pre:
                print(f"  PRECONDITION: {pre}")
            if tdat:
                print(f"  TEST DATA:    {tdat}")
            print(self.DIVIDER)
            print()

    # ── Steps ──────────────────────────────────────────────────

    _step_counter: int = 0

    def step(self, description: str):
        self._step_counter += 1
        print(f"STEP {self._step_counter}: {description}")

    def detail(self, *lines: str):
        for line in lines:
            print(f"  → {line}")

    # ── Verification / checks ──────────────────────────────────

    def verify(self, assertion_label: str, condition: bool) -> bool:
        status = "✓ PASS" if condition else "✗ FAIL"
        print(f"\nVERIFY: {assertion_label}")
        print(f"  {status}")
        if not condition:
            print(f"  ⚠ EXPECTATION NOT MET")
        return condition

    def check(self, label: str, actual: Any, expected: Any = None):
        if expected is not None:
            match = actual == expected
            mark = "✓" if match else "✗"
            print(f"  {mark} {label}: actual={actual!r}, expected={expected!r}")
        else:
            print(f"  • {label}: {actual!r}")

    # ── Result ──────────────────────────────────────────────────

    def passed(self, summary: str = ""):
        print()
        if summary:
            print(f"RESULT: PASSED — {summary}")
        else:
            print("RESULT: PASSED")
        print()

    def failed(self, reason: str):
        print()
        print(f"RESULT: FAILED — {reason}")
        print()
