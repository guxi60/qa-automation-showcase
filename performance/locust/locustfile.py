"""
Performance / load test — JSONPlaceholder REST API.

Simulates realistic e-commerce backend traffic patterns:
- Browse users / posts (read-heavy, 60 % of traffic)
- View details (20 %)
- Write (10 %)

Target: https://jsonplaceholder.typicode.com
Rate-limit guard: ``wait_time = between(0.6, 1.2)`` keeps per-user
request rate well within the free tier ceiling (~100 req/min total).

Run headless with HTML report
-----------------------------
    cd performance/locust
    locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html report.html

- ``-u 10``   — peak 10 concurrent simulated users
- ``-r 2``    — spawn 2 users / second
- ``-t 60s``  — run for 60 seconds

Open the web UI (interactive mode)
-----------------------------------
    locust -f locustfile.py
    # then open http://localhost:8089
"""

from locust import HttpUser, task, between
from random import randint

BASE = "https://jsonplaceholder.typicode.com"


class JSONPlaceholderUser(HttpUser):
    """Simulated user browsing a RESTful e-commerce API."""

    host = BASE
    wait_time = between(0.6, 1.2)

    # ── Read ─────────────────────────────────────────────────

    @task(3)
    def list_users(self):
        """Browse all users (high-frequency read)."""
        with self.client.get("/users", name="GET /users", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"Expected 200, got {r.status_code}")
            elif not isinstance(r.json(), list):
                r.failure("Response is not a JSON array")

    @task(2)
    def get_user(self):
        """View a single user by id."""
        uid = randint(1, 10)
        with self.client.get(f"/users/{uid}", name="GET /users/{id}", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"Expected 200, got {r.status_code}")

    @task(3)
    def list_posts(self):
        """Browse all posts (high-frequency read)."""
        with self.client.get("/posts", name="GET /posts", catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f"Expected 200, got {r.status_code}")

    @task(2)
    def filter_posts(self):
        """Filter posts by a specific user."""
        uid = randint(1, 10)
        with self.client.get(
            "/posts", params={"userId": uid}, name="GET /posts?userId={id}", catch_response=True
        ) as r:
            if r.status_code != 200:
                r.failure(f"Expected 200, got {r.status_code}")

    # ── Write ────────────────────────────────────────────────

    @task(1)
    def create_post(self):
        """Create a new post (low-frequency write)."""
        payload = {"userId": 1, "title": "perf test", "body": "load test post"}
        with self.client.post(
            "/posts", json=payload, name="POST /posts", catch_response=True
        ) as r:
            if r.status_code != 201:
                r.failure(f"Expected 201, got {r.status_code}")
