# 🤖 AI 员工世界 - 定时任务配置

**目标**：每小时自动执行一次完整工作流

---

## 📋 方案选择

### 方案 A：OpenClaw Cron（推荐）

使用 OpenClaw 的 cron 功能，每小时触发一次 workflow.py

### 方案 B：系统 Cron

使用 Linux 系统级 cron 任务

### 方案 C：Heartbeat

使用 OpenClaw 的 heartbeat 功能

---

## ✅ 推荐：方案 A（OpenClaw Cron）

### 配置方法

在 OpenClaw 中创建 cron 任务：

```bash
openclaw cron add --name "AI 员工工作流" --schedule "0 * * * *" --command "cd ~/.openclaw/workspace/ai-agents-world && python3 workflow.py"
```

### 执行时间

- 每小时整点执行（0 分）
- 例如：17:00, 18:00, 19:00...

### 优点

- ✅ OpenClaw 原生支持
- ✅ 执行日志记录在 OpenClaw
- ✅ 失败有通知
- ✅ 可以随时暂停/恢复

---

## 📝 手动触发脚本

创建一个简单的手动触发脚本：

```bash
#!/bin/bash
# ai-workers-start.sh
cd ~/.openclaw/workspace/ai-agents-world
python3 workflow.py >> logs/workflow-$(date +%Y%m%d-%H%M%S).log 2>&1
```

---

## 📊 监控和日志

### 日志位置

```
~/.openclaw/workspace/ai-agents-world/logs/
├── workflow-20260301-170000.log
├── workflow-20260301-180000.log
└── ...
```

### 查看最新日志

```bash
tail -f logs/workflow-$(date +%Y%m%d)*.log
```

---

## 🎯 执行策略

### 第 1 周：手动触发
- 每天手动执行 1-2 次
- 观察 AI 员工输出质量
- 调整 prompt 优化结果

### 第 2 周：半自动
- 设置 cron 每小时执行
- 人工审核产出内容
- 筛选优质内容发布

### 第 3 周：全自动
- cron 自动执行
- 自动发布优质内容
- 只需要监控数据

---

**维护**：小龙虾一号 | **创建**：2026-03-01
