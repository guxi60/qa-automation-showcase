# QA Automation Showcase

> **同一个被测系统，三套自动化框架 —— 这是我的测试工程能力的最佳证明。**
>
> 被测对象：[SauceDemo](https://www.saucedemo.com/)（标准电商流程：登录 → 商品浏览 → 购物车 → 结账）

---

## 🎯 项目理念

这个项目的核心叙事是：**从传统到现代，从单一到多元**。

| 框架 | 定位 | 理念 |
|------|------|------|
| **Selenium + pytest** | 我的老本行 | WebDriver 标准协议，最广泛的浏览器兼容性 |
| **Robot Framework** | 我在 PwC 推动的转型 | 关键字驱动，降低非技术人员参与门槛 |
| **Playwright + pytest** | 我主动学习的新一代 | 现代化架构，auto-wait、trace、并行执行 |

面试时我可以清楚地告诉你：**什么场景选什么框架，以及为什么。**

---

## 🧰 技术栈

```
Web UI Testing:  Selenium  |  Playwright  |  Robot Framework
API Testing:     pytest + requests  |  JSON Schema Validation
Mobile Testing:  Maestro
Performance:     JMeter
CI/CD:           GitHub Actions
Lang:            Python 3.x
Reports:         pytest-html  |  Allure
```

---

## 📁 项目结构

```
qa-automation-showcase/
├── web-ui-tests/                # Playwright + pytest（现代化方案）
│   ├── pages/                   # Page Object Model
│   ├── tests/                   # 测试用例
│   ├── test_data/               # 测试数据
│   └── conftest.py              # Fixtures & 配置
├── selenium-tests/              # Selenium + pytest（经典方案）
│   ├── pages/                   # Page Object Model
│   ├── tests/                   # 测试用例
│   ├── test_data/               # 测试数据
│   └── conftest.py              # Fixtures & 配置
├── robot-tests/                 # Robot Framework（关键字驱动方案）
│   ├── resources/               # 公共关键字 & 页面对象
│   └── tests/                   # .robot 用例文件
├── api-tests/                   # API 测试
│   ├── tests/                   # 接口测试用例
│   └── schemas/                 # JSON Schema 定义
├── performance/                 # JMeter 性能测试
├── mobile-tests/                # Maestro 移动端测试
├── .github/workflows/           # GitHub Actions CI
└── requirements.txt             # Python 依赖
```

---

## 🚀 快速开始

```bash
# 1. Clone
git clone https://github.com/guxi60/qa-automation-showcase.git
cd qa-automation-showcase

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
playwright install chromium

# 4. 运行 Playwright 测试
cd web-ui-tests
pytest -v --html=report.html

# 5. 运行 Selenium 测试
cd selenium-tests
pytest -v --html=report.html

# 6. 运行 Robot Framework 测试
cd robot-tests
robot -d results tests/

# 7. 运行 API 测试
cd api-tests
pytest -v
```

---

## 📊 测试覆盖矩阵

| 功能模块 | Playwright | Selenium | Robot Framework | API |
|---------|-----------|----------|-----------------|-----|
| 登录（正常/异常/边界） | ✅ | ✅ | ✅ | — |
| 商品列表（排序/展示） | ✅ | ✅ | — | — |
| 购物车（增删改） | ✅ | ✅ | — | — |
| 结账 E2E | ✅ | ✅ | ✅ | — |
| 用户 CRUD | — | — | — | ✅ |
| 帖子 CRUD | — | — | — | ✅ |
| Schema 校验 | — | — | — | ✅ |
| 性能压测 | — | — | — | — |

---

## 🧪 测试理念

1. **可读性优先** — 测试用例读起来应该像场景描述，不是代码堆砌
2. **失败可追溯** — 每次失败自动截图 + trace，不需要重现才能定位
3. **数据分离** — 测试数据与逻辑解耦
4. **横向可比较** — 同一个场景用不同框架实现，体现工具选型能力

---

## 👤 关于我

顾翔 (Gu Xiang) | Senior QA Engineer | 15+ 年测试经验

- 精通 Selenium / Robot Framework / Playwright / Maestro / JMeter
- 曾任 QA Lead / Scrum Master，带领跨时区测试团队
- 从 CT 医疗影像到 Web3 数字钱包，多行业测试经验
- 热衷于 AI + 自动化测试的结合

📧 guxi60@outlook.com
