# REQ-PERF: API Performance — Load & Stress Baseline

> **Module**: JSONPlaceholder REST API — `https://jsonplaceholder.typicode.com`
>
> **Tools**: [Locust](https://locust.io/), [Apache JMeter](https://jmeter.apache.org/),
> [Grafana k6](https://k6.io/) — three performance testing philosophies side-by-side
>
> **Why three tools**: The same 5 JSONPlaceholder scenarios are implemented in three
> frameworks to demonstrate tool selection rationale:
>
> | Tool | Philosophy | Best For |
> |------|-----------|----------|
> | **Locust** | Pure Python, code-as-test (`locustfile.py`) | Dev-owned scripts, Python ecosystem |
> | **JMeter** | XML test plan, GUI editor, enterprise standard | Legacy migration, test-ops team handoff |
> | **K6** | JavaScript, CLI-native, Grafana Cloud ready | Greenfield, CI/CD integration, cloud scale |
>
> All three target the same endpoints with the same load profile
> (10 users, 2/s ramp-up, 60s duration, 0.6–1.2s think time), making
> their output directly comparable — apples-to-apples across paradigms.

---

## REQ-PERF-001: Baseline throughput — 10 concurrent users sustain ≥ 5 RPS with zero failures

- **Priority**: CRITICAL
- **Type**: Non-Functional · Performance
- **Precondition**: JSONPlaceholder API is reachable
- **Acceptance Criteria**:
  1. Given 10 simulated concurrent users with `wait_time = between(0.6, 1.2)` → When running a 60-second load test against `/users`, `/posts`, and `/posts?userId={id}` endpoints → Then the aggregate throughput is ≥ 5 requests per second
  2. Given the same test conditions → When the 60-second run completes → Then the failure rate is 0 % (no 5xx errors; sporadic network timeouts ≤ 1 % acceptable)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | locust | TC-PERF-001 | performance/locust/locustfile.py | ✅ |
  | JMeter | TC-PERF-001 | performance/jmeter/jsonplaceholder.jmx | ✅ |
  | K6 | TC-PERF-001 | performance/k6/jsonplaceholder.js | ✅ |

---

## REQ-PERF-002: Read latency P95 ≤ 1500 ms

- **Priority**: CRITICAL
- **Type**: Non-Functional · Performance
- **Precondition**: API under normal load (10 concurrent users)
- **Acceptance Criteria**:
  1. Given `GET /users`, `GET /users/{id}`, `GET /posts`, and `GET /posts?userId={id}` endpoints → When measured over a 60-second load test → Then the 95th percentile response time for each read endpoint is ≤ 1500 ms
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | locust | TC-PERF-002 | performance/locust/locustfile.py | ✅ |
  | JMeter | TC-PERF-002 | performance/jmeter/jsonplaceholder.jmx | ✅ |
  | K6 | TC-PERF-002 | performance/k6/jsonplaceholder.js | ✅ |

---

## REQ-PERF-003: Write latency P95 ≤ 2000 ms

- **Priority**: NORMAL
- **Type**: Non-Functional · Performance
- **Precondition**: API under normal load
- **Acceptance Criteria**:
  1. Given `POST /posts` with a valid JSON payload → When measured over a 60-second load test → Then the 95th percentile response time is ≤ 2000 ms (writes to JSONPlaceholder are echoed but not persisted — they are expected to be faster than real database writes)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | locust | TC-PERF-003 | performance/locust/locustfile.py | ✅ |
  | JMeter | TC-PERF-003 | performance/jmeter/jsonplaceholder.jmx | ✅ |
  | K6 | TC-PERF-003 | performance/k6/jsonplaceholder.js | ✅ |

---

## REQ-PERF-004: No degradation at 2× baseline load

- **Priority**: NORMAL
- **Type**: Non-Functional · Stress
- **Precondition**: JSONPlaceholder is reachable; we are mindful of the free-tier ~100 req/min ceiling
- **Acceptance Criteria**:
  1. Given 20 concurrent users (double the baseline) → When running a 30-second stress test → Then the failure rate remains ≤ 5 % and the median response time does not exceed 2× the baseline median
  2. **Note**: This test intentionally pushes closer to the free-tier limit. It is a stress smoke test, not a sustained load test.
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | locust | TC-PERF-004 | performance/locust/locustfile.py | ✅ |
  | JMeter | TC-PERF-004 | performance/jmeter/jsonplaceholder.jmx | ✅ |
  | K6 | TC-PERF-004 | performance/k6/jsonplaceholder.js | ✅ |

---

## REQ-PERF-005: Test report is human-readable and CI-friendly

- **Priority**: NORMAL
- **Type**: Non-Functional · Observability
- **Precondition**: A locust test run has completed
- **Acceptance Criteria**:
  1. Given a completed headless run → Then an HTML report (`report.html`) is generated containing:
     - Request statistics table (endpoint, #requests, #failures, median/P95/P99 response times, RPS)
     - Response time distribution chart
     - Aggregate throughput (RPS) graph
  2. Given the `run_report.bat` / `run_report.sh` script → When executed → Then it runs the default baseline test and prints the report path to stdout
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | locust | TC-PERF-005 | performance/locust/run_report.sh | ✅ |
  | JMeter | TC-PERF-005 | performance/jmeter/run_report.sh | ✅ |
  | K6 | TC-PERF-005 | performance/k6/run_report.sh | ✅ |
