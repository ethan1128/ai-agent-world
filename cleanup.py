#!/usr/bin/env python3
"""
数据清理脚本
每天执行一次，清理 30 天前的旧数据
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def cleanup_old_data(days=30):
    """清理 N 天前的数据"""
    conn = get_db()
    cursor = conn.cursor()
    
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"🧹 开始清理 {days} 天前的数据（{cutoff_str}之前）...")
    
    # 清理 platform_monitor 表
    cursor.execute("""
        DELETE FROM platform_monitor 
        WHERE crawl_time < ?
    """, (cutoff_str,))
    deleted_monitor = cursor.rowcount
    
    # 清理 activity_log 表
    cursor.execute("""
        DELETE FROM activity_log 
        WHERE created_at < ?
    """, (cutoff_str,))
    deleted_logs = cursor.rowcount
    
    # 清理 events 表
    cursor.execute("""
        DELETE FROM events 
        WHERE created_at < ?
    """, (cutoff_str,))
    deleted_events = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"✅ 清理完成")
    print(f"   - platform_monitor: {deleted_monitor} 条")
    print(f"   - activity_log: {deleted_logs} 条")
    print(f"   - events: {deleted_events} 条")
    
    return {
        'platform_monitor': deleted_monitor,
        'activity_log': deleted_logs,
        'events': deleted_events
    }

if __name__ == '__main__':
    print("=" * 60)
    print("🧹 数据清理任务")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    cleanup_old_data(30)
    
    print()
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
