"""API test fixtures — rate-limited HTTP client, Allure integration, DDT + Schema.

Target: JSONPlaceholder (https://jsonplaceholder.typicode.com) — a free
fake REST API for testing and prototyping.  We treat it as the mock API
layer behind the SauceDemo e-commerce front-end, exercising the same
CRUD operations (Users, Posts) that a real backend would expose.

Rate-limit guard: enforces a minimum interval between requests so we never
hammer the free tier.  Adjust MIN_INTERVAL if the API starts returning 429s.
"""

from __future__ import annotations

import time
import json
import pytest
import allure
import requests
from pathlib import Path
from jsonschema import validate, ValidationError

BASE_URL = "https://jsonplaceholder.typicode.com"
SCHEMA_DIR = Path(__file__).parent / "schemas"

# ── Rate-limit guard ────────────────────────────────────────────
# JSONPlaceholder is a free service shared by thousands of developers.
# Keep this at >= 0.6 s to stay well within the unofficial ~100 req/min
# ceiling.  If you see 429 Too Many Requests, bump it to 1.0 s.
MIN_INTERVAL = 0.6  # seconds


class RateLimitedSession:
    """Thin wrapper around ``requests.Session`` that enforces a minimum
    interval between outgoing HTTP requests.

    Usage is identical to ``requests.Session`` — call ``.get()``,
    ``.post()``, ``.put()``, ``.delete()``, or the generic ``.request()``.
    """

    def __init__(self, min_interval: float = MIN_INTERVAL) -> None:
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "qa-automation-showcase/1.0 (API test suite)",
        })
        self._min_interval = min_interval
        self._last_request = 0.0

    # -- internal -------------------------------------------------

    def _throttle(self) -> None:
        """Sleep if the previous request was less than *min_interval* ago."""
        gap = time.time() - self._last_request
        if gap < self._min_interval:
            time.sleep(self._min_interval - gap)

    # -- public HTTP verbs ----------------------------------------

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        self._throttle()
        resp = self._session.request(method, url, **kwargs)
        self._last_request = time.time()
        return resp

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

    def close(self) -> None:
        self._session.close()


# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def api() -> RateLimitedSession:
    """Session-scoped rate-limited HTTP client (JSONPlaceholder)."""
    client = RateLimitedSession()
    yield client
    client.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL of the JSONPlaceholder API."""
    return BASE_URL


@pytest.fixture
def report(request):
    """Attach full HTTP request + response details to Allure.

    Usage inside a test::

        resp = api.get(f"{base_url}/users")
        report(resp)   # ← attaches REQUEST + RESPONSE to Allure

    On test failure the last stored response is re-attached to the
    failure report for quick debugging.
    """
    from api_reporter import report as _report

    def _track(resp: requests.Response) -> None:
        _report(resp, node=request.node)

    return _track


# ── Schema helpers ──────────────────────────────────────────────

def load_schema(filename: str) -> dict:
    """Load a JSON Schema definition from ``api-tests/schemas/``."""
    path = SCHEMA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def assert_valid_schema(instance: dict, schema: dict,
                        description: str = "") -> None:
    """Validate *instance* against *schema*; raise AssertionError on failure."""
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as exc:
        allure.attach(
            json.dumps(instance, indent=2, ensure_ascii=False),
            name=f"offending payload ({description})",
            attachment_type=allure.attachment_type.JSON,
        )
        raise AssertionError(
            f"Schema validation failed [{description}]: {exc.message}"
        ) from exc


# ── Allure: attach last response on failure ─────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """When a test fails, re-attach the stored response body for the
    failure report so the user sees exactly what the API returned."""
    outcome = yield
    report_result = outcome.get_result()
    if report_result.when == "call" and report_result.failed:
        resp = getattr(item, "_last_response", None)
        if resp is not None:
            try:
                body = json.dumps(resp.json(), indent=2, ensure_ascii=False)
            except Exception:
                body = resp.text[:4000]
            allure.attach(
                body,
                name=f"FAILURE — API Response ({resp.status_code})",
                attachment_type=allure.attachment_type.JSON,
            )


# ── Allure: environment info ────────────────────────────────────

def pytest_sessionfinish(session) -> None:
    """Write environment.properties showing API-target metadata."""
    env_dir = Path("allure-results")
    env_dir.mkdir(exist_ok=True)
    (env_dir / "environment.properties").write_text(
        "API.Base.URL=https://jsonplaceholder.typicode.com\n"
        "API.Rate.Limit.Interval=0.6s\n"
        "Schema.Draft=Draft 7\n"
        "Language=Python 3\n"
        "Framework=pytest + requests + jsonschema\n",
        encoding="utf-8",
    )


# ── Markers ─────────────────────────────────────────────────────

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: P0 critical-path API tests")
    config.addinivalue_line("markers", "regression: full API regression suite")
    config.addinivalue_line("markers", "schema: JSON Schema validation tests")
    config.addinivalue_line("markers", "crud: Create / Read / Update / Delete")
