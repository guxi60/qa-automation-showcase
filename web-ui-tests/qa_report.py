"""
Professional test reporting framework.

Design principles
──────────────────
1.  Every test case is a formal entity: ID, title, module, feature, test
    level, priority, tags, requirements traceability, preconditions, test
    data, expected result.
2.  The execution log is a structured, timestamped event stream: each step
    produces ACTION → CHECK → VERIFY events, with actual-vs-expected for
    every verification point.
3.  The HTML report table shows scannable columns (ID, Module, Level,
    Priority) so a hiring manager can grasp coverage at a glance.
4.  The expanded detail panel tells the full story — from preconditions
    through each step to the final verdict.

Usage
─────
    from qa_report import testcase, TestLog

    @testcase(
        id="TC-LOGIN-001",
        title="Valid credentials grant access to inventory",
        module="Authentication",
        feature="Login",
        level="System",
        priority="P0",
        tags=["smoke", "happy-path"],
        precondition=[
            "SauceDemo login page is accessible.",
            "User 'standard_user' exists.",
        ],
        test_data={"username": "standard_user", "password": "secret_sauce"},
        expected="Redirected to /inventory.html; 6 products displayed.",
    )
    def test_login_with_valid_credentials(page):
        log = TestLog()                    # ← auto-discovers metadata
        log.step("Navigate to login page")
        log.action("goto https://www.saucedemo.com/")
        log.check("Login button visible", login.btn.is_visible(), True)
        ...
        log.verify("Redirected to inventory",
                   actual=page.url,
                   expected=InventoryPage.URL)
        log.finish("PASSED")
"""

from __future__ import annotations

import inspect
import json
from datetime import datetime, timezone
from typing import Any, Callable

# ═══════════════════════════════════════════════════════════════
#  Metadata registry
# ═══════════════════════════════════════════════════════════════

_registry: dict[str, "TestCase"] = {}


class TestCase:
    """Immutable test-case descriptor."""

    __slots__ = (
        "id", "title", "module", "feature", "level",
        "priority", "tags", "requirement", "precondition",
        "test_data", "expected",
    )

    def __init__(
        self,
        id: str,
        title: str = "",
        module: str = "",
        feature: str = "",
        level: str = "System",
        priority: str = "P2",
        tags: list[str] | None = None,
        requirement: str = "",
        precondition: str | list[str] = "",
        test_data: Any = None,
        expected: str = "",
    ):
        self.id = id
        self.title = title
        self.module = module
        self.feature = feature
        self.level = level
        self.priority = priority
        self.tags = tags or []
        self.requirement = requirement
        self.precondition = precondition
        self.test_data = test_data
        self.expected = expected

    # -- friendly accessors used by conftest columns -----------------

    @property
    def precond_str(self) -> str:
        if isinstance(self.precondition, list):
            return "; ".join(self.precondition)
        return self.precondition or "-"

    @property
    def testdata_str(self) -> str:
        if self.test_data is None:
            return "-"
        if isinstance(self.test_data, dict):
            return ", ".join(f"{k}={v}" for k, v in self.test_data.items())
        return str(self.test_data)

    @property
    def tags_str(self) -> str:
        return ", ".join(self.tags) if self.tags else "-"

    def to_dict(self) -> dict:
        return {
            "tc_id":    self.id,
            "module":   self.module,
            "feature":  self.feature,
            "level":    self.level,
            "priority": self.priority,
            "tags":     self.tags_str,
        }


def testcase(
    id: str,
    title: str = "",
    module: str = "",
    feature: str = "",
    level: str = "System",
    priority: str = "P2",
    tags: list[str] | None = None,
    requirement: str = "",
    precondition: str | list[str] = "",
    test_data: Any = None,
    expected: str = "",
) -> Callable:
    """
    Decorator: attach a formal TestCase descriptor to a pytest function.

    The descriptor is stored in the global registry and picked up by
    conftest.py hooks to populate custom HTML report columns.
    """
    tc = TestCase(
        id=id, title=title, module=module, feature=feature,
        level=level, priority=priority, tags=tags,
        requirement=requirement, precondition=precondition,
        test_data=test_data, expected=expected,
    )

    def decorator(func):
        _registry[func.__name__] = tc
        return func

    return decorator


def get_metadata(key: str = "") -> dict:
    """Retrieve a TestCase as a flat dict (for conftest column rendering)."""
    if key:
        tc = _registry.get(key)
        return tc.to_dict() if tc else {}
    return {}


def get_testcase(key: str = "") -> TestCase | None:
    """Retrieve the full TestCase object."""
    return _registry.get(key)


# ═══════════════════════════════════════════════════════════════
#  Structured test logger
# ═══════════════════════════════════════════════════════════════

class TestLog:
    """
    Professional test execution logger.

    Produces structured, scannable plain-text output that renders
    beautifully inside the pytest-html report log panel.
    """

    __test__ = False  # not a pytest collection target

    # Visual constants
    _B  = "┃"   # heavy vertical
    _TL = "┏"   # top-left
    _TR = "┓"   # top-right
    _BL = "┗"   # bottom-left
    _BR = "┛"   # bottom-right
    _H  = "━"   # heavy horizontal
    _S  = "┣"   # section left
    _SR = "┫"   # section right
    _L  = "╼"   # light horizontal (for sub-items)

    P0 = "■"
    P1 = "▲"
    P2 = "◆"
    _CHECK   = "✓"
    _CROSS   = "✗"

    _W = 64   # log width

    def __init__(self):
        # Auto-discover metadata
        caller = inspect.stack()[1].function
        self._tc = _registry.get(caller)
        self._step_n = 0
        self._start = datetime.now(timezone.utc)
        self._print_header()

    # ── Header block ─────────────────────────────────────────

    def _print_header(self):
        W = self._W
        B, H, S, SR, L, TL, TR, BL, BR = (
            self._B, self._H, self._S, self._SR, self._L,
            self._TL, self._TR, self._BL, self._BR,
        )

        tc = self._tc
        if tc is None:
            return  # test not decorated; skip header

        # Top rule + case id + title
        print(f"{TL}{H * (W-2)}{TR}")
        print(f"{B}  CASE  {tc.id:<52}{B}")
        if tc.title:
            print(f"{B}  {tc.title[:W-4]:<{W-4}}{B}")
        print(f"{S}{H * (W-2)}{SR}")

        # Metadata row
        rows = [
            ("Module",    tc.module,    "Level",    tc.level),
            ("Feature",   tc.feature,   "Priority",  f"{self._pri_icon(tc.priority)} {tc.priority}"),
        ]
        for left_k, left_v, right_k, right_v in rows:
            lhs = f"  {left_k:<10}{left_v:<19}"
            rhs = f"{right_k:<10}{right_v}"
            print(f"{B}{lhs}{rhs}{' ' * (W - 2 - len(lhs) - len(rhs))}{B}")

        # Tags & requirement (single row)
        tags = ", ".join(tc.tags) if tc.tags else "—"
        req  = tc.requirement or "—"
        line = f"  Tags       {tags:<19}Req.       {req}"
        print(f"{B}{line}{' ' * max(0, W - 2 - len(line))}{B}")
        print(f"{S}{H * (W-2)}{SR}")

        # Preconditions
        pre = tc.precondition
        if isinstance(pre, str):
            pre = [pre] if pre else []
        if pre:
            print(f"{B}  PRECONDITION{' ' * (W - 16)}{B}")
            for i, p in enumerate(pre, 1):
                print(f"{B}    {i}. {p[:W-8]:<{W-8}}{B}")
            print(f"{S}{H * (W-2)}{SR}")

        # Test data
        td = tc.test_data
        if td is not None:
            print(f"{B}  TEST DATA{' ' * (W - 13)}{B}")
            if isinstance(td, dict):
                for k, v in td.items():
                    line = f"    {k:<14}= {v}"
                    print(f"{B}{line}{' ' * max(0, W - 2 - len(line))}{B}")
            else:
                print(f"{B}    {str(td)[:W-6]:<{W-6}}{B}")
            print(f"{S}{H * (W-2)}{SR}")

        # Expected result
        if tc.expected:
            print(f"{B}  EXPECTED RESULT{' ' * (W - 18)}{B}")
            print(f"{B}    {tc.expected[:W-6]:<{W-6}}{B}")

        # Bottom rule
        print(f"{BL}{H * (W-2)}{BR}")
        print()

        # Start marker
        ts = self._start.strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"  [{ts}]  TEST STARTED")
        print()

    @staticmethod
    def _pri_icon(priority: str) -> str:
        if "P0" in priority: return TestLog.P0
        if "P1" in priority: return TestLog.P1
        return TestLog.P2

    # ── Step methods ──────────────────────────────────────────

    def step(self, description: str):
        self._step_n += 1
        print(f"  STEP {self._step_n}: {description}")
        print()

    def action(self, *descriptions: str):
        for d in descriptions:
            print(f"    ▶ {d}")

    def note(self, *lines: str):
        for ln in lines:
            print(f"    · {ln}")

    # ── Checkpoints ───────────────────────────────────────────

    def check(self,
              label: str,
              actual: Any,
              expected: Any = None,
              ) -> bool:
        if expected is not None:
            ok = (actual == expected)
            mark = self._CHECK if ok else self._CROSS
            print(f"    CHECK   {label}")
            print(f"            actual   = {actual!r}")
            print(f"            expected = {expected!r}")
            print(f"            {mark} {'PASS' if ok else 'FAIL'}")
            print()
            return ok
        else:
            # boolean check
            ok = bool(actual)
            mark = self._CHECK if ok else self._CROSS
            print(f"    CHECK   {label}  {mark}")
            print()
            return ok

    def verify(self,
               assertion: str,
               actual: Any = None,
               expected: Any = None,
               ) -> bool:
        if actual is not None and expected is not None:
            ok = (actual == expected)
        elif actual is not None:
            ok = bool(actual)
        else:
            ok = True  # caller already passed condition as assertion

        mark = f"{self._CHECK} PASS" if ok else f"{self._CROSS} FAIL"
        print(f"    VERIFY  {assertion}")
        if actual is not None and expected is not None:
            print(f"            actual   = {actual!r}")
            print(f"            expected = {expected!r}")
        elif actual is not None:
            print(f"            value = {actual!r}")
        print(f"            {mark}")
        print()
        return ok

    # ── Final verdict ─────────────────────────────────────────

    def finish(self, passed: bool | str = True, summary: str = ""):
        """Emit the final result line.  `passed` can be True, False, or "PASSED"."""
        if isinstance(passed, str):
            is_pass = "PASS" in passed.upper()
        else:
            is_pass = bool(passed)

        mark = f"{self._CHECK}  PASSED" if is_pass else f"{self._CROSS}  FAILED"
        elapsed = (datetime.now(timezone.utc) - self._start).total_seconds()

        print(f"  {'─' * 56}")
        print(f"  RESULT   {mark}")
        if summary:
            print(f"           {summary}")
        print(f"  ───────────────────────────────────────────────────────")
        print(f"  Duration {elapsed:.1f}s")
        print()
