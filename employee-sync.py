#!/usr/bin/env python3
"""
员工状态同步服务
确保数据库中的员工状态实时同步
"""

import sqlite3
import json
import subprocess
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sync_employees_from_sessions():
    """从 OpenClaw sessions 同步员工"""
    print("🔄 同步员工状态...")
    
    try:
        # 获取当前会话列表
        result = subprocess.run(
            ['openclaw', 'sessions', 'list', '--json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            sessions = json.loads(result.stdout)
            
            conn = get_db()
            cursor = conn.cursor()
            
            for session in sessions:
                session_key = session.get('sessionKey', '')
                label = session.get('label', '')
                
                if 'subagent' in session_key:
                    # 更新员工状态
                    cursor.execute('''
                        UPDATE employees 
                        SET status = 'working', updated_at = ?
                        WHERE session_key = ?
                    ''', (datetime.now(), session_key))
                    
                    if cursor.rowcount == 0:
                        # 新员工，添加到数据库
                        cursor.execute('''
                            INSERT INTO employees (session_key, name, role, avatar, status, created_at)
                            VALUES (?, ?, ?, ?, 'working', ?)
                        ''', (session_key, label, 'AI 员工', '🤖', datetime.now()))
            
            conn.commit()
            conn.close()
            print(f"✅ 同步完成")
        else:
            print(f"⚠️  获取会话失败")
    except Exception as e:
        print(f"❌ 同步失败：{e}")

def ensure_all_employees_registered():
    """确保所有已知员工都在数据库中"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 已知的员工会话
    known_employees = [
        ('agent:main', '小龙虾主管', '协调员', '🦞'),
        ('agent:main:subagent:99eb750e', '文曲星', '内容专家', '✍️'),
        ('agent:main:subagent:1636204c', '数据通', '数据专家', '📊'),
        ('agent:main:subagent:4f20a4b3', '任务收集专员', '任务收集', '📥'),
        ('agent:main:subagent:5236aaaf', '任务审核专员', '任务审核', '✅'),
    ]
    
    for session_key, name, role, avatar in known_employees:
        cursor.execute('''
            INSERT OR REPLACE INTO employees (session_key, name, role, avatar, status, created_at)
            VALUES (?, ?, ?, ?, 'idle', ?)
        ''', (session_key, name, role, avatar, datetime.now()))
    
    conn.commit()
    conn.close()
    print("✅ 员工注册检查完成")

if __name__ == '__main__':
    print("=" * 60)
    print("🔄 员工状态同步服务")
    print("=" * 60)
    
    ensure_all_employees_registered()
    sync_employees_from_sessions()
    
    print("=" * 60)
