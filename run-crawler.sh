#!/bin/bash
# AI 员工世界 - 多平台抓取定时任务
# 每 10 分钟执行一次

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/crawler-$(date +%Y%m%d).log"

echo "🕷️  [$(date)] 开始抓取多平台内容..." >> "$LOG_FILE"

cd "$(dirname "$0")"
python3 platform-crawler.py >> "$LOG_FILE" 2>&1

echo "✅  [$(date)] 抓取完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
