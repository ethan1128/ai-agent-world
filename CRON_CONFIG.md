# AI 员工世界 - 定时任务配置

## 当前配置

### 多平台抓取任务
- **频率**：每 10 分钟
- **脚本**：`platform-crawler.py`
- **状态**：✅ 已配置

### AI 员工工作流
- **频率**：待配置（建议每小时）
- **脚本**：`workflow-v2.py`
- **状态**：⏳ 待配置

### 数据清理
- **频率**：待配置（建议每天凌晨 3 点）
- **脚本**：`cleanup.py`（待创建）
- **状态**：⏳ 待配置

---

## 配置方法

### 方法 1：使用系统 crontab

```bash
# 编辑 crontab
crontab -e

# 添加任务
*/10 * * * * cd ~/.openclaw/workspace/ai-agents-world && python3 platform-crawler.py >> logs/crawler.log 2>&1
0 * * * * cd ~/.openclaw/workspace/ai-agents-world && python3 workflow-v2.py >> logs/workflow.log 2>&1
0 3 * * * cd ~/.openclaw/workspace/ai-agents-world && python3 cleanup.py >> logs/cleanup.log 2>&1
```

### 方法 2：使用 OpenClaw Heartbeat

编辑 `~/.openclaw/workspace/HEARTBEAT.md`：

```markdown
# 多平台内容抓取
每 10 分钟执行一次

# AI 员工工作流
每小时执行一次
```

---

## 监控和日志

### 查看抓取日志
```bash
tail -f logs/crawler.log
```

### 查看工作流日志
```bash
tail -f logs/workflow.log
```

### 查看数据库记录
```bash
sqlite3 agents-world.db "SELECT type, data, created_at FROM events ORDER BY created_at DESC LIMIT 10;"
```

---

## 告警配置

### 任务失败告警
如果连续 3 次抓取失败，发送通知。

### 数据异常告警
如果抓取数据为 0，发送通知。

---

**维护**：AI Agent World Team  
**最后更新**：2026-03-01
