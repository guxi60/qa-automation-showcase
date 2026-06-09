# Requirements Traceability Matrix (RTM)

> **Purpose**: Track the mapping of every requirement → test case, ensuring 100% requirements coverage.
>
> **Legend**: ✅ Implemented · ⬜ To be implemented · — Not applicable

---

## Coverage Overview

| Module | Reqs | Playwright | Selenium | Robot Framework |
|--------|------|------------|----------|-----------------|
| AUTH | 6 | 6/6 ✅ | 6/6 ✅ | 6/6 ✅ |
| INVENTORY | 8 | 8/8 ✅ | 8/8 ✅ | 8/8 ✅ |
| CART | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ |
| CHECKOUT | 5 | 5/5 ✅ | 5/5 ✅ | 5/5 ✅ |
| **Total** | **24** | **24/24 (100%)** | **24/24 (100%)** | **24/24 (100%)** |

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

---

## TDD Closed-Loop Verification

```text
Requirements Spec (REQ-*.md)
       │
       ▼
   Test Data (test_data/*.json)
       │
       ├──▶ Playwright tests (web-ui-tests/tests/) ✅
       ├──▶ Selenium tests   (selenium-tests/tests/) ✅
       └──▶ Robot tests      (robot-tests/tests/)    ✅
```

**Closed-loop rule**: Every requirement → at least one test case → implemented in all three frameworks → test results traceable back to the requirement.
