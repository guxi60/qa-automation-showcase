# QA Automation Showcase

> **同一个被测系统，三套自动化框架 —— 一套完整的测试工程对比，展示工具选型与技术迁移能力。**
>
> 被测对象：[SauceDemo](https://www.saucedemo.com/)（标准电商流程：登录 → 商品浏览 → 购物车 → 结账）

---

## 🎯 项目动机

做这个项目的出发点很简单：**什么场景该选什么测试框架？** 与其在面试中口头回答，不如用代码说话。

同一个 SauceDemo 电商网站，分别用三种不同理念的框架实现完整的测试覆盖：

| 框架 | 设计理念 | 适用场景 |
|------|---------|---------|
| **Selenium + pytest** | WebDriver 标准协议，最广泛的浏览器支持 | 多浏览器兼容性测试、传统企业项目 |
| **Robot Framework** | 关键字驱动，降低非技术成员的参与门槛 | 跨角色协作项目、BDD 风格团队 |
| **Playwright + pytest** | 现代化设计，内置 auto-wait、trace、并行 | 快速迭代的 Web 应用、新项目启动 |

每种框架有各自的 POM 实现、测试用例和网络容错策略，可以直接对比它们在同一个场景下的表现差异。

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
├── web-ui-tests/                # Playwright + pytest（现代方案）
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

# 2. 创建虚拟环境 & 安装依赖
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# 3. 运行 Playwright 测试（含 HTML 报告）
cd web-ui-tests
pytest -v --html=report.html --self-contained-html
# 报告: web-ui-tests/report.html

# 4. 运行 Selenium 测试
cd selenium-tests
pytest -v --html=report.html --self-contained-html

# 5. 运行 Robot Framework 测试
cd robot-tests
robot -d results tests/

# 6. 运行 API 测试
cd api-tests
pytest -v
```

---

## 📊 测试覆盖矩阵

| 功能模块 | Playwright | Selenium | Robot Framework | API |
|---------|-----------|----------|-----------------|-----|
| 登录（正常/异常/边界） | ✅ (6 用例) | ⬜ | ⬜ | — |
| 商品列表（排序/展示/图片） | ✅ (11 用例) | ⬜ | — | — |
| 购物车（增删改/持久化） | ✅ (5 用例) | ⬜ | — | — |
| 结账 E2E（含表单校验） | ✅ (5 用例) | ⬜ | ⬜ | — |
| 用户 CRUD | — | — | — | ⬜ |
| 帖子 CRUD | — | — | — | ⬜ |
| Schema 校验 | — | — | — | ⬜ |
| 性能压测 | — | — | — | — |

---

## 🧪 测试理念

1. **可读性优先** — 测试用例的结构读起来像场景描述，而非代码堆砌
2. **失败可追溯** — 每次测试失败自动截图，无需重现即可定位问题
3. **数据与逻辑分离** — 测试数据独立于用例代码，便于维护和复用
4. **横向可比较** — 同一场景用不同框架实现，为工具选型提供真实参考
5. **网络容错** — 内置导航超时与重试机制，适应不稳定网络环境

---

## 👤 关于作者

**顾翔 (Gu Xiang)** | Senior QA Engineer | 15+ 年测试经验

- 精通 Selenium / Robot Framework / Playwright / Maestro / JMeter
- 曾任 QA Lead / Scrum Master，带领跨时区测试团队
- 从 CT 医疗影像到 Web3 数字钱包，多行业交付经验
- 热衷探索 AI + 测试自动化的工程化落地

📧 guxi60@outlook.com
