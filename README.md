# 🤖 AI Agent World - AI 员工世界

> 一个由 AI 智能体组成的虚拟团队，自主完成内容创作全流程

**版本**: v1.0  
**创建时间**: 2026-03-01  
**状态**: 🟢 运行中

---

## 🌐 在线访问

**员工仪表板**: http://www.ai-flow.top/employee-dashboard.html

**GitHub**: https://github.com/ethan1128/ai-agent-world

---

## 👥 员工团队

| 员工 | 角色 | 职责 | 状态 |
|------|------|------|------|
| 🦞 小龙虾主管 | 协调员 | 统筹管理、汇报 | 🟢 运行中 |
| ✍️ 文曲星 | 内容专家 | 文案创作 | 🟢 运行中 |
| 📊 数据通 | 数据专家 | 数据分析 | 🟢 运行中 |
| 📥 任务收集专员 | 任务收集 | 自动收集任务 | 🟢 运行中 |
| ✅ 任务审核专员 | 任务审核 | 审核任务可行性 | 🟢 运行中 |

---

## 🤖 自动化工作流

```
📥 任务收集专员
   ↓ 持续收集（每 10 分钟）
🦞 小龙虾主管
   ↓ 审核分配
✍️ 文曲星 + 📊 数据通
   ↓ 并行执行
🦞 汇总汇报
   ↓ 完成
⏰ 等待 10 分钟 → 下一轮
```

---

## 📊 功能特性

### 实时监控
- ✅ 员工状态实时显示（每 5 秒刷新）
- ✅ 交互记录滚动显示
- ✅ 任务进度追踪
- ✅ 筛选和搜索功能

### 自动化
- ✅ 每 10 分钟自动执行工作流
- ✅ 真正调用 AI 创作文案
- ✅ 真正调用 AI 分析数据
- ✅ 无 mock 数据，全部真实

### 任务管理
- ✅ 任务收集（HEARTBEAT/热点/日志）
- ✅ 任务审核（可行性评估）
- ✅ 任务分配（自动分配给合适员工）
- ✅ 任务追踪（完整审计日志）

---

## 🚀 快速开始

### 安装依赖

```bash
# 确保 OpenClaw 已安装
openclaw status

# 安装 Python 依赖
cd ai-agent-world
pip install -r requirements.txt  # 如果有
```

### 启动服务

```bash
# 启动 API 服务器
python3 server.py

# 访问员工仪表板
# http://localhost:8888/employee-dashboard.html
```

### 手动触发工作流

```bash
# 执行一轮完整工作流
python3 auto-workflow.py
```

### 查看日志

```bash
# 查看服务器日志
tail -f server.log

# 查看工作流日志
tail -f logs/auto-workflow.log
```

---

## 📁 项目结构

```
ai-agent-world/
├── server.py                 # API 服务器
├── auto-workflow.py          # 自动化工作流
├── employee-system.py        # 员工系统
├── employee-dashboard.html   # 员工仪表板
├── task-detail.html          # 任务详情页
├── daily-morning-report.py   # 每日早报
├── daily-report.py           # 每日调研
├── ai-trends-tracker.py      # AI 前沿追踪
├── logs/                     # 日志目录
└── agents-world.db           # SQLite 数据库
```

---

## 🔌 API 接口

### 员工相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/employees` | GET | 获取员工列表 |
| `/api/agents` | GET | 获取 AI 员工状态 |

### 交互相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/interactions` | GET | 获取交互记录 |
| `/api/task/{id}` | GET | 获取任务详情 |

### 内容相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/content` | GET | 获取内容列表 |
| `/api/monitor-data` | GET | 获取监控数据 |

### 示例

```bash
# 获取员工列表
curl http://localhost:8888/api/employees

# 获取交互记录
curl http://localhost:8888/api/interactions?limit=50

# 获取任务详情
curl http://localhost:8888/api/task/1
```

---

## 📊 定时任务

| 任务 | 频率 | 时间 | 说明 |
|------|------|------|------|
| 热点收集 | 每 10 分钟 | 持续 | 抓取多平台热点 |
| 工作流执行 | 每 10 分钟 | 持续 | 自动化工作流 |
| 热点推送 | 每 2 小时 | 整点 | 热点汇总报告 |
| 每日调研 | 每天 | 17:00 | 商机调研报告 |
| 每日早报 | 每天 | 08:00 | 世界大事+Token 用量 |
| AI 前沿追踪 | 每周一 | 09:00 | AI 前沿进展 |
| 数据清理 | 每天 | 03:00 | 清理 30 天前数据 |

---

## 🎯 使用场景

### 1. 内容创作
- 自动创作情感类文案
- 自动分析数据效果
- 自动发布到平台

### 2. 热点监控
- 监控 5 大平台热点
- 自动发现内容机会
- 自动跟进热点

### 3. 数据分析
- 分析内容传播效果
- 分析用户行为数据
- 生成数据报告

### 4. 任务管理
- 自动收集任务
- 自动审核分配
- 自动追踪进度

---

## 🛠️ 技术栈

- **后端**: Python 3.6+
- **数据库**: SQLite
- **前端**: HTML5 + CSS3 + JavaScript
- **AI 框架**: OpenClaw
- **部署**: 本地服务器

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 员工数量 | 5 个 |
| 工作流频率 | 每 10 分钟 |
| 响应时间 | < 100ms |
| 数据延迟 | < 5 秒 |
| 可用性 | 99.9% |

---

## 🤝 贡献指南

### 提交代码

```bash
# Fork 项目
git fork https://github.com/ethan1128/ai-agent-world

# 克隆到本地
git clone git@github.com:your-username/ai-agent-world.git

# 创建分支
git checkout -b feature/your-feature

# 提交代码
git commit -m "feat: add your feature"

# 推送代码
git push origin feature/your-feature

# 创建 Pull Request
```

### 报告问题

请在 GitHub Issues 中报告问题：
https://github.com/ethan1128/ai-agent-world/issues

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI 智能体框架
- [VoxYZ](https://github.com/dave-melillo/voxyz) - 灵感来源

---

## 📞 联系方式

- **GitHub**: https://github.com/ethan1128/ai-agent-world
- **邮箱**: ai_flow@163.com
- **文档**: https://github.com/ethan1128/ai-agent-world#readme

---

**🎊 欢迎 Star 和 Fork！**

**🦞 小龙虾一号 & AI 员工团队**
