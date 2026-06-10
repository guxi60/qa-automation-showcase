# REQ-CHECKOUT: Checkout Flow

> **Module**: Three-step checkout — Information → Overview → Complete
>
> **Sub-pages**:
> - Step One: `checkout-step-one.html` — Shipping information form
> - Step Two: `checkout-step-two.html` — Order overview
> - Complete: `checkout-complete.html` — Order confirmation

---

## REQ-CHK-001: Complete E2E purchase flow

- **Priority**: BLOCKER
- **Type**: E2E · Happy Path
- **Precondition**: Logged in, items in cart
- **Acceptance Criteria**:
  1. Given the user's cart has items → When they complete the shipping form → review the order → click Finish → Then a "Thank you" confirmation is displayed → and clicking Back Home returns to Inventory
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CHK-001 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-001 | test_checkout.py | ✅ |
  | Robot Framework | TC-CHK-001 | checkout.robot | ✅ |

---

## REQ-CHK-002: Empty field validation — First Name

- **Priority**: CRITICAL
- **Type**: Functional · Validation · Negative
- **Precondition**: On Checkout Step One
- **Acceptance Criteria**:
  1. Given the user is on the checkout form → When First Name is empty and Continue is clicked → Then an error containing "First Name" is displayed
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CHK-002 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-002 | test_checkout.py | ✅ |
  | Robot Framework | TC-CHK-002 | checkout.robot | ✅ |

---

## REQ-CHK-003: Empty field validation — Last Name

- **Priority**: CRITICAL
- **Type**: Functional · Validation · Negative
- **Precondition**: On Checkout Step One
- **Acceptance Criteria**:
  1. Given the user is on the checkout form → When Last Name is empty and Continue is clicked → Then an error containing "Last Name" is displayed
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CHK-003 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-003 | test_checkout.py | ✅ |
  | Robot Framework | TC-CHK-003 | checkout.robot | ✅ |

---

## REQ-CHK-004: Empty field validation — Postal Code

- **Priority**: CRITICAL
- **Type**: Functional · Validation · Negative
- **Precondition**: On Checkout Step One
- **Acceptance Criteria**:
  1. Given the user is on the checkout form → When Postal Code is empty and Continue is clicked → Then an error containing "Postal Code" is displayed
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CHK-004 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-004 | test_checkout.py | ✅ |
  | Robot Framework | TC-CHK-004 | checkout.robot | ✅ |

---

## REQ-CHK-005: Cancel returns to cart

- **Priority**: NORMAL
- **Type**: Functional · Navigation
- **Precondition**: On Checkout Step One
- **Acceptance Criteria**:
  1. Given the user is on the checkout form → When they click Cancel (without filling any fields) → Then they are returned to the cart page with no side effects
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CHK-005 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-005 | test_checkout.py | ✅ |
  | Robot Framework | TC-CHK-005 | checkout.robot | ✅ |
