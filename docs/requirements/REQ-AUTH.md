# REQ-AUTH: 用户认证

> **模块**: 登录页面 — `https://www.saucedemo.com/`
>
> **页面元素**: 用户名输入框 (`[data-test="username"]`)、密码输入框 (`[data-test="password"]`)、登录按钮 (`[data-test="login-button"]`)、错误提示 (`[data-test="error"]`)

---

## REQ-AUTH-001: 有效凭据登录成功

- **优先级**: BLOCKER
- **类型**: Functional · Happy Path
- **前置条件**: 使用有效账号（如 `standard_user` / `secret_sauce`）
- **验收标准**:
  1. Given 用户在登录页 → When 输入正确用户名和密码并点击 Login → Then 页面跳转至 `/inventory.html`，显示 Products 标题
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-001 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-001 | test_login.py | ✅ |

---

## REQ-AUTH-002: 错误密码拒绝登录

- **优先级**: CRITICAL
- **类型**: Functional · Negative
- **前置条件**: 使用有效用户名但错误密码
- **验收标准**:
  1. Given 用户在登录页 → When 输入正确用户名但错误密码并点击 Login → Then 页面停留在登录页，显示包含 "do not match" 的错误信息
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-002 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-002 | test_login.py | ✅ |

---

## REQ-AUTH-003: 空用户名拒绝登录

- **优先级**: CRITICAL
- **类型**: Functional · Boundary
- **前置条件**: 无
- **验收标准**:
  1. Given 用户在登录页 → When 用户名为空、密码非空，点击 Login → Then 显示 "Username is required" 错误
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-003 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-003 | test_login.py | ✅ |

---

## REQ-AUTH-004: 空密码拒绝登录

- **优先级**: CRITICAL
- **类型**: Functional · Boundary
- **前置条件**: 无
- **验收标准**:
  1. Given 用户在登录页 → When 用户名非空、密码为空，点击 Login → Then 显示 "Password is required" 错误
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-004 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-004 | test_login.py | ✅ |

---

## REQ-AUTH-005: 锁定账户拒绝访问

- **优先级**: CRITICAL
- **类型**: Functional · Access Control
- **前置条件**: 使用 `locked_out_user` 账号
- **验收标准**:
  1. Given 用户在登录页 → When 使用被锁定的账号登录 → Then 显示包含 "locked out" 的错误信息，停留在登录页
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-005 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-005 | test_login.py | ✅ |

---

## REQ-AUTH-006: 登录页 GUI 元素渲染

- **优先级**: BLOCKER
- **类型**: GUI
- **前置条件**: 无
- **验收标准**:
  1. Given 用户访问登录页 → When 页面加载完成 → Then 用户名输入框、密码输入框、Login 按钮均可见，按钮显示 "Login" 文案
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-LOGIN-006 | test_login.py | ✅ |
  | Selenium | TC-LOGIN-006 | test_login.py | ✅ |
