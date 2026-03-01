#!/usr/bin/env python3
"""
AI 员工世界 - 内容查看工具
查看 AI 员工生成的文案和审核结果
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

def view_content():
    """查看生成的内容"""
    conn = get_db()
    cursor = conn.cursor()
    
    print("=" * 80)
    print("📝 生成的内容")
    print("=" * 80)
    
    cursor.execute("""
        SELECT c.*, a.name as creator_name
        FROM content c
        LEFT JOIN agents a ON c.created_by = a.id
        ORDER BY c.created_at DESC
        LIMIT 10
    """)
    
    contents = cursor.fetchall()
    
    if not contents:
        print("❌ 暂无生成的内容")
        print("\n💡 提示：运行 python3 workflow.py 生成内容")
    else:
        for i, content in enumerate(contents, 1):
            print(f"\n【{i}】{content['title']}")
            print(f"创作者：{content['creator_name']}")
            print(f"平台：{content['platform']}")
            print(f"状态：{content['status']}")
            print(f"时间：{content['created_at']}")
            print(f"数据：{content['body'][:200] if content['body'] else '(空)'}...")
            print("-" * 80)
    
    conn.close()

def view_workflow_results():
    """查看工作流执行结果"""
    conn = get_db()
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("📊 工作流执行记录")
    print("=" * 80)
    
    cursor.execute("""
        SELECT * FROM events 
        WHERE type = 'workflow_completed' 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    events = cursor.fetchall()
    
    for event in events:
        data = json.loads(event['data'])
        print(f"\n⏰ 时间：{event['created_at']}")
        print(f"⏱️  耗时：{data['duration']:.1f}秒")
        print(f"✅ 成功：{data['success']}/{data['total']}")
        print("-" * 80)
    
    conn.close()

def view_recent_logs():
    """查看最近活动日志"""
    conn = get_db()
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("📋 最近活动日志")
    print("=" * 80)
    
    cursor.execute("""
        SELECT l.*, a.name as agent_name, a.avatar
        FROM activity_log l
        LEFT JOIN agents a ON l.agent_id = a.id
        ORDER BY l.created_at DESC
        LIMIT 20
    """)
    
    logs = cursor.fetchall()
    
    for log in logs:
        emoji = {'working': '🔄', 'completed': '✅', 'failed': '❌', 'system': '⚙️'}.get(log['action'], '📝')
        print(f"{emoji} {log['created_at']} | {log['agent_name']} {log['avatar']} | {log['message']}")
    
    conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'content':
            view_content()
        elif cmd == 'workflow':
            view_workflow_results()
        elif cmd == 'logs':
            view_recent_logs()
        else:
            print("用法：python3 view.py [content|workflow|logs]")
    else:
        # 显示所有内容
        view_content()
        view_workflow_results()
        view_recent_logs()
