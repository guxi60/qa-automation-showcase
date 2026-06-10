# REQ-AUTH: Authentication

> **Module**: Login page — `https://www.saucedemo.com/`
>
> **Page elements**: Username input (`[data-test="username"]`), Password input (`[data-test="password"]`), Login button (`[data-test="login-button"]`), Error message (`[data-test="error"]`)

---

## REQ-AUTH-001: Successful login with valid credentials

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: Use a valid account (e.g. `standard_user` / `secret_sauce`)
- **Acceptance Criteria**:
  1. Given the user is on the login page → When they enter a correct username and password and click Login → Then the page redirects to `/inventory.html`, displaying the "Products" title
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-001 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-001 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-001 | login.robot | ✅ |

---

## REQ-AUTH-002: Wrong password rejected

- **Priority**: CRITICAL
- **Type**: Functional · Negative
- **Precondition**: Use a valid username with an incorrect password
- **Acceptance Criteria**:
  1. Given the user is on the login page → When they enter a correct username but a wrong password and click Login → Then the page stays on the login page and displays an error containing "do not match"
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-002 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-002 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-002 | login.robot | ✅ |

---

## REQ-AUTH-003: Empty username rejected

- **Priority**: CRITICAL
- **Type**: Functional · Boundary
- **Precondition**: None
- **Acceptance Criteria**:
  1. Given the user is on the login page → When the username is empty and password is non-empty, then click Login → Then the error "Username is required" is displayed
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-003 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-003 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-003 | login.robot | ✅ |

---

## REQ-AUTH-004: Empty password rejected

- **Priority**: CRITICAL
- **Type**: Functional · Boundary
- **Precondition**: None
- **Acceptance Criteria**:
  1. Given the user is on the login page → When the username is non-empty and password is empty, then click Login → Then the error "Password is required" is displayed
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-004 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-004 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-004 | login.robot | ✅ |

---

## REQ-AUTH-005: Locked-out account denied access

- **Priority**: CRITICAL
- **Type**: Functional · Access Control
- **Precondition**: Use the `locked_out_user` account
- **Acceptance Criteria**:
  1. Given the user is on the login page → When they attempt to log in with a locked-out account → Then an error containing "locked out" is displayed and the user remains on the login page
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-005 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-005 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-005 | login.robot | ✅ |

---

## REQ-AUTH-006: Login page GUI elements render correctly

- **Priority**: BLOCKER
- **Type**: GUI
- **Precondition**: None
- **Acceptance Criteria**:
  1. Given the user visits the login page → When the page finishes loading → Then the username input, password input, and Login button are all visible, and the button reads "Login"
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | Playwright | TC-LOGIN-006 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-006 | test_login.py | ✅ |
  | Robot Framework | TC-LOGIN-006 | login.robot | ✅ |
