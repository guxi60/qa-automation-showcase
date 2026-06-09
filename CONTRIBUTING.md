# Contributing

> How to add requirements, test cases, and frameworks while maintaining the TDD closed loop across all three frameworks.

---

## Project Constants (do not break these)

| Rule | Detail |
|------|--------|
| **Shared test data** | All three frameworks consume `web-ui-tests/test_data/*.json` — never duplicate test data per framework |
| **TC-ID naming** | `TC-{MODULE}-{NNN}` (e.g. `TC-LOGIN-001`, `TC-CHK-003`). Unique across the project |
| **TC count parity** | Every requirement → exactly 1 TC-ID → exactly 1 test function/case per framework |
| **Allure everywhere** | All frameworks produce `allure-results/` → `allure-report/`, with branded `environment.properties` |
| **One browser** | All frameworks reuse Playwright's bundled Chromium (same binary, same version) |

---

## TDD Closed-Loop Process

```
  1. Write Requirement (REQ-*.md)
         │
  2. Add Test Data  (test_data/*.json)
         │
  3. Implement Test  (all three frameworks)
         │
  4. Run & Verify    (24/24 per framework)
         │
  5. Update Docs     (RTM, README, framework coverage)
```

**Each step is mandatory.** Skipping a step breaks traceability.

---

## Adding a New Requirement

### Step 1: Write the requirement spec

In `docs/requirements/REQ-{MODULE}.md` (or create a new file):

```markdown
## REQ-XXX-NNN: Title

- **Priority**: BLOCKER | CRITICAL | NORMAL | MINOR
- **Type**: Functional | GUI | E2E | Validation | ...
- **Precondition**: ...
- **Acceptance Criteria**:
  1. Given ... When ... Then ...
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-XXX-NNN | test_file.py | ✅ |
  | Selenium | TC-XXX-NNN | test_file.py | ✅ |
  | Robot Framework | TC-XXX-NNN | file.robot | ✅ |
```

### Step 2: Add test data

In `web-ui-tests/test_data/{module}.json`, add a JSON entry with at least `id`, `title`, `severity`, `tags`.

The JSON is read by:
- **Playwright / Selenium**: `load_data()` → `@pytest.mark.parametrize`
- **Robot Framework**: `resources/test_data.py` → Python variable file

### Step 3: Implement in three frameworks

| Framework | Test file | DDT mechanism | Metadata |
|-----------|----------|---------------|----------|
| **Playwright** | `web-ui-tests/tests/test_{module}.py` | `@pytest.mark.parametrize("tc", load_data(...))` + `set_meta(tc)` | `@allure.feature(...)` |
| **Selenium** | `selenium-tests/tests/test_{module}.py` | Same pattern as Playwright | Same pattern |
| **Robot Framework** | `robot-tests/tests/{module}.robot` | `[Template]` keyword + data rows *or* standalone keyword-driven test cases | `[Tags]` + `[Documentation]` |

### Step 4: Verify

```bash
# Each framework must pass 100%
cd web-ui-tests && pytest -v          # expect all green
cd selenium-tests && pytest -v         # expect all green
cd robot-tests && robot --pythonpath resources tests/  # expect all green
```

### Step 5: Update docs

- [ ] `docs/requirements/REQ-{MODULE}.md` — add Linked Test Cases row for all three frameworks
- [ ] `docs/requirements/traceability-matrix.md` — add row with `TC-XXX-NNN` for Playwright, Selenium, Robot columns
- [ ] `docs/requirements/README.md` — update requirement count if new module
- [ ] `README.md` — update Test Coverage Matrix

---

## Adding a New Framework

If you add a fourth framework (e.g. Cypress, TestCafe):

### File structure convention

```
{framework}-tests/
├── pages/          (or resources/ for Robot-style)
├── tests/          (test files)
├── conftest.py     (if pytest-based)
└── allure-results/ (generated, gitignored)
```

### Checklist

1. **Consume shared test data** — read from `web-ui-tests/test_data/`, don't copy or fork
2. **Match TC-IDs** — use the same `TC-XXX-NNN` identifiers as the other frameworks
3. **Allure output** — produce `allure-results/` with `environment.properties` (brand the Framework name)
4. **Same browser** — reuse Playwright's Chromium binary
5. **Update RTM** — add a column for the new framework
6. **Update README** — add to Test Coverage Matrix and Quick Start
7. **Update all REQ-*.md files** — add Linked Test Cases row for the new framework
8. **Run all three existing suites** first to confirm no regressions

---

## Documentation Consistency Rules

These files must stay in sync. When you change any one, verify the others:

| File | What it tracks | Updated when |
|------|---------------|--------------|
| `docs/requirements/REQ-*.md` | Per-requirement acceptance criteria + per-framework linked test cases | New requirement added |
| `docs/requirements/traceability-matrix.md` | Full RTM: every requirement × every framework with TC-IDs | New requirement or new framework |
| `docs/requirements/README.md` | Requirements overview + framework coverage table | New framework or count change |
| `README.md` | Test Coverage Matrix, Quick Start, project-level overview | Any change to frameworks or modules |
| `CONTRIBUTING.md` | This file | Process changes |

**Self-check after any change**: `grep` for old TC count numbers across all `.md` files — they must agree.

---

## DDT Conventions by Framework

| Framework | DDT Approach | Data Source |
|-----------|-------------|-------------|
| **Playwright + pytest** | `@pytest.mark.parametrize("tc", load_data(file)["key"])` → `set_meta(tc)` inside test | `test_data/*.json` |
| **Selenium + pytest** | Identical to Playwright (same `load_data`, same `set_meta`) | Same JSON |
| **Robot Framework** | `[Template]` keyword with data arguments per test case; also standalone keyword-driven tests for unique flows | `test_data.py` (Python var file reads JSON) |

**When to use template DDT vs. standalone test in Robot:**
- Validation / negative tests that share the same step sequence → `[Template]`
- Unique flow tests (E2E, persistence, GUI checks) → standalone keyword-driven test case

---

## Reporting Consistency

All frameworks produce Allure reports with distinct branding:

| Framework | `environment.properties` |
|-----------|-------------------------|
| Playwright | `Framework=Pytest + Playwright` / `Browser=Chromium (Playwright)` |
| Selenium | `Framework=Selenium + pytest` / `Browser=Chrome (Selenium WebDriver)` |
| Robot Framework | `Framework=Robot Framework + SeleniumLibrary` / `Browser=Chrome (Robot Framework - SeleniumLibrary)` |

Command to run + generate report in one shot:

```bash
# Playwright
cd web-ui-tests && pytest -v && allure generate allure-results -o allure-report --clean

# Selenium
cd selenium-tests && pytest -v && allure generate allure-results -o allure-report --clean

# Robot Framework
cd robot-tests && robot --listener allure_robotframework:allure-results --pythonpath resources tests/ && allure generate allure-results -o allure-report --clean
```
