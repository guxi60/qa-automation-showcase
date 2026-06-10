"""User CRUD + Schema validation — DDT-driven, Allure-rich.

Test cases (7) sourced from ``test_data/users_api.yaml``:
    TC-API-USERS-001   GET /users — list all
    TC-API-USERS-002   GET /users/1 — single + schema
    TC-API-USERS-003   POST /users — create
    TC-API-USERS-004   PUT /users/1 — update
    TC-API-USERS-005   DELETE /users/1 — remove
    TC-API-USERS-006   GET /users/999 — 404 (negative)
    TC-API-USERS-007   Schema batch validation
"""

from __future__ import annotations

import allure
import pytest

from conftest import load_schema, assert_valid_schema
from api_reporter import load_data, set_meta, step, action, note

USER_SCHEMA = load_schema("user_schema.json")

# ── Method dispatch ─────────────────────────────────────────────

_METHODS = {
    "GET":    lambda api, url, **kw: api.get(url, **kw),
    "POST":   lambda api, url, **kw: api.post(url, json=kw.pop("json", kw.pop("payload", {})), **kw),
    "PUT":    lambda api, url, **kw: api.put(url, json=kw.pop("json", kw.pop("payload", {})), **kw),
    "DELETE": lambda api, url, **kw: api.delete(url, **kw),
}


def _call(api, base_url: str, tc: dict):
    """Execute the HTTP request described by *tc*."""
    method = tc["method"]
    url = f"{base_url}{tc['endpoint']}"
    payload = tc.get("payload", {})
    params = tc.get("query_params", {})
    fn = _METHODS[method]
    if method in ("POST", "PUT"):
        return fn(api, url, json=payload, params=params)
    return fn(api, url, params=params)


# ── Parametrized test ───────────────────────────────────────────

@allure.feature("Users API")
@pytest.mark.parametrize("tc", load_data("users_api.yaml")["users"],
                         ids=lambda tc: tc["id"])
def test_users(api, base_url, tc, report):
    """DDT-driven Users API test — one pytest item per YAML record."""
    set_meta(tc)

    method = tc["method"]
    endpoint = tc["endpoint"]
    assert_type = tc["assert_type"]

    # ── 1. Execute ──────────────────────────────────────────
    with step(f"{method} {endpoint}"):
        resp = _call(api, base_url, tc)
        action(f"{method} {resp.url}")
        report(resp)

    # ── 2. Status code ──────────────────────────────────────
    expected = tc["expected_status"]
    with step(f"Assert HTTP {expected}"):
        assert resp.status_code == expected, (
            f"Expected {expected}, got {resp.status_code}"
        )

    # ── 3. Domain assertions (branch on assert_type) ─────────
    data = resp.json() if resp.status_code < 400 and resp.text else None

    if assert_type == "collection":
        with step(f"Assert list of {tc['expected_count']} users"):
            assert isinstance(data, list)
            assert len(data) == tc["expected_count"]
        with step("Assert every user has required fields"):
            required = {"id", "name", "username", "email", "address",
                        "phone", "website", "company"}
            for i, user in enumerate(data):
                missing = required - set(user.keys())
                assert not missing, (
                    f"User[{i}] (id={user.get('id')}) missing: {missing}"
                )

    elif assert_type == "single":
        with step("Validate response against User JSON Schema"):
            assert_valid_schema(data, USER_SCHEMA,
                                description=f"GET {endpoint}")
        with step(f"Assert id == {tc['expected_id']}"):
            assert data["id"] == tc["expected_id"]

    elif assert_type == "create":
        with step("Assert echoed fields match submitted payload"):
            for key in ("name", "username", "email"):
                assert data[key] == tc["payload"][key], (
                    f"Mismatch on {key!r}"
                )
        with step("Assert id is auto-assigned"):
            assert "id" in data and isinstance(data["id"], int)

    elif assert_type == "update":
        with step("Assert response reflects submitted update"):
            for key in ("name", "email", "username"):
                assert data[key] == tc["payload"][key]

    elif assert_type == "delete":
        note("DELETE returned 200 OK (JSONPlaceholder convention)")

    elif assert_type == "negative":
        note(f"Confirmed: {endpoint} returns 404 as expected")

    elif assert_type == "schema_batch":
        with step(f"Validate each of {len(data)} users against schema"):
            failures = []
            for user in data:
                try:
                    assert_valid_schema(user, USER_SCHEMA,
                                        description=f"id={user.get('id')}")
                except AssertionError as exc:
                    failures.append(str(exc))
            if failures:
                pytest.fail(
                    f"{len(failures)}/{len(data)} users failed:\n"
                    + "\n".join(failures)
                )
            note(f"All {len(data)} users passed schema validation")
