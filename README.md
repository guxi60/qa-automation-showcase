# QA Automation Showcase

> **One system under test, three automation frameworks — a side-by-side comparison demonstrating tool selection rationale and technology migration capability.**
>
> System under test: [SauceDemo](https://www.saucedemo.com/) (standard e-commerce flow: Login → Browse → Cart → Checkout)

---

## 🎯 Motivation

The motivation is simple: **which test framework should you choose for a given context?** Instead of giving a hand-wavy answer in an interview, let the code speak for itself.

The same SauceDemo e-commerce site, tested end-to-end with three frameworks built on fundamentally different philosophies:

| Framework | Design Philosophy | Best For |
|-----------|-------------------|----------|
| **Selenium + pytest** | WebDriver standard protocol, broadest browser support | Cross-browser compatibility, traditional enterprise projects |
| **Robot Framework** | Keyword-driven, lowers the barrier for non-technical stakeholders | Cross-role collaboration, BDD-style teams |
| **Playwright + pytest** | Modern design, built-in auto-wait, trace viewer, parallelism | Fast-iterating web apps, greenfield projects |

Each framework has its own POM implementation, test cases, and network resilience strategy. You can directly compare how they handle the exact same scenarios.

---

## 🧰 Tech Stack

```
Web UI Testing:  Selenium  |  Playwright  |  Robot Framework
API Testing:     pytest + requests  |  JSON Schema Validation

Performance:     locust
CI/CD:           GitHub Actions
Lang:            Python 3.x
Reports:         Allure  |  [Live Report ↗](https://guxi60.github.io/qa-automation-showcase/#)
```

---

## 📊 Live Allure Report

[![Allure Report](https://img.shields.io/badge/Allure-Report-ff69b4?logo=java)](https://guxi60.github.io/qa-automation-showcase/#)

> Frozen snapshot of the latest Playwright run — 24 tests with screenshots, severity, and traceability tags.

Open [**guxi60.github.io/qa-automation-showcase**](https://guxi60.github.io/qa-automation-showcase/#) to browse the report without running anything locally.

---

## 📁 Project Structure

```
qa-automation-showcase/
├── docs/requirements/            # Requirements specs & traceability matrix
│   ├── README.md                 # Methodology overview
│   ├── REQ-AUTH.md               # Authentication requirements (6)
│   ├── REQ-INVENTORY.md          # Inventory requirements (8)
│   ├── REQ-CART.md               # Cart requirements (5)
│   ├── REQ-CHECKOUT.md           # Checkout requirements (5)
│   └── traceability-matrix.md    # Requirements Traceability Matrix (RTM)
├── web-ui-tests/                # Playwright + pytest (modern)
│   ├── pages/                   # Page Object Model
│   ├── tests/                   # Test cases
│   ├── test_data/               # Test data (shared with Selenium)
│   └── conftest.py              # Fixtures & config
├── selenium-tests/              # Selenium + pytest (classic)
│   ├── pages/                   # Page Object Model
│   ├── tests/                   # Test cases
│   └── conftest.py              # Fixtures & config
├── robot-tests/                 # Robot Framework (keyword-driven)
│   ├── resources/               # Shared keywords & page objects
│   └── tests/                   # .robot test files
├── api-tests/                   # API tests
│   ├── tests/                   # API test cases
│   └── schemas/                 # JSON Schema definitions
├── performance/                 # locust performance tests
├── .github/workflows/           # GitHub Actions CI
└── requirements.txt             # Python dependencies
```

---

## 🚀 Quick Start

> 💡 **Don't want to install anything?** Browse the [hosted Allure report](https://guxi60.github.io/qa-automation-showcase/#) — frozen snapshot of the latest Playwright run with 24 tests, screenshots, and traceability metadata.

```bash
# 1. Clone
git clone https://github.com/guxi60/qa-automation-showcase.git
cd qa-automation-showcase

# 2. Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# 3. Run Playwright tests (Allure report)
cd web-ui-tests
pytest -v
allure generate allure-results -o allure-report --clean
allure open allure-report

# 4. Run Selenium tests (Allure report)
cd ../selenium-tests
pytest -v
allure generate allure-results -o allure-report --clean
allure open allure-report

# 5. Run Robot Framework tests (Allure report)
cd ../robot-tests
robot --listener allure_robotframework:allure-results --pythonpath resources tests/
allure generate allure-results -o allure-report --clean
allure open allure-report

# 6. Run API tests
cd api-tests
pytest -v
```

---

## 📊 Test Coverage Matrix

| Feature | Playwright | Selenium | Robot Framework | API | Performance |
|---------|-----------|----------|-----------------|-----|-------------|
| Login (happy/negative/boundary) | ✅ (6) | ✅ (6) | ✅ (6) | — | — |
| Inventory (sort/display/images) | ✅ (8) | ✅ (8) | ✅ (8) | — | — |
| Cart (add/remove/persistence) | ✅ (5) | ✅ (5) | ✅ (5) | — | — |
| Checkout E2E (incl. validation) | ✅ (5) | ✅ (5) | ✅ (5) | — | — |
| User CRUD | — | — | — | ✅ (7) | — |
| Post CRUD | — | — | — | ✅ (7) | — |
| Schema validation | — | — | — | ✅ | — |
| Performance / Load | — | — | — | — | ✅ (5 scenarios) |

---

## 📋 Requirements-Driven Testing

This project follows the TDD closed-loop methodology: **Requirements Spec → Test Design → Automation → Traceability**.

### Requirements Documentation

Each module has a corresponding requirements specification in [docs/requirements/](docs/requirements/):

| Document | Reqs | Description |
|----------|------|-------------|
| [REQ-AUTH.md](docs/requirements/REQ-AUTH.md) | 6 | Login, credential validation, error messages |
| [REQ-INVENTORY.md](docs/requirements/REQ-INVENTORY.md) | 8 | Product display, sorting, data integrity |
| [REQ-CART.md](docs/requirements/REQ-CART.md) | 5 | Cart add/remove, state persistence |
| [REQ-CHECKOUT.md](docs/requirements/REQ-CHECKOUT.md) | 5 | E2E purchase flow, form validation |
| [REQ-API-USERS.md](docs/requirements/REQ-API-USERS.md) | 7 | User CRUD — list / single / create / update / delete / 404 / schema |
| [REQ-API-POSTS.md](docs/requirements/REQ-API-POSTS.md) | 7 | Post CRUD — list / single / create / update / delete / filter / schema |
| [REQ-PERF.md](docs/requirements/REQ-PERF.md) | 5 | Load & stress baseline — throughput, latency, report |

### Requirements Traceability Matrix

The [RTM](docs/requirements/traceability-matrix.md) ensures every requirement maps to automated test cases, cross-validated across multiple frameworks.

```text
Requirements (REQ-*.md)
  ├── Web UI: Test Data (test_data/*.yaml ↔ *.json) → Playwright ✅ (24)
  │                                                   → Selenium    ✅ (24)
  │                                                   → Robot       ✅ (24)
  ├── API:    Test Data (test_data/*.yaml)           → pytest+requests ✅ (14)
  └── Perf:   locustfile.py                          → locust ✅ (5 scenarios)
```

---

## 🧪 Testing Principles

1. **Readability First** — Test cases read like scenario descriptions, not code dumps
2. **Failure Traceability** — Automatic screenshots on every failure; no reproduction needed to pinpoint issues
3. **Data–Logic Separation** — Test data lives independently from test code, making maintenance and reuse straightforward
4. **Cross-Framework Comparison** — Same scenarios implemented with different frameworks provide real-world reference for tool selection
5. **Network Resilience** — Built-in navigation timeouts and retry mechanisms for unstable network conditions

---

## 👤 About the Author

**Gu Xiang** | Senior QA Engineer | 15+ years of testing experience

- Proficient in Selenium / Robot Framework / Playwright / locust
- Former QA Lead / Scrum Master, leading cross-timezone testing teams
- Cross-industry delivery experience — from CT medical imaging to Web3 digital wallets
- Passionate about engineering the intersection of AI + test automation

📧 guxi60@outlook.com
