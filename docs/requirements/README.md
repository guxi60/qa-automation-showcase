# Requirements Specification — SauceDemo

> **被测系统**: [SauceDemo](https://www.saucedemo.com/) — 标准电商网站
>
> **方法论**: 本需求规格从已有自动化测试逆向提炼，采用 EARS (Easy Approach to Requirements Syntax) 风格编写验收标准。

---

## 需求组织

| 模块 | 文档 | 需求数 | 描述 |
|------|------|--------|------|
| 用户认证 | [REQ-AUTH.md](REQ-AUTH.md) | 6 | 登录/登出、凭据验证、错误提示、GUI 渲染 |
| 商品浏览 | [REQ-INVENTORY.md](REQ-INVENTORY.md) | 8 | 商品列表展示、排序、数据完整性、购物车徽章 |
| 购物车 | [REQ-CART.md](REQ-CART.md) | 5 | 商品增删、状态持久化、空状态、结账入口 |
| 结账流程 | [REQ-CHECKOUT.md](REQ-CHECKOUT.md) | 5 | E2E 购买流程、表单校验、取消返回 |

---

## 优先级定义

| 优先级 | 含义 |
|--------|------|
| **BLOCKER** | 核心路径阻断 — 用户无法完成基本操作 |
| **CRITICAL** | 重要功能异常 — 影响用户体验但可绕过 |
| **NORMAL** | 一般功能 — 不影响核心流程 |
| **MINOR** | 边缘场景或体验优化 |

---

## 需求追溯

完整的需求→测试追溯矩阵见 [traceability-matrix.md](traceability-matrix.md)。

---

## 测试框架覆盖

| 框架 | 覆盖状态 |
|------|---------|
| Playwright + pytest | ✅ 27 用例 — 完整覆盖 |
| Selenium + pytest | ✅ 24 用例 — 完整覆盖 |
| Robot Framework | ⬜ 待实现 |
