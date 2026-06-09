# Requirements Specification — SauceDemo

> **System Under Test**: [SauceDemo](https://www.saucedemo.com/) — a standard e-commerce website
>
> **Methodology**: These requirements are reverse-engineered from existing automated tests, with acceptance criteria written in EARS (Easy Approach to Requirements Syntax) style.

---

## Requirements Organization

| Module | Document | Reqs | Description |
|--------|----------|------|-------------|
| Authentication | [REQ-AUTH.md](REQ-AUTH.md) | 6 | Login/logout, credential validation, error display, GUI rendering |
| Inventory | [REQ-INVENTORY.md](REQ-INVENTORY.md) | 8 | Product listing, sorting, data integrity, cart badge |
| Cart | [REQ-CART.md](REQ-CART.md) | 5 | Item add/remove, state persistence, empty state, checkout entry |
| Checkout | [REQ-CHECKOUT.md](REQ-CHECKOUT.md) | 5 | E2E purchase flow, form validation, cancel & return |

---

## Priority Definitions

| Priority | Meaning |
|----------|---------|
| **BLOCKER** | Core path blocked — user cannot complete a fundamental operation |
| **CRITICAL** | Key feature defect — impacts user experience but has a workaround |
| **NORMAL** | General function — does not affect the critical path |
| **MINOR** | Edge case or experience polish |

---

## Requirements Traceability

See the full requirements → test traceability matrix at [traceability-matrix.md](traceability-matrix.md).

---

## Test Framework Coverage

| Framework | Coverage Status |
|-----------|----------------|
| Playwright + pytest | ✅ 27 test cases — full coverage |
| Selenium + pytest | ✅ 25 test cases — full coverage |
| Robot Framework | ✅ 24 test cases — full coverage |
