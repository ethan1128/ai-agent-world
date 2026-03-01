#!/usr/bin/env python3
"""
AI 员工定时任务 - 多平台抓取
由 OpenClaw Heartbeat 触发，每 10 分钟执行一次
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def crawl_platforms():
    """执行多平台抓取"""
    print(f"🕷️  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行多平台抓取任务...")
    
    # 调用抓取脚本
    os.system(f"cd {os.path.dirname(__file__)} && python3 platform-crawler.py")
    
    # 记录执行日志
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (type, data)
        VALUES (?, ?)
    """, ('crawler_executed', json.dumps({
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'message': '多平台抓取任务执行完成'
    }, ensure_ascii=False)))
    conn.commit()
    conn.close()
    
    print(f"✅  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 多平台抓取任务完成")

if __name__ == '__main__':
    crawl_platforms()
