#!/usr/bin/env python3
"""
任务管理系统
负责任务的收集、审核、分配、追踪
"""

import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def init_task_db():
    """初始化任务数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建任务表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            source TEXT,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT 'pending',
            assigned_to TEXT,
            created_by TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            reviewed_at DATETIME,
            started_at DATETIME,
            completed_at DATETIME,
            review_result TEXT,
            review_comment TEXT
        )
    ''')
    
    # 创建任务流转表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_flow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            from_employee TEXT,
            to_employee TEXT,
            action TEXT,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 任务数据库初始化完成")

def create_task(title, description, source='manual', priority=1, created_by='agent:main'):
    """创建任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (title, description, source, priority, created_by, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    ''', (title, description, source, priority, created_by))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ 任务已创建：{title} (ID: {task_id})")
    return task_id

def review_task(task_id, result, comment='', reviewer='agent:main:subagent:xxx'):
    """审核任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    status = 'approved' if result == 'approved' else 'rejected'
    
    cursor.execute('''
        UPDATE tasks 
        SET status = ?, review_result = ?, review_comment = ?, reviewed_at = ?
        WHERE id = ?
    ''', (status, result, comment, datetime.now(), task_id))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 任务已审核：{task_id} - {result}")

def assign_task(task_id, assigned_to):
    """分配任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks 
        SET status = 'assigned', assigned_to = ?, started_at = ?
        WHERE id = ?
    ''', (assigned_to, datetime.now(), task_id))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 任务已分配：{task_id} → {assigned_to}")

def complete_task(task_id, result=''):
    """完成任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks 
        SET status = 'completed', completed_at = ?
        WHERE id = ?
    ''', (datetime.now(), task_id))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 任务已完成：{task_id}")

def log_task_flow(task_id, from_emp, to_emp, action, message):
    """记录任务流转"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO task_flow (task_id, from_employee, to_employee, action, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (task_id, from_emp, to_emp, action, message))
    
    conn.commit()
    conn.close()

def get_pending_tasks():
    """获取待审核任务"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE status = "pending" ORDER BY priority DESC, created_at')
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return tasks

def get_approved_tasks():
    """获取待分配任务"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE status = "approved" ORDER BY priority DESC')
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return tasks

def demo_task_system():
    """演示任务管理系统"""
    print("=" * 60)
    print("📋 任务管理系统演示")
    print("=" * 60)
    
    # 初始化数据库
    init_task_db()
    
    # 1. 任务收集专员创建任务
    print("\n📝 步骤 1: 任务收集")
    task1_id = create_task(
        title='根据热点创作文案',
        description='根据"人到中年"热点创作情感文案',
        source='热点监控',
        priority=2,
        created_by='agent:main:subagent:4f20a4b3'  # 任务收集专员
    )
    
    log_task_flow(task1_id, '任务收集专员', '任务审核专员', 'submit_review', '请审核这个任务')
    
    task2_id = create_task(
        title='分析文案传播效果',
        description='分析文案的预计浏览量和互动数据',
        source='任务依赖',
        priority=1,
        created_by='agent:main:subagent:4f20a4b3'
    )
    
    log_task_flow(task2_id, '任务收集专员', '任务审核专员', 'submit_review', '请审核这个任务')
    
    # 2. 任务审核专员审核
    print("\n📝 步骤 2: 任务审核")
    review_task(
        task1_id,
        result='approved',
        comment='✅ 可行性高，预计 5 分钟完成，风险低',
        reviewer='agent:main:subagent:5236aaaf'  # 任务审核专员
    )
    
    log_task_flow(task1_id, '任务审核专员', '小龙虾主管', 'review_complete', '任务审核通过')
    
    review_task(
        task2_id,
        result='approved',
        comment='✅ 可行性高，预计 5 分钟完成，风险低',
        reviewer='agent:main:subagent:5236aaaf'
    )
    
    log_task_flow(task2_id, '任务审核专员', '小龙虾主管', 'review_complete', '任务审核通过')
    
    # 3. 主管分配任务
    print("\n📝 步骤 3: 任务分配")
    assign_task(task1_id, 'agent:main:subagent:99eb750e')  # 文曲星
    log_task_flow(task1_id, '小龙虾主管', '文曲星', 'assign_task', '请创作文案')
    
    assign_task(task2_id, 'agent:main:subagent:1636204c')  # 数据通
    log_task_flow(task2_id, '小龙虾主管', '数据通', 'assign_task', '请分析数据')
    
    # 4. 员工执行任务
    print("\n📝 步骤 4: 任务执行（并行）")
    print("   ✍️ 文曲星正在创作文案...")
    print("   📊 数据通正在分析数据...")
    
    # 5. 完成任务
    print("\n📝 步骤 5: 任务完成")
    complete_task(task1_id)
    log_task_flow(task1_id, '文曲星', '小龙虾主管', 'task_complete', '文案已创作完成')
    
    complete_task(task2_id)
    log_task_flow(task2_id, '数据通', '小龙虾主管', 'task_complete', '数据分析完成')
    
    # 6. 汇总汇报
    print("\n📝 步骤 6: 汇总汇报")
    print("   🦞 小龙虾主管：两个任务都已完成")
    print("   ✅ 文案 + 数据分析 = 完整方案")
    
    print("\n" + "=" * 60)
    print("🎉 任务管理系统演示完成！")
    print("=" * 60)

if __name__ == '__main__':
    demo_task_system()
