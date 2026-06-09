# Requirements Traceability Matrix (RTM)

> **用途**: 追踪每条需求 → 测试用例的映射关系，确保需求覆盖率 100%。
>
> **图例**: ✅ 已实现 · ⬜ 待实现 · — 不适用

---

## 覆盖概览

| 模块 | 需求数 | Playwright | Selenium | Robot Framework |
|------|--------|------------|----------|-----------------|
| AUTH | 6 | 6/6 ✅ | 6/6 ✅ | 0/6 ⬜ |
| INVENTORY | 8 | 8/8 ✅ | 8/8 ✅ | 0/8 ⬜ |
| CART | 5 | 5/5 ✅ | 5/5 ✅ | 0/5 ⬜ |
| CHECKOUT | 5 | 5/5 ✅ | 5/5 ✅ | 0/5 ⬜ |
| **总计** | **24** | **24/24 (100%)** | **24/24 (100%)** | **0/24 (0%)** |

---

## 详细追溯

### AUTH — 用户认证

| 需求ID | 需求描述 | 优先级 | Playwright | Selenium | Robot |
|--------|---------|--------|------------|----------|-------|
| [REQ-AUTH-001](REQ-AUTH.md#req-auth-001-有效凭据登录成功) | 有效凭据登录成功 | BLOCKER | TC-LOGIN-001 ✅ | TC-LOGIN-001 ✅ | ⬜ |
| [REQ-AUTH-002](REQ-AUTH.md#req-auth-002-错误密码拒绝登录) | 错误密码拒绝登录 | CRITICAL | TC-LOGIN-002 ✅ | TC-LOGIN-002 ✅ | ⬜ |
| [REQ-AUTH-003](REQ-AUTH.md#req-auth-003-空用户名拒绝登录) | 空用户名拒绝登录 | CRITICAL | TC-LOGIN-003 ✅ | TC-LOGIN-003 ✅ | ⬜ |
| [REQ-AUTH-004](REQ-AUTH.md#req-auth-004-空密码拒绝登录) | 空密码拒绝登录 | CRITICAL | TC-LOGIN-004 ✅ | TC-LOGIN-004 ✅ | ⬜ |
| [REQ-AUTH-005](REQ-AUTH.md#req-auth-005-锁定账户拒绝访问) | 锁定账户拒绝访问 | CRITICAL | TC-LOGIN-005 ✅ | TC-LOGIN-005 ✅ | ⬜ |
| [REQ-AUTH-006](REQ-AUTH.md#req-auth-006-登录页-gui-元素渲染) | 登录页 GUI 元素渲染 | BLOCKER | TC-LOGIN-006 ✅ | TC-LOGIN-006 ✅ | ⬜ |

### INVENTORY — 商品浏览

| 需求ID | 需求描述 | 优先级 | Playwright | Selenium | Robot |
|--------|---------|--------|------------|----------|-------|
| [REQ-INV-001](REQ-INVENTORY.md#req-inv-001-商品列表展示-6-件商品) | 商品列表展示 6 件商品 | BLOCKER | TC-INV-001 ✅ | TC-INV-001 ✅ | ⬜ |
| [REQ-INV-002](REQ-INVENTORY.md#req-inv-002-商品数据完整性名称--价格) | 商品数据完整性（名称+价格） | CRITICAL | TC-INV-002 ✅ | TC-INV-002 ✅ | ⬜ |
| [REQ-INV-003](REQ-INVENTORY.md#req-inv-003-商品图片有效加载) | 商品图片有效加载 | CRITICAL | TC-INV-003 ✅ | TC-INV-003 ✅ | ⬜ |
| [REQ-INV-004](REQ-INVENTORY.md#req-inv-004-商品排序4-种排序方式) | 商品排序（4 种方式） | CRITICAL | TC-INV-004 ✅ | TC-INV-004 ✅ | ⬜ |
| [REQ-INV-005](REQ-INVENTORY.md#req-inv-005-价格排序数值正确性) | 价格排序数值正确性 | MINOR | TC-INV-005 ✅ | TC-INV-005 ✅ | ⬜ |
| [REQ-INV-006](REQ-INVENTORY.md#req-inv-006-空购物车时徽章隐藏) | 空购物车时徽章隐藏 | CRITICAL | TC-INV-006 ✅ | TC-INV-006 ✅ | ⬜ |
| [REQ-INV-007](REQ-INVENTORY.md#req-inv-007-添加商品时徽章递增) | 添加商品时徽章递增 | CRITICAL | TC-INV-007 ✅ | TC-INV-007 ✅ | ⬜ |
| [REQ-INV-008](REQ-INVENTORY.md#req-inv-008-添加后移除商品徽章归零) | 添加后移除商品徽章归零 | NORMAL | TC-INV-008 ✅ | TC-INV-008 ✅ | ⬜ |

### CART — 购物车

| 需求ID | 需求描述 | 优先级 | Playwright | Selenium | Robot |
|--------|---------|--------|------------|----------|-------|
| [REQ-CART-001](REQ-CART.md#req-cart-001-已添加商品在购物车中展示) | 已添加商品在购物车中展示 | BLOCKER | TC-CART-001 ✅ | TC-CART-001 ✅ | ⬜ |
| [REQ-CART-002](REQ-CART.md#req-cart-002-从购物车移除商品) | 从购物车移除商品 | CRITICAL | TC-CART-002 ✅ | TC-CART-002 ✅ | ⬜ |
| [REQ-CART-003](REQ-CART.md#req-cart-003-购物车状态跨页面持久化) | 购物车状态跨页面持久化 | CRITICAL | TC-CART-003 ✅ | TC-CART-003 ✅ | ⬜ |
| [REQ-CART-004](REQ-CART.md#req-cart-004-空购物车状态) | 空购物车状态 | CRITICAL | TC-CART-004 ✅ | TC-CART-004 ✅ | ⬜ |
| [REQ-CART-005](REQ-CART.md#req-cart-005-结账按钮可用) | 结账按钮可用 | CRITICAL | TC-CART-005 ✅ | TC-CART-005 ✅ | ⬜ |

### CHECKOUT — 结账流程

| 需求ID | 需求描述 | 优先级 | Playwright | Selenium | Robot |
|--------|---------|--------|------------|----------|-------|
| [REQ-CHK-001](REQ-CHECKOUT.md#req-chk-001-完整购买流程-e2e) | 完整购买流程 E2E | BLOCKER | TC-CHK-001 ✅ | TC-CHK-001 ✅ | ⬜ |
| [REQ-CHK-002](REQ-CHECKOUT.md#req-chk-002-空名字段校验--first-name) | 空字段校验 — First Name | CRITICAL | TC-CHK-002 ✅ | TC-CHK-002 ✅ | ⬜ |
| [REQ-CHK-003](REQ-CHECKOUT.md#req-chk-003-空名字段校验--last-name) | 空字段校验 — Last Name | CRITICAL | TC-CHK-003 ✅ | TC-CHK-003 ✅ | ⬜ |
| [REQ-CHK-004](REQ-CHECKOUT.md#req-chk-004-空名字段校验--postal-code) | 空字段校验 — Postal Code | CRITICAL | TC-CHK-004 ✅ | TC-CHK-004 ✅ | ⬜ |
| [REQ-CHK-005](REQ-CHECKOUT.md#req-chk-005-取消返回购物车) | 取消返回购物车 | NORMAL | TC-CHK-005 ✅ | TC-CHK-005 ✅ | ⬜ |

---

## TDD 闭环验证

```
需求规格文档 (REQ-*.md)
       │
       ▼
  测试数据 (test_data/*.json)
       │
       ├──▶ Playwright 测试 (web-ui-tests/tests/)
       │         │
       │         ▼
       │    Allure 报告
       │
       └──▶ Selenium 测试 (selenium-tests/tests/)
                 │
                 ▼
            pytest-html 报告
```

**闭环规则**: 每条需求 → 至少一个测试用例 → 至少在两个框架中实现 → 测试结果可追溯回需求。
