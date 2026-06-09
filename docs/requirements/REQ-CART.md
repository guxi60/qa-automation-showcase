# REQ-CART: 购物车

> **模块**: 购物车页 — `https://www.saucedemo.com/cart.html`
>
> **页面元素**: 购物车商品列表 (`.cart_item`)、结账按钮 (`[data-test="checkout"]`)、继续购物 (`[data-test="continue-shopping"]`)

---

## REQ-CART-001: 已添加商品在购物车中展示

- **优先级**: BLOCKER
- **类型**: Functional · Smoke
- **前置条件**: 已登录，已添加商品至购物车
- **验收标准**:
  1. Given 用户从 Inventory 添加了 N 件商品 → When 进入购物车页 → Then 购物车显示 N 件商品，名称与添加一致
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CART-001 | test_cart.py | ✅ |
  | Selenium | TC-CART-001 | test_cart.py | ✅ |

---

## REQ-CART-002: 从购物车移除商品

- **优先级**: CRITICAL
- **类型**: Functional
- **前置条件**: 购物车中有多件商品
- **验收标准**:
  1. Given 购物车有 2 件商品 → When 点击其中 1 件的 Remove → Then 商品数减为 1，被移除商品不在列表中
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CART-002 | test_cart.py | ✅ |
  | Selenium | TC-CART-002 | test_cart.py | ✅ |

---

## REQ-CART-003: 购物车状态跨页面持久化

- **优先级**: CRITICAL
- **类型**: Functional · State
- **前置条件**: 已添加商品
- **验收标准**:
  1. Given 用户添加 1 件商品（徽章显示 1） → When 进入购物车后返回 Inventory → Then 徽章仍显示 1，商品仍在购物车中
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CART-003 | test_cart.py | ✅ |
  | Selenium | TC-CART-003 | test_cart.py | ✅ |

---

## REQ-CART-004: 空购物车状态

- **优先级**: CRITICAL
- **类型**: Functional · Empty State
- **前置条件**: 已登录，未添加任何商品
- **验收标准**:
  1. Given 用户刚登录未添加商品 → When 进入购物车 → Then 购物车无商品（item count = 0）
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CART-004 | test_cart.py | ✅ |
  | Selenium | TC-CART-004 | test_cart.py | ✅ |

---

## REQ-CART-005: 结账按钮可用

- **优先级**: CRITICAL
- **类型**: GUI · Functional
- **前置条件**: 购物车有商品
- **验收标准**:
  1. Given 购物车有商品 → When 查看结账按钮 → Then 按钮可见且可点击
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-CART-005 | test_cart.py | ✅ |
  | Selenium | TC-CART-005 | test_cart.py | ✅ |
