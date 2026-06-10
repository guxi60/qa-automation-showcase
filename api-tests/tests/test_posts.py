"""Post CRUD + Schema validation — DDT-driven, Allure-rich.

Test cases (7) sourced from ``test_data/posts_api.yaml``:
    TC-API-POSTS-001   GET /posts — list all
    TC-API-POSTS-002   GET /posts/1 — single + schema
    TC-API-POSTS-003   POST /posts — create
    TC-API-POSTS-004   PUT /posts/1 — update
    TC-API-POSTS-005   DELETE /posts/1 — remove
    TC-API-POSTS-006   GET /posts?userId=1 — filter
    TC-API-POSTS-007   Schema batch validation
"""

from __future__ import annotations

import allure
import pytest

from conftest import load_schema, assert_valid_schema
from api_reporter import load_data, set_meta, step, action, note

POST_SCHEMA = load_schema("post_schema.json")

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

@allure.feature("Posts API")
@pytest.mark.parametrize("tc", load_data("posts_api.yaml")["posts"],
                         ids=lambda tc: tc["id"])
def test_posts(api, base_url, tc, report):
    """DDT-driven Posts API test — one pytest item per YAML record."""
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
        with step(f"Assert list of {tc['expected_count']} posts"):
            assert isinstance(data, list)
            assert len(data) == tc["expected_count"]
        with step("Assert every post has required fields"):
            required = {"userId", "id", "title", "body"}
            for i, post in enumerate(data):
                missing = required - set(post.keys())
                assert not missing, (
                    f"Post[{i}] (id={post.get('id')}) missing: {missing}"
                )

    elif assert_type == "single":
        with step("Validate response against Post JSON Schema"):
            assert_valid_schema(data, POST_SCHEMA,
                                description=f"GET {endpoint}")
        with step(f"Assert id == {tc['expected_id']}"):
            assert data["id"] == tc["expected_id"]

    elif assert_type == "create":
        with step("Assert echoed fields match submitted payload"):
            for key in ("title", "body", "userId"):
                assert data[key] == tc["payload"][key], (
                    f"Mismatch on {key!r}"
                )
        with step("Assert id is auto-assigned"):
            assert "id" in data and isinstance(data["id"], int)

    elif assert_type == "update":
        with step("Assert response reflects submitted update"):
            for key in ("title", "body"):
                assert data[key] == tc["payload"][key]

    elif assert_type == "delete":
        note("DELETE returned 200 OK (JSONPlaceholder convention)")

    elif assert_type == "filter":
        field = tc["validate_field"]
        expected_val = tc["validate_value"]
        with step(f"Assert every post.{field} == {expected_val}"):
            assert len(data) > 0, "Expected at least 1 post"
            for post in data:
                assert post[field] == expected_val, (
                    f"Post id={post['id']} has {field}={post[field]}"
                )

    elif assert_type == "schema_batch":
        with step(f"Validate each of {len(data)} posts against schema"):
            failures = []
            for post in data:
                try:
                    assert_valid_schema(post, POST_SCHEMA,
                                        description=f"id={post.get('id')}")
                except AssertionError as exc:
                    failures.append(str(exc))
            if failures:
                pytest.fail(
                    f"{len(failures)}/{len(data)} posts failed:\n"
                    + "\n".join(failures)
                )
            note(f"All {len(data)} posts passed schema validation")
