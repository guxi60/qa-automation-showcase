# REQ-API-USERS: Users API — CRUD & Schema Validation

> **Module**: User resource REST endpoints — `https://jsonplaceholder.typicode.com/users`
>
> **Sub-pages**:
> - `GET    /users`     — list all (10 users)
> - `GET    /users/{id}` — single user
> - `POST   /users`     — create
> - `PUT    /users/{id}` — update
> - `DELETE /users/{id}` — remove

---

## REQ-API-USERS-001: List all users with correct count and structure

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: API is reachable
- **Acceptance Criteria**:
  1. Given the API endpoint `/users` → When sending `GET /users` → Then the API returns `200 OK` with a JSON array of exactly 10 user objects
  2. Given the response array → When inspecting each element → Then every object must contain the required keys: `id`, `name`, `username`, `email`, `address`, `phone`, `website`, `company`
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-001 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-002: Single user retrieval with JSON Schema validation

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: User ID `1` exists in the system
- **Acceptance Criteria**:
  1. Given user ID `1` → When sending `GET /users/1` → Then the API returns `200 OK` with a JSON object whose `id` matches the requested resource (`1`)
  2. Given the response body → When validated against the User JSON Schema → Then all required fields are present with correct types, including nested `address` and `company` objects
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-002 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-003: Create a new user and verify echoed payload

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: API accepts POST requests to `/users`
- **Acceptance Criteria**:
  1. Given a well-formed user JSON payload → When sending `POST /users` with the body → Then the API returns `201 Created`
  2. Given the `201` response → When inspecting the echoed object → Then the `name`, `username`, and `email` fields match the submitted values
  3. Given the echoed object → When inspecting `id` → Then it is auto-assigned as an integer
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-003 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-004: Full update of an existing user

- **Priority**: NORMAL
- **Type**: Functional · Happy Path
- **Precondition**: User ID `1` exists
- **Acceptance Criteria**:
  1. Given a complete replacement user JSON payload → When sending `PUT /users/1` with that body → Then the API returns `200 OK`
  2. Given the `200` response → When inspecting the echoed object → Then `name`, `email`, and `username` reflect the submitted replacement values
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-004 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-005: Delete an existing user

- **Priority**: NORMAL
- **Type**: Functional · Happy Path
- **Precondition**: User ID `1` exists
- **Acceptance Criteria**:
  1. Given user ID `1` → When sending `DELETE /users/1` → Then the API returns `200 OK` (JSONPlaceholder convention; a real API would return `204 No Content`)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-005 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-006: Non-existent user returns 404

- **Priority**: MINOR
- **Type**: Functional · Negative
- **Precondition**: User ID `999` does not exist
- **Acceptance Criteria**:
  1. Given a non-existent user ID `999` → When sending `GET /users/999` → Then the API returns `404 Not Found`
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-006 | api-tests/tests/test_users.py | ✅ |

---

## REQ-API-USERS-007: Batch JSON Schema validation across all users

- **Priority**: BLOCKER
- **Type**: Functional · Data Integrity
- **Precondition**: The `/users` endpoint returns the full 10-user collection
- **Acceptance Criteria**:
  1. Given the full user collection from `GET /users` → When validating each user object against the User JSON Schema → Then all 10 users pass validation with zero schema violations
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-USERS-007 | api-tests/tests/test_users.py | ✅ |
