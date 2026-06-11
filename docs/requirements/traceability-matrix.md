# Requirements Traceability Matrix (RTM)

> **Purpose**: Track the mapping of every requirement → test case, ensuring 100% requirements coverage.
>
> **Legend**: ✅ Implemented · ⬜ To be implemented · — Not applicable

---

## Coverage Overview

| Module | Reqs | Playwright | Selenium | Robot Framework | API | Performance |
|--------|------|------------|----------|-----------------|-----|-------------|
| AUTH | 6 | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ | — | — |
| INVENTORY | 8 | 8/8 ✅ | 8/8 ✅ | 8/8 ✅ | — | — |
| CART | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | — | — |
| CHECKOUT | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ | — | — |
| API-USERS | 7 | — | — | — | 7/7 ✅ | — |
| API-POSTS | 7 | — | — | — | 7/7 ✅ | — |
| PERF | 5 | — | — | — | — | 5/5 ✅ |
| **Total** | **43** | **24/24 (100%)** | **24/24 (100%)** | **24/24 (100%)** | **14/14 (100%)** | **5/5 (100%)** |

---

## Detailed Traceability

### AUTH — Authentication

| Req ID | Description | Priority | Playwright | Selenium | Robot |
|--------|------------|----------|------------|----------|-------|
| [REQ-AUTH-001](REQ-AUTH.md#req-auth-001-successful-login-with-valid-credentials) | Valid credentials login | BLOCKER | TC-LOGIN-001 ✅ | TC-LOGIN-001 ✅ | TC-LOGIN-001 ✅ |
| [REQ-AUTH-002](REQ-AUTH.md#req-auth-002-wrong-password-rejected) | Wrong password rejected | CRITICAL | TC-LOGIN-002 ✅ | TC-LOGIN-002 ✅ | TC-LOGIN-002 ✅ |
| [REQ-AUTH-003](REQ-AUTH.md#req-auth-003-empty-username-rejected) | Empty username rejected | CRITICAL | TC-LOGIN-003 ✅ | TC-LOGIN-003 ✅ | TC-LOGIN-003 ✅ |
| [REQ-AUTH-004](REQ-AUTH.md#req-auth-004-empty-password-rejected) | Empty password rejected | CRITICAL | TC-LOGIN-004 ✅ | TC-LOGIN-004 ✅ | TC-LOGIN-004 ✅ |
| [REQ-AUTH-005](REQ-AUTH.md#req-auth-005-locked-out-account-denied-access) | Locked-out account denied | CRITICAL | TC-LOGIN-005 ✅ | TC-LOGIN-005 ✅ | TC-LOGIN-005 ✅ |
| [REQ-AUTH-006](REQ-AUTH.md#req-auth-006-login-page-gui-elements-render-correctly) | Login page GUI elements | BLOCKER | TC-LOGIN-006 ✅ | TC-LOGIN-006 ✅ | TC-LOGIN-006 ✅ |

### INVENTORY — Product Inventory

| Req ID | Description | Priority | Playwright | Selenium | Robot |
|--------|------------|----------|------------|----------|-------|
| [REQ-INV-001](REQ-INVENTORY.md#req-inv-001-product-listing-displays-6-items) | 6 products displayed | BLOCKER | TC-INV-001 ✅ | TC-INV-001 ✅ | TC-INV-001 ✅ |
| [REQ-INV-002](REQ-INVENTORY.md#req-inv-002-product-data-integrity-name--price) | Data integrity (name+price) | CRITICAL | TC-INV-002 ✅ | TC-INV-002 ✅ | TC-INV-002 ✅ |
| [REQ-INV-003](REQ-INVENTORY.md#req-inv-003-product-images-load-correctly) | Product images load | CRITICAL | TC-INV-003 ✅ | TC-INV-003 ✅ | TC-INV-003 ✅ |
| [REQ-INV-004](REQ-INVENTORY.md#req-inv-004-product-sorting-4-sort-options) | Sort (4 options) | CRITICAL | TC-INV-004 ✅ | TC-INV-004 ✅ | TC-INV-004 ✅ |
| [REQ-INV-005](REQ-INVENTORY.md#req-inv-005-price-sort-is-numerically-correct) | Price sort numerical | MINOR | TC-INV-005 ✅ | TC-INV-005 ✅ | TC-INV-005 ✅ |
| [REQ-INV-006](REQ-INVENTORY.md#req-inv-006-cart-badge-hidden-when-cart-is-empty) | Badge hidden when empty | CRITICAL | TC-INV-006 ✅ | TC-INV-006 ✅ | TC-INV-006 ✅ |
| [REQ-INV-007](REQ-INVENTORY.md#req-inv-007-cart-badge-increments-when-adding-items) | Badge increments | CRITICAL | TC-INV-007 ✅ | TC-INV-007 ✅ | TC-INV-007 ✅ |
| [REQ-INV-008](REQ-INVENTORY.md#req-inv-008-add-then-remove-resets-cart-badge-to-zero) | Add-then-remove resets | NORMAL | TC-INV-008 ✅ | TC-INV-008 ✅ | TC-INV-008 ✅ |

### CART — Shopping Cart

| Req ID | Description | Priority | Playwright | Selenium | Robot |
|--------|------------|----------|------------|----------|-------|
| [REQ-CART-001](REQ-CART.md#req-cart-001-added-items-appear-in-the-cart) | Items appear in cart | BLOCKER | TC-CART-001 ✅ | TC-CART-001 ✅ | TC-CART-001 ✅ |
| [REQ-CART-002](REQ-CART.md#req-cart-002-remove-item-from-cart) | Remove item from cart | CRITICAL | TC-CART-002 ✅ | TC-CART-002 ✅ | TC-CART-002 ✅ |
| [REQ-CART-003](REQ-CART.md#req-cart-003-cart-state-persists-across-page-navigation) | State persists | CRITICAL | TC-CART-003 ✅ | TC-CART-003 ✅ | TC-CART-003 ✅ |
| [REQ-CART-004](REQ-CART.md#req-cart-004-empty-cart-state) | Empty cart state | CRITICAL | TC-CART-004 ✅ | TC-CART-004 ✅ | TC-CART-004 ✅ |
| [REQ-CART-005](REQ-CART.md#req-cart-005-checkout-button-available) | Checkout button available | CRITICAL | TC-CART-005 ✅ | TC-CART-005 ✅ | TC-CART-005 ✅ |

### CHECKOUT — Checkout Flow

| Req ID | Description | Priority | Playwright | Selenium | Robot |
|--------|------------|----------|------------|----------|-------|
| [REQ-CHK-001](REQ-CHECKOUT.md#req-chk-001-complete-e2e-purchase-flow) | E2E purchase flow | BLOCKER | TC-CHK-001 ✅ | TC-CHK-001 ✅ | TC-CHK-001 ✅ |
| [REQ-CHK-002](REQ-CHECKOUT.md#req-chk-002-empty-field-validation--first-name) | Empty field — First Name | CRITICAL | TC-CHK-002 ✅ | TC-CHK-002 ✅ | TC-CHK-002 ✅ |
| [REQ-CHK-003](REQ-CHECKOUT.md#req-chk-003-empty-field-validation--last-name) | Empty field — Last Name | CRITICAL | TC-CHK-003 ✅ | TC-CHK-003 ✅ | TC-CHK-003 ✅ |
| [REQ-CHK-004](REQ-CHECKOUT.md#req-chk-004-empty-field-validation--postal-code) | Empty field — Postal Code | CRITICAL | TC-CHK-004 ✅ | TC-CHK-004 ✅ | TC-CHK-004 ✅ |
| [REQ-CHK-005](REQ-CHECKOUT.md#req-chk-005-cancel-returns-to-cart) | Cancel returns to cart | NORMAL | TC-CHK-005 ✅ | TC-CHK-005 ✅ | TC-CHK-005 ✅ |

### API-USERS — Users CRUD & Schema

| Req ID | Description | Priority | API |
|--------|------------|----------|-----|
| [REQ-API-USERS-001](REQ-API-USERS.md#req-api-users-001-list-all-users-with-correct-count-and-structure) | List all users (10) | BLOCKER | TC-API-USERS-001 ✅ |
| [REQ-API-USERS-002](REQ-API-USERS.md#req-api-users-002-single-user-retrieval-with-json-schema-validation) | Single user + schema | BLOCKER | TC-API-USERS-002 ✅ |
| [REQ-API-USERS-003](REQ-API-USERS.md#req-api-users-003-create-a-new-user-and-verify-echoed-payload) | Create user | BLOCKER | TC-API-USERS-003 ✅ |
| [REQ-API-USERS-004](REQ-API-USERS.md#req-api-users-004-full-update-of-an-existing-user) | Update user | NORMAL | TC-API-USERS-004 ✅ |
| [REQ-API-USERS-005](REQ-API-USERS.md#req-api-users-005-delete-an-existing-user) | Delete user | NORMAL | TC-API-USERS-005 ✅ |
| [REQ-API-USERS-006](REQ-API-USERS.md#req-api-users-006-non-existent-user-returns-404) | 404 negative | MINOR | TC-API-USERS-006 ✅ |
| [REQ-API-USERS-007](REQ-API-USERS.md#req-api-users-007-batch-json-schema-validation-across-all-users) | Batch schema | BLOCKER | TC-API-USERS-007 ✅ |

### API-POSTS — Posts CRUD & Schema

| Req ID | Description | Priority | API |
|--------|------------|----------|-----|
| [REQ-API-POSTS-001](REQ-API-POSTS.md#req-api-posts-001-list-all-posts-with-correct-count-and-structure) | List all posts (100) | BLOCKER | TC-API-POSTS-001 ✅ |
| [REQ-API-POSTS-002](REQ-API-POSTS.md#req-api-posts-002-single-post-retrieval-with-json-schema-validation) | Single post + schema | BLOCKER | TC-API-POSTS-002 ✅ |
| [REQ-API-POSTS-003](REQ-API-POSTS.md#req-api-posts-003-create-a-new-post-and-verify-echoed-payload) | Create post | BLOCKER | TC-API-POSTS-003 ✅ |
| [REQ-API-POSTS-004](REQ-API-POSTS.md#req-api-posts-004-full-update-of-an-existing-post) | Update post | NORMAL | TC-API-POSTS-004 ✅ |
| [REQ-API-POSTS-005](REQ-API-POSTS.md#req-api-posts-005-delete-an-existing-post) | Delete post | NORMAL | TC-API-POSTS-005 ✅ |
| [REQ-API-POSTS-006](REQ-API-POSTS.md#req-api-posts-006-filter-posts-by-user-id) | Filter by userId | NORMAL | TC-API-POSTS-006 ✅ |
| [REQ-API-POSTS-007](REQ-API-POSTS.md#req-api-posts-007-batch-json-schema-validation-across-all-posts) | Batch schema | BLOCKER | TC-API-POSTS-007 ✅ |

### PERF — Performance & Load

| Req ID | Description | Priority | Performance |
|--------|------------|----------|-------------|
| [REQ-PERF-001](REQ-PERF.md#req-perf-001-baseline-throughput--10-concurrent-users-sustain--5-rps-with-zero-failures) | Baseline 10 users, 0 % failures | CRITICAL | TC-PERF-001 ✅ |
| [REQ-PERF-002](REQ-PERF.md#req-perf-002-read-latency-p95--1000-ms) | Read latency P95 ≤ 1000 ms | CRITICAL | TC-PERF-002 ✅ |
| [REQ-PERF-003](REQ-PERF.md#req-perf-003-write-latency-p95--2000-ms) | Write latency P95 ≤ 2000 ms | NORMAL | TC-PERF-003 ✅ |
| [REQ-PERF-004](REQ-PERF.md#req-perf-004-no-degradation-at-2-baseline-load) | 2× baseline stress test | NORMAL | TC-PERF-004 ✅ |
| [REQ-PERF-005](REQ-PERF.md#req-perf-005-test-report-is-human-readable-and-ci-friendly) | HTML report, CI-friendly | NORMAL | TC-PERF-005 ✅ |

---


## TDD Closed-Loop Verification

```text
Requirements Spec (REQ-*.md)
       │
       ├──▶ Web UI  Test Data (test_data/*.yaml / *.json)
       │         │
       │         ├──▶ Playwright tests (web-ui-tests/tests/) ✅
       │         ├──▶ Selenium tests   (selenium-tests/tests/) ✅
       │         └──▶ Robot tests      (robot-tests/tests/)    ✅
       │
       └──▶ API    Test Data (test_data/*.yaml)
                 │
                 └──▶ pytest + requests  (api-tests/tests/)   ✅
```

**Closed-loop rule**: Every requirement → at least one test case → implemented in the relevant framework(s) → test results traceable back to the requirement.
