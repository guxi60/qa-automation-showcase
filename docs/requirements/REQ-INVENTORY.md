# REQ-INVENTORY: 商品浏览

> **模块**: 商品列表页 — `https://www.saucedemo.com/inventory.html`
>
> **页面元素**: 商品列表 (`.inventory_item`)、排序下拉 (`[data-test="product-sort-container"]`)、购物车徽章 (`.shopping_cart_badge`)、购物车链接 (`.shopping_cart_link`)

---

## REQ-INV-001: 商品列表展示 6 件商品

- **优先级**: BLOCKER
- **类型**: Functional · Smoke
- **前置条件**: 已使用标准账号登录
- **验收标准**:
  1. Given 用户已登录 → When 进入 Inventory 页面 → Then 显示 6 件商品，标题为 "Products"
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-001 | test_inventory.py | ✅ |
  | Selenium | TC-INV-001 | test_inventory.py | ✅ |

---

## REQ-INV-002: 商品数据完整性（名称 + 价格）

- **优先级**: CRITICAL
- **类型**: Functional · Data Integrity
- **前置条件**: 已登录
- **验收标准**:
  1. Given 用户在 Inventory 页 → When 遍历所有商品 → Then 每件商品名称非空、价格 > $0
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-002 | test_inventory.py | ✅ |
  | Selenium | TC-INV-002 | test_inventory.py | ✅ |

---

## REQ-INV-003: 商品图片有效加载

- **优先级**: CRITICAL
- **类型**: GUI · Data Integrity
- **前置条件**: 已登录
- **验收标准**:
  1. Given 用户在 Inventory 页 → When 查看每件商品 → Then 每件商品图片可见，src 属性有效（以 `/static/media/` 或 `http` 开头）
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-003 | test_inventory.py | ✅ |
  | Selenium | TC-INV-003 | test_inventory.py | ✅ |

---

## REQ-INV-004: 商品排序（4 种排序方式）

- **优先级**: CRITICAL
- **类型**: Functional
- **前置条件**: 已登录
- **验收标准**:
  1. Given 用户在 Inventory 页 → When 选择 "Name (A to Z)" → Then 第一件商品为 "Sauce Labs Backpack"
  2. Given 用户在 Inventory 页 → When 选择 "Name (Z to A)" → Then 第一件商品为 "Test.allTheThings() T-Shirt (Red)"
  3. Given 用户在 Inventory 页 → When 选择 "Price (low to high)" → Then 第一件商品为 "Sauce Labs Onesie"
  4. Given 用户在 Inventory 页 → When 选择 "Price (high to low)" → Then 第一件商品为 "Sauce Labs Fleece Jacket"
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-004 | test_inventory.py | ✅ |
  | Selenium | TC-INV-004 | test_inventory.py | ✅ |

---

## REQ-INV-005: 价格排序数值正确性

- **优先级**: MINOR
- **类型**: Functional
- **前置条件**: 已登录
- **验收标准**:
  1. Given 用户选择 "Price (low to high)" → When 遍历价格列表 → Then 价格为非递减序列
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-005 | test_inventory.py | ✅ |
  | Selenium | TC-INV-005 | test_inventory.py | ✅ |

---

## REQ-INV-006: 空购物车时徽章隐藏

- **优先级**: CRITICAL
- **类型**: Functional
- **前置条件**: 已登录，购物车为空
- **验收标准**:
  1. Given 用户刚登录进入 Inventory 页 → When 购物车为空 → Then 购物车徽章不显示（count = 0）
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-006 | test_inventory.py | ✅ |
  | Selenium | TC-INV-006 | test_inventory.py | ✅ |

---

## REQ-INV-007: 添加商品时徽章递增

- **优先级**: CRITICAL
- **类型**: Functional
- **前置条件**: 已登录
- **验收标准**:
  1. Given 购物车为空 → When 依次添加 2 件商品 → Then 徽章数字依次为 1、2
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-007 | test_inventory.py | ✅ |
  | Selenium | TC-INV-007 | test_inventory.py | ✅ |

---

## REQ-INV-008: 添加后移除商品徽章归零

- **优先级**: NORMAL
- **类型**: Functional
- **前置条件**: 已登录
- **验收标准**:
  1. Given 用户添加 1 件商品 → When 点击该商品的 Remove → Then 徽章归零
- **关联测试用例**:
  | 框架 | 用例ID | 文件 | 状态 |
  |------|--------|------|------|
  | Playwright | TC-INV-008 | test_inventory.py | ✅ |
  | Selenium | TC-INV-008 | test_inventory.py | ✅ |
