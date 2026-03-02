#!/usr/bin/env python3
"""
数字员工交互记录系统
记录员工之间的协作和沟通
"""

import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def init_employee_db():
    """初始化员工数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建员工表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key TEXT UNIQUE,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            avatar TEXT,
            status TEXT DEFAULT 'idle',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建交互记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_employee TEXT,
            to_employee TEXT,
            message TEXT,
            task_type TEXT,
            status TEXT DEFAULT 'pending',
            result TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME
        )
    ''')
    
    # 创建任务表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            title TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 员工数据库初始化完成")

def register_employee(session_key, name, role, avatar):
    """注册员工"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO employees (session_key, name, role, avatar, status)
        VALUES (?, ?, ?, ?, 'idle')
    ''', (session_key, name, role, avatar))
    
    conn.commit()
    conn.close()
    print(f"✅ 员工注册：{name} ({role})")

def log_interaction(from_emp, to_emp, message, task_type='message'):
    """记录交互"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO interactions (from_employee, to_employee, message, task_type, status, created_at)
        VALUES (?, ?, ?, ?, 'pending', ?)
    ''', (from_emp, to_emp, message, task_type, datetime.now()))
    
    conn.commit()
    conn.close()

def get_recent_interactions(limit=50):
    """获取最近的交互记录"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT i.*, 
               e1.name as from_name, e1.avatar as from_avatar,
               e2.name as to_name, e2.avatar as to_avatar
        FROM interactions i
        LEFT JOIN employees e1 ON i.from_employee = e1.session_key
        LEFT JOIN employees e2 ON i.to_employee = e2.session_key
        ORDER BY i.created_at DESC
        LIMIT ?
    ''', (limit,))
    
    interactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return interactions

def get_employee_status():
    """获取员工状态"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM employees')
    employees = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return employees

if __name__ == '__main__':
    init_employee_db()
    
    # 注册员工
    register_employee('agent:main', '小龙虾主管', '协调员', '🦞')
    register_employee('agent:main:subagent:38c7e7e0', '文曲星', '内容专家', '✍️')
    register_employee('agent:main:subagent:6dd8cf1f', '数据通', '数据专家', '📊')
    
    print("✅ 员工系统初始化完成")
