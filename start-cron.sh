#!/bin/bash
# AI 员工世界 - 定时任务启动脚本

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/workflow-$(date +%Y%m%d-%H%M%S).log"

echo "🚀 AI 员工工作流启动 - $(date)"
echo "📝 日志文件：$LOG_FILE"

# 执行工作流
python3 workflow.py 2>&1 | tee "$LOG_FILE"

echo "✅ 工作流完成 - $(date)"
