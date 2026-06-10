# REQ-INVENTORY: Product Inventory

> **Module**: Inventory page — `https://www.saucedemo.com/inventory.html`
>
> **Page elements**: Product list (`.inventory_item`), Sort dropdown (`[data-test="product-sort-container"]`), Cart badge (`.shopping_cart_badge`), Cart link (`.shopping_cart_link`)

---

## REQ-INV-001: Product listing displays 6 items

- **Priority**: BLOCKER
- **Type**: Functional · Smoke
- **Precondition**: Logged in with a standard account
- **Acceptance Criteria**:
  1. Given the user is logged in → When they land on the Inventory page → Then 6 products are displayed with the title "Products"
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-001 | test_inventory.py | ✅ |
  | Selenium | TC-INV-001 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-001 | inventory.robot | ✅ |

---

## REQ-INV-002: Product data integrity (name + price)

- **Priority**: CRITICAL
- **Type**: Functional · Data Integrity
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the user is on the Inventory page → When iterating over all products → Then every product has a non-empty name and a price > $0
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-002 | test_inventory.py | ✅ |
  | Selenium | TC-INV-002 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-002 | inventory.robot | ✅ |

---

## REQ-INV-003: Product images load correctly

- **Priority**: CRITICAL
- **Type**: GUI · Data Integrity
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the user is on the Inventory page → When viewing each product → Then every product image is visible and has a valid `src` attribute (starting with `/static/media/` or `http`)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-003 | test_inventory.py | ✅ |
  | Selenium | TC-INV-003 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-003 | inventory.robot | ✅ |

---

## REQ-INV-004: Product sorting (4 sort options)

- **Priority**: CRITICAL
- **Type**: Functional
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the user is on the Inventory page → When selecting "Name (A to Z)" → Then the first product is "Sauce Labs Backpack"
  2. Given the user is on the Inventory page → When selecting "Name (Z to A)" → Then the first product is "Test.allTheThings() T-Shirt (Red)"
  3. Given the user is on the Inventory page → When selecting "Price (low to high)" → Then the first product is "Sauce Labs Onesie"
  4. Given the user is on the Inventory page → When selecting "Price (high to low)" → Then the first product is "Sauce Labs Fleece Jacket"
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-004 | test_inventory.py | ✅ |
  | Selenium | TC-INV-004 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-004 | inventory.robot | ✅ |

---

## REQ-INV-005: Price sort is numerically correct

- **Priority**: MINOR
- **Type**: Functional
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the user selects "Price (low to high)" → When iterating over the price list → Then prices are in non-decreasing order
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-005 | test_inventory.py | ✅ |
  | Selenium | TC-INV-005 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-005 | inventory.robot | ✅ |

---

## REQ-INV-006: Cart badge hidden when cart is empty

- **Priority**: CRITICAL
- **Type**: Functional
- **Precondition**: Logged in, cart is empty
- **Acceptance Criteria**:
  1. Given the user has just logged in and landed on the Inventory page → When the cart is empty → Then the cart badge is not displayed (count = 0)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-006 | test_inventory.py | ✅ |
  | Selenium | TC-INV-006 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-006 | inventory.robot | ✅ |

---

## REQ-INV-007: Cart badge increments when adding items

- **Priority**: CRITICAL
- **Type**: Functional
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the cart is empty → When 2 items are added sequentially → Then the badge shows 1, then 2
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-007 | test_inventory.py | ✅ |
  | Selenium | TC-INV-007 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-007 | inventory.robot | ✅ |

---

## REQ-INV-008: Add-then-remove resets cart badge to zero

- **Priority**: NORMAL
- **Type**: Functional
- **Precondition**: Logged in
- **Acceptance Criteria**:
  1. Given the user adds 1 item → When clicking Remove on that item → Then the badge returns to zero
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-INV-008 | test_inventory.py | ✅ |
  | Selenium | TC-INV-008 | test_inventory.py | ✅ |
  | Robot Framework | TC-INV-008 | inventory.robot | ✅ |
