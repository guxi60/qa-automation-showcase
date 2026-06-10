# REQ-API-POSTS: Posts API — CRUD & Schema Validation

> **Module**: Post resource REST endpoints — `https://jsonplaceholder.typicode.com/posts`
>
> **Sub-pages**:
> - `GET    /posts`          — list all (100 posts)
> - `GET    /posts/{id}`      — single post
> - `GET    /posts?userId={id}` — filter by user
> - `POST   /posts`          — create
> - `PUT    /posts/{id}`      — update
> - `DELETE /posts/{id}`      — remove

---

## REQ-API-POSTS-001: List all posts with correct count and structure

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: API is reachable
- **Acceptance Criteria**:
  1. Given the API endpoint `/posts` → When sending `GET /posts` → Then the API returns `200 OK` with a JSON array of exactly 100 post objects
  2. Given the response array → When inspecting each element → Then every object must contain the required keys: `userId`, `id`, `title`, `body`
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-001 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-002: Single post retrieval with JSON Schema validation

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: Post ID `1` exists in the system
- **Acceptance Criteria**:
  1. Given post ID `1` → When sending `GET /posts/1` → Then the API returns `200 OK` with a JSON object whose `id` equals `1`
  2. Given the response body → When validated against the Post JSON Schema → Then required fields (`userId`, `id`, `title`, `body`) are present with correct types
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-002 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-003: Create a new post and verify echoed payload

- **Priority**: BLOCKER
- **Type**: Functional · Happy Path
- **Precondition**: API accepts POST requests to `/posts`
- **Acceptance Criteria**:
  1. Given a well-formed post JSON payload (with `userId`, `title`, `body`) → When sending `POST /posts` → Then the API returns `201 Created`
  2. Given the `201` response → When inspecting the echoed object → Then `title`, `body`, and `userId` match the submitted values
  3. Given the echoed object → When inspecting `id` → Then it is auto-assigned as an integer
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-003 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-004: Full update of an existing post

- **Priority**: NORMAL
- **Type**: Functional · Happy Path
- **Precondition**: Post ID `1` exists
- **Acceptance Criteria**:
  1. Given a complete replacement post JSON payload → When sending `PUT /posts/1` with that body → Then the API returns `200 OK`
  2. Given the `200` response → When inspecting the echoed object → Then `title` and `body` reflect the submitted replacement values
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-004 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-005: Delete an existing post

- **Priority**: NORMAL
- **Type**: Functional · Happy Path
- **Precondition**: Post ID `1` exists
- **Acceptance Criteria**:
  1. Given post ID `1` → When sending `DELETE /posts/1` → Then the API returns `200 OK` (JSONPlaceholder convention)
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-005 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-006: Filter posts by user ID

- **Priority**: NORMAL
- **Type**: Functional · Happy Path
- **Precondition**: Posts exist for user ID `1`
- **Acceptance Criteria**:
  1. Given user ID `1` → When sending `GET /posts?userId=1` → Then the API returns `200 OK` with only posts whose `userId` field equals `1`
  2. Given the response array → When counting results → Then at least one post is returned
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-006 | api-tests/tests/test_posts.py | ✅ |

---

## REQ-API-POSTS-007: Batch JSON Schema validation across all posts

- **Priority**: BLOCKER
- **Type**: Functional · Data Integrity
- **Precondition**: The `/posts` endpoint returns the full 100-post collection
- **Acceptance Criteria**:
  1. Given the full post collection from `GET /posts` → When validating each post object against the Post JSON Schema → Then all 100 posts pass validation with zero schema violations
- **Linked Test Cases**:
  | Framework | Case ID | File | Status |
  |-----------|---------|------|--------|
  | pytest + requests | TC-API-POSTS-007 | api-tests/tests/test_posts.py | ✅ |
