# REQ-CART: Shopping Cart

> **Module**: Cart page — `https://www.saucedemo.com/cart.html`
>
> **Page elements**: Cart item list (`.cart_item`), Checkout button (`[data-test="checkout"]`), Continue Shopping (`[data-test="continue-shopping"]`)

---

## REQ-CART-001: Added items appear in the cart

- **Priority**: BLOCKER
- **Type**: Functional · Smoke
- **Precondition**: Logged in, items added to cart
- **Acceptance Criteria**:
  1. Given the user added N items from the Inventory → When navigating to the Cart page → Then the cart displays N items with names matching those added
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CART-001 | test_cart.py | ✅ |
  | Selenium | TC-CART-001 | test_cart.py | ✅ |
  | Robot Framework | TC-CART-001 | cart.robot | ✅ |

---

## REQ-CART-002: Remove item from cart

- **Priority**: CRITICAL
- **Type**: Functional
- **Precondition**: Cart contains multiple items
- **Acceptance Criteria**:
  1. Given the cart has 2 items → When clicking Remove on 1 of them → Then the item count drops to 1 and the removed item is no longer in the list
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CART-002 | test_cart.py | ✅ |
  | Selenium | TC-CART-002 | test_cart.py | ✅ |
  | Robot Framework | TC-CART-002 | cart.robot | ✅ |

---

## REQ-CART-003: Cart state persists across page navigation

- **Priority**: CRITICAL
- **Type**: Functional · State
- **Precondition**: Items added to cart
- **Acceptance Criteria**:
  1. Given the user added 1 item (badge shows 1) → When navigating to the cart and back to Inventory → Then the badge still shows 1 and the item remains in the cart
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CART-003 | test_cart.py | ✅ |
  | Selenium | TC-CART-003 | test_cart.py | ✅ |
  | Robot Framework | TC-CART-003 | cart.robot | ✅ |

---

## REQ-CART-004: Empty cart state

- **Priority**: CRITICAL
- **Type**: Functional · Empty State
- **Precondition**: Logged in, no items added
- **Acceptance Criteria**:
  1. Given the user has just logged in without adding items → When navigating to the Cart page → Then the cart is empty (item count = 0)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CART-004 | test_cart.py | ✅ |
  | Selenium | TC-CART-004 | test_cart.py | ✅ |
  | Robot Framework | TC-CART-004 | cart.robot | ✅ |

---

## REQ-CART-005: Checkout button available

- **Priority**: CRITICAL
- **Type**: GUI · Functional
- **Precondition**: Cart has items
- **Acceptance Criteria**:
  1. Given the cart has items → When viewing the checkout button → Then the button is visible and enabled
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-CART-005 | test_cart.py | ✅ |
  | Selenium | TC-CART-005 | test_cart.py | ✅ |
  | Robot Framework | TC-CART-005 | cart.robot | ✅ |
