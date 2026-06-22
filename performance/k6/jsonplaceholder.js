/**
 * Performance / load test — JSONPlaceholder REST API.
 *
 * Same 5 scenarios as the Locust and JMeter counterparts,
 * implemented in idiomatic k6 with constant-arrival-rate executors
 * and threshold-based pass/fail criteria.
 *
 * Target: https://jsonplaceholder.typicode.com
 *
 * Run headless with HTML report
 * -----------------------------
 *   cd performance/k6
 *   k6 run jsonplaceholder.js
 *
 * Output files
 * ------------
 *   report.html   — standalone HTML (charts, checks, thresholds)
 *   summary.json  — raw metrics for CI / post-processing
 *
 * Dependencies (all loaded at runtime — no npm install needed)
 * -------------------------------------------------------------
 *   k6-reporter (benc-uk) — embedded in handleSummary()
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

// ── Custom metrics (one Trend per endpoint for thresholding) ──
const getUsersDuration    = new Trend('get_users_duration');
const getPostsDuration    = new Trend('get_posts_duration');
const getUserDuration     = new Trend('get_user_duration');
const filterPostsDuration = new Trend('filter_posts_duration');
const createPostDuration  = new Trend('create_post_duration');
const errors              = new Rate('errors');

const BASE = 'https://jsonplaceholder.typicode.com';

// ═══════════════════════════════════════════════════════════════
//  Configuration
// ═══════════════════════════════════════════════════════════════

export const options = {
  // 5 independent scenarios — one per endpoint.
  // Arrival rates mirror Locust task weights (3 : 3 : 2 : 2 : 1).
  // Pre-allocated VUs ≈ arrival rate so each scenario has dedicated
  // capacity; total VU footprint ≈ 11 (close to the 10-user baseline).
  scenarios: {
    list_users: {
      executor: 'constant-arrival-rate',
      rate: 3,
      timeUnit: '1s',
      duration: '55s',
      preAllocatedVUs: 3,
      exec: 'listUsers',
    },
    list_posts: {
      executor: 'constant-arrival-rate',
      rate: 3,
      timeUnit: '1s',
      duration: '55s',
      preAllocatedVUs: 3,
      exec: 'listPosts',
    },
    get_user: {
      executor: 'constant-arrival-rate',
      rate: 2,
      timeUnit: '1s',
      duration: '55s',
      preAllocatedVUs: 2,
      exec: 'getUser',
    },
    filter_posts: {
      executor: 'constant-arrival-rate',
      rate: 2,
      timeUnit: '1s',
      duration: '55s',
      preAllocatedVUs: 2,
      exec: 'filterPosts',
    },
    create_post: {
      executor: 'constant-arrival-rate',
      rate: 1,
      timeUnit: '1s',
      duration: '55s',
      preAllocatedVUs: 1,
      exec: 'createPost',
    },
  },

  // Thresholds map to REQ-PERF-001 through REQ-PERF-004.
  // When a threshold is breached k6 exits non-zero → CI catches it.
  thresholds: {
    // REQ-PERF-001: < 1 % failure rate
    'errors':              ['rate < 0.01'],

    // REQ-PERF-002: read-latency P95 ≤ 1500 ms
    'get_users_duration':  ['p(95) < 1500'],
    'get_posts_duration':  ['p(95) < 1500'],
    'get_user_duration':   ['p(95) < 1500'],
    'filter_posts_duration': ['p(95) < 1500'],

    // REQ-PERF-003: write-latency P95 ≤ 2000 ms
    'create_post_duration': ['p(95) < 2000'],

    // REQ-PERF-004: overall ceiling (2× baseline guard)
    'http_req_duration':   ['p(95) < 2500'],
  },
};

// ═══════════════════════════════════════════════════════════════
//  Helpers
// ═══════════════════════════════════════════════════════════════

/**
 * Record a request result: push duration into the per-endpoint Trend,
 * run a status-code check, and sleep for the think-time window
 * (0.6–1.2 s, matching Locust's ``wait_time = between(0.6, 1.2)``).
 */
function record(res, trend, expectedStatus) {
  trend.add(res.timings.duration);
  const ok = check(res, {
    [`status is ${expectedStatus}`]: (r) => r.status === expectedStatus,
  });
  errors.add(!ok);
  sleep(0.6 + Math.random() * 0.6);
}

// ═══════════════════════════════════════════════════════════════
//  Scenarios — one exported function per endpoint
// ═══════════════════════════════════════════════════════════════

export function listUsers() {
  record(http.get(`${BASE}/users`), getUsersDuration, 200);
}

export function listPosts() {
  record(http.get(`${BASE}/posts`), getPostsDuration, 200);
}

export function getUser() {
  const uid = Math.floor(Math.random() * 10) + 1;
  record(http.get(`${BASE}/users/${uid}`), getUserDuration, 200);
}

export function filterPosts() {
  const uid = Math.floor(Math.random() * 10) + 1;
  record(http.get(`${BASE}/posts?userId=${uid}`), filterPostsDuration, 200);
}

export function createPost() {
  const payload = JSON.stringify({
    userId: 1,
    title: 'perf test',
    body: 'load test post',
  });
  const params = { headers: { 'Content-Type': 'application/json' } };
  record(http.post(`${BASE}/posts`, payload, params), createPostDuration, 201);
}

// ═══════════════════════════════════════════════════════════════
//  Summary — HTML report + JSON export
// ═══════════════════════════════════════════════════════════════

export function handleSummary(data) {
  return {
    'stdout': JSON.stringify(data.metrics, null, 2),
    'summary.json': JSON.stringify(data, null, 2),
    'report.html': htmlReport(data),
  };
}
