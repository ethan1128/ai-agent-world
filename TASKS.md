# AI 员工世界 - 定时任务配置

## 任务列表

### 1. 多平台内容抓取
- **频率**：每 10 分钟
- **任务**：抓取 5 大平台热门内容
- **脚本**：`platform-crawler.py`

### 2. AI 员工工作流
- **频率**：每小时
- **任务**：执行完整工作流（研究→情报→创作→审核）
- **脚本**：`workflow-v2.py`

### 3. 数据清理
- **频率**：每天凌晨 3 点
- **任务**：清理 30 天前的旧数据
- **脚本**：`cleanup.py`

---

## OpenClaw 定时任务配置

### 使用 Heartbeat

在 `HEARTBEAT.md` 中添加：

```markdown
# 每 10 分钟检查一次
- [ ] 执行多平台抓取
```

### 使用 Cron

```bash
# 多平台抓取（每 10 分钟）
*/10 * * * * cd ~/.openclaw/workspace/ai-agents-world && python3 platform-crawler.py >> logs/crawler.log 2>&1

# AI 员工工作流（每小时）
0 * * * * cd ~/.openclaw/workspace/ai-agents-world && python3 workflow-v2.py >> logs/workflow.log 2>&1

# 数据清理（每天 3 点）
0 3 * * * cd ~/.openclaw/workspace/ai-agents-world && python3 cleanup.py >> logs/cleanup.log 2>&1
```

---

## 任务监控

### 查看执行日志

```bash
# 多平台抓取日志
tail -f logs/crawler.log

# 工作流日志
tail -f logs/workflow.log

# 清理日志
tail -f logs/cleanup.log
```

### 查看任务状态

```bash
# 查看 cron 任务
crontab -l

# 查看进程
ps aux | grep python3
```

---

## 告警配置

### 任务失败告警

如果任务连续失败 3 次，发送通知：

```python
# 在脚本中添加
if failed_count >= 3:
    send_alert("多平台抓取任务连续失败 3 次")
```

### 数据异常告警

如果抓取数据为 0，发送通知：

```python
if total_count == 0:
    send_alert("本次抓取未获取到任何数据")
```

---

**维护**：AI Agent World Team  
**最后更新**：2026-03-01
