# REQ-CHECKOUT: 结账流程

> **模块**: 结账三步流程 — 信息填写 → 订单确认 → 完成
>
> **子页面**:
> - Step One: `checkout-step-one.html` — 收货信息表单
> - Step Two: `checkout-step-two.html` — 订单概览
> - Complete: `checkout-complete.html` — 完成确认

---

## REQ-CHK-001: 完整购买流程 E2E

- **优先级**: BLOCKER
- **类型**: E2E · Happy Path
- **前置条件**: 已登录，购物车有商品
- **验收标准**:
  1. Given 用户购物车中有商品 → When 依次完成填写收货信息 → 确认订单 → 点击 Finish → Then 显示 "Thank you" 确认页 → 点击 Back Home 返回 Inventory
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CHK-001 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-001 | test_checkout.py | ✅ |

---

## REQ-CHK-002: 空名字段校验 — First Name

- **优先级**: CRITICAL
- **类型**: Functional · Validation · Negative
- **前置条件**: 已进入结账 Step One
- **验收标准**:
  1. Given 用户在结账表单 → When First Name 为空，点击 Continue → Then 显示包含 "First Name" 的错误信息
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CHK-002 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-002 | test_checkout.py | ✅ |

---

## REQ-CHK-003: 空名字段校验 — Last Name

- **优先级**: CRITICAL
- **类型**: Functional · Validation · Negative
- **前置条件**: 已进入结账 Step One
- **验收标准**:
  1. Given 用户在结账表单 → When Last Name 为空，点击 Continue → Then 显示包含 "Last Name" 的错误信息
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CHK-003 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-003 | test_checkout.py | ✅ |

---

## REQ-CHK-004: 空名字段校验 — Postal Code

- **优先级**: CRITICAL
- **类型**: Functional · Validation · Negative
- **前置条件**: 已进入结账 Step One
- **验收标准**:
  1. Given 用户在结账表单 → When Postal Code 为空，点击 Continue → Then 显示包含 "Postal Code" 的错误信息
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CHK-004 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-004 | test_checkout.py | ✅ |

---

## REQ-CHK-005: 取消返回购物车

- **优先级**: NORMAL
- **类型**: Functional · Navigation
- **前置条件**: 已进入结账 Step One
- **验收标准**:
  1. Given 用户在结账表单 → When 点击 Cancel（不填写任何字段）→ Then 返回购物车页，无副作用
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CHK-005 | test_checkout.py | ✅ |
  | Selenium | TC-CHK-005 | test_checkout.py | ✅ |
