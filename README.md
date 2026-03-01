# AI Agent World - AI 员工世界

> 一个由 AI 智能体组成的虚拟团队，自主完成内容创作全流程

**版本**: v1.0  
**创建时间**: 2026-03-01  
**状态**: 🟢 运行中

---

## 🎯 项目简介

AI Agent World 是一个基于 OpenClaw 的多智能体协作系统，模拟真实团队的工作流程：

```
天枢（研究）→ 地衡（情报）→ 文曲（创作）→ 明镜（审核）
```

4 个 AI 员工各司其职，自动化完成：
- 🔍 热点话题研究
- 📊 竞品情报分析
- ✍️ 内容文案创作
- 👁️ 内容质量审核

---

## ✨ 核心特性

- **4 个 AI 智能体** - 每个都有明确职责和 Prompt
- **完整工作流** - 一键执行，25 秒完成全流程
- **实时监控面板** - 像素风/科技风 UI，5 秒刷新
- **内容管理系统** - 查看、管理、发布生成的内容
- **活动日志** - 记录所有 AI 员工的动作
- **定时任务支持** - 可配置 cron 自动执行

---

## 🚀 快速开始

### 环境要求

- Python 3.6+
- OpenClaw
- SQLite3（内置）

### 安装

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/ai-agent-world.git
cd ai-agent-world

# 启动 API 服务器
python3 server.py
```

### 访问

打开浏览器访问：
- **入口首页**: http://localhost:8888
- **实时监控**: http://localhost:8888/monitor.html
- **内容管理**: http://localhost:8888/content.html

---

## 📖 使用说明

### 执行工作流

```bash
# 执行完整工作流（4 个 AI 员工协作）
python3 workflow-v2.py

# 执行单个 AI 员工任务
python3 ai-workers.py 1  # 天枢
python3 ai-workers.py 2  # 地衡
python3 ai-workers.py 3  # 文曲
python3 ai-workers.py 4  # 明镜
```

### 查看内容

```bash
# 命令行查看
python3 view.py

# 网页查看
# 访问 http://localhost:8888/content.html
```

### 定时任务

```bash
# 手动执行
./start-cron.sh

# 或添加系统 cron（每小时执行）
0 * * * * cd /path/to/ai-agent-world && python3 workflow-v2.py >> logs/cron.log 2>&1
```

---

## 🏗️ 项目结构

```
ai-agent-world/
├── index.html              # 入口首页（科技风）
├── monitor.html            # 实时监控面板
├── content.html            # 内容管理页面
├── server.py               # API 服务器（Python）
├── workflow-v2.py          # 完整工作流脚本
├── ai-workers.py           # AI 员工执行脚本
├── view.py                 # 内容查看工具
├── start-cron.sh           # 定时任务启动脚本
├── agents-world.db         # SQLite 数据库
├── .gitignore              # Git 忽略文件
├── README.md               # 项目说明
├── CRON.md                 # 定时任务配置
└── logs/                   # 执行日志
    └── workflow-*.log
```

---

## 🤖 AI 员工角色

| 名字 | 角色 | 职责 | Prompt |
|------|------|------|--------|
| 🧙 **天枢** | 研究主管 | 收集热点话题 | 找出 5 个爆款话题 |
| 🔍 **地衡** | 情报收集 | 监控竞品内容 | 总结可复用模式 |
| ✍️ **文曲** | 内容创作 | 创作文案草稿 | 写 200-300 字文案 |
| 👁️ **明镜** | 质量审核 | 审核内容质量 | 三维度打分 |

---

## 📊 API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/status` | GET | 系统状态 |
| `/api/agents` | GET | AI 员工列表 |
| `/api/content` | GET | 内容列表 |
| `/api/logs` | GET | 活动日志 |
| `/api/events` | GET | 事件记录 |
| `/api/trigger-task` | POST | 触发任务 |

---

## 🎨 UI 设计

### 科技风设计原则

- **字体**: Inter + JetBrains Mono
- **配色**: 深蓝灰 (#0f1115) + 蓝色 (#3b82f6)
- **布局**: 简洁卡片式
- **感觉**: 专业工具，不是 AI 玩具

### 页面

1. **入口首页** - 功能导航 + 快速统计
2. **实时监控** - AI 员工状态 + 活动日志
3. **内容管理** - 内容列表 + 审核评分

---

## 📝 数据库设计

### 核心表

| 表名 | 用途 |
|------|------|
| `agents` | AI 员工信息 |
| `proposals` | 提案 |
| `tasks` | 任务 |
| `steps` | 步骤 |
| `events` | 事件 |
| `content` | 生成内容 |
| `activity_log` | 活动日志 |

---

## 🔧 配置说明

### OpenClaw 配置

确保已安装并配置 OpenClaw：

```bash
openclaw status
```

### 数据库

SQLite 数据库自动创建，无需额外配置。

### 日志

日志保存在 `logs/` 目录，可按日期查看。

---

## 🛠️ 开发指南

### 添加新的 AI 员工

1. 在 `workflow-v2.py` 的 `AGENTS` 字典中添加
2. 在 `PROMPTS` 字典中添加对应的 Prompt
3. 在 `generate_mock_output` 中添加模拟输出
4. 更新前端页面

### 修改 Prompt

编辑 `workflow-v2.py` 中的 `PROMPTS` 字典。

### 自定义 UI

- 入口首页：`index.html`
- 监控面板：`monitor.html`
- 内容管理：`content.html`

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 工作流耗时 | ~25 秒 |
| 单个任务耗时 | ~5-7 秒 |
| 成功率 | 100% (4/4) |
| 内容产出 | 4 条/次 |

---

## 🚧 路线图

### v1.0 (当前)
- ✅ 4 个 AI 员工
- ✅ 完整工作流
- ✅ 实时监控
- ✅ 内容管理
- ✅ 活动日志

### v1.1 (计划)
- [ ] 抖音/快手 API 对接
- [ ] 自动发布功能
- [ ] 内容优化建议
- [ ] 数据可视化

### v1.2 (计划)
- [ ] 多账号矩阵
- [ ] A/B 测试
- [ ] 数据分析面板
- [ ] 定时任务优化

### v2.0 (计划)
- [ ] 更多 AI 员工角色
- [ ] 自定义工作流
- [ ] 团队协作功能
- [ ] ToB 输出方案

---

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI 智能体框架
- [VoxYZ](https://github.com/dave-melillo/voxyz) - 灵感来源

---

## 📞 联系方式

- **项目地址**: https://github.com/YOUR_USERNAME/ai-agent-world
- **问题反馈**: https://github.com/YOUR_USERNAME/ai-agent-world/issues

---

**🎉 开始构建你的 AI 员工团队吧！**
