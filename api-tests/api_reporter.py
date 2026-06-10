"""
API test helpers — DDT data loading, Allure metadata, request/response logging.

Mirrors ``web-ui-tests/qa_report.py`` for API context:
- ``load_data()`` reads YAML from ``test_data/``
- ``set_meta(tc)`` binds dynamic Allure metadata from a YAML test-case dict
- ``step()`` prints to terminal *and* wraps ``allure.step()``
- ``action()`` / ``note()`` log UI/API actions to the console
- ``log_request()`` / ``log_response()`` attach full HTTP details to Allure
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import allure
import yaml
import requests

_DATA_DIR = Path(__file__).parent / "test_data"


# ═══════════════════════════════════════════════════════════════
#  DDT — data loading
# ═══════════════════════════════════════════════════════════════

def load_data(filename: str) -> dict:
    """Load a YAML test-data file from ``api-tests/test_data/``."""
    path = _DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════
#  Allure — dynamic metadata (same contract as web-ui-tests)
# ═══════════════════════════════════════════════════════════════

def set_meta(tc: dict):
    """Apply dynamic Allure metadata from a DDT test-case dictionary.

    Expected keys (all optional):
        id, title, severity, tags, story, level
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


# ═══════════════════════════════════════════════════════════════
#  Console + Allure dual-output helpers
# ═══════════════════════════════════════════════════════════════

@contextmanager
def step(title: str):
    """Context manager — prints *title* to stdout and wraps in allure.step()."""
    print(f"\n  ▸ {title}")
    with allure.step(title):
        yield


def action(*descriptions: str):
    """Log an action to the console terminal."""
    for d in descriptions:
        print(f"    ▶ {d}")


def note(*lines: str):
    """Log an informational note to the console."""
    for ln in lines:
        print(f"    · {ln}")


# ═══════════════════════════════════════════════════════════════
#  Allure — attach HTTP request / response details
# ═══════════════════════════════════════════════════════════════

def _redact_headers(headers: dict) -> dict:
    """Return a copy of *headers* with auth tokens redacted."""
    redacted = {}
    for k, v in headers.items():
        if k.lower() in ("authorization", "x-api-key", "cookie", "set-cookie"):
            redacted[k] = f"{v[:20]}..." if len(v) > 20 else "***"
        else:
            redacted[k] = v
    return redacted


def _safe_body(resp_or_req) -> str:
    """Best-effort extract body as a printable string."""
    body = None
    # Try to get body from a PreparedRequest
    if hasattr(resp_or_req, "body") and resp_or_req.body is not None:
        body = resp_or_req.body
        if isinstance(body, bytes):
            try:
                body = body.decode("utf-8")
            except Exception:
                body = repr(body)
    # Try .text for response
    if body is None and hasattr(resp_or_req, "text"):
        try:
            body = resp_or_req.text
            # Truncate very large bodies for readability
            if len(body) > 4000:
                body = body[:4000] + "\n... [truncated]"
        except Exception:
            body = "[binary / unreadable]"
    if body is None:
        body = "(no body)"
    return body


def log_request(resp: requests.Response):
    """Attach the **request** portion of *resp* to the current Allure step.

    Call this immediately after making an HTTP request — the ``requests``
    library stores the outgoing ``PreparedRequest`` on every ``Response``
    object in ``resp.request``.
    """
    req = resp.request
    if req is None:
        return

    body = _safe_body(req)
    try:
        formatted = json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        formatted = body

    detail = (
        f"{req.method} {req.url}\n\n"
        f"Headers:\n{json.dumps(_redact_headers(dict(req.headers)), indent=2, ensure_ascii=False)}\n\n"
        f"Body:\n{formatted}"
    )
    allure.attach(
        detail,
        name=f"REQUEST: {req.method} {req.path_url}",
        attachment_type=allure.attachment_type.TEXT,
    )


def log_response(resp: requests.Response):
    """Attach response status, headers, body, and timing to the current
    Allure step.

    Call this after ``log_request()`` for a complete request/response
    pair in the report.
    """
    body = _safe_body(resp)
    try:
        formatted = json.dumps(json.loads(body), indent=2, ensure_ascii=False)
    except Exception:
        formatted = body

    elapsed_ms = round(resp.elapsed.total_seconds() * 1000)

    detail = (
        f"Status: {resp.status_code} {resp.reason}\n"
        f"Duration: {elapsed_ms} ms\n"
        f"URL: {resp.url}\n\n"
        f"Headers:\n{json.dumps(_redact_headers(dict(resp.headers)), indent=2, ensure_ascii=False)}\n\n"
        f"Body:\n{formatted}"
    )
    allure.attach(
        detail,
        name=f"RESPONSE: {resp.status_code} ({elapsed_ms}ms)",
        attachment_type=allure.attachment_type.TEXT,
    )


def report(resp: requests.Response, *, node: Any = None):
    """Attach full request + response details to Allure AND store on the
    pytest node for failure-time attachment.

    This is the "one call" replacement for the old ``track(resp)``.
    If *node* is ``None`` (e.g. called from a helper, not a test function),
    the per-node storage is skipped.
    """
    log_request(resp)
    log_response(resp)
    if node is not None:
        node._last_response = resp
