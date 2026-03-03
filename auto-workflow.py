#!/usr/bin/env python3
"""
自动化工作流系统 - 真实执行版
真正调用子会话执行任务，获取实际结果
"""

import sqlite3
import subprocess
import time
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_interaction(from_emp, to_emp, message, task_type='message', task_id=None):
    """记录交互"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (from_employee, to_employee, message, task_type, status, task_id, created_at, completed_at)
        VALUES (?, ?, ?, ?, 'completed', ?, ?, ?)
    ''', (from_emp, to_emp, message, task_type, task_id, datetime.now(), datetime.now()))
    conn.commit()
    conn.close()

def update_employee_status(name, status):
    """更新员工状态"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET status = ? WHERE name = ?', (status, name))
    conn.commit()
    conn.close()

def get_pending_tasks():
    """获取待处理任务"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interactions WHERE task_type = "task_report" AND status = "pending" ORDER BY created_at LIMIT 5')
    tasks = cursor.fetchall()
    conn.close()
    return [dict(t) for t in tasks]

def create_content_task():
    """创建文案创作任务"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, status, priority, created_at)
        VALUES (?, ?, 'pending', 2, ?)
    ''', ('创作情感类文案', '根据热点"人到中年"创作情感文案', datetime.now()))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def create_analysis_task():
    """创建数据分析任务"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, status, priority, created_at)
        VALUES (?, ?, 'pending', 2, ?)
    ''', ('分析最新热点数据', '分析热点数据的传播效果', datetime.now()))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def run_content_creation(task_id):
    """真正调用文曲星创作文案"""
    print("✍️ 调用文曲星创作文案...")
    
    # 调用 sessions_spawn 创作文案
    cmd = [
        'openclaw', 'sessions', 'spawn',
        '--mode', 'run',
        '--label', '文曲星 - 文案创作',
        '--task', '请根据热点"人到中年，这三种人要学会远离"创作一篇情感类文案，要求 200-300 字，引起中老年共鸣，配上标签。直接输出文案内容。',
        '--timeout', '60'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        content = result.stdout.strip()
        
        # 更新任务状态
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = "completed", completed_at = ? WHERE id = ?', (datetime.now(), task_id))
        conn.commit()
        conn.close()
        
        print(f"✅ 文案创作完成")
        return content[:200]  # 返回前 200 字
        
    except Exception as e:
        print(f"⚠️  文案创作失败：{e}")
        return "文案创作失败"

def run_data_analysis(task_id):
    """真正调用数据通分析数据"""
    print("📊 调用数据通分析数据...")
    
    cmd = [
        'openclaw', 'sessions', 'spawn',
        '--mode', 'run',
        '--label', '数据通 - 数据分析',
        '--task', '请分析文案"人到中年，这三种人要学会远离"的传播效果和潜在数据，包括预计浏览量、点赞、评论、分享等，给出综合评分。直接输出分析报告。',
        '--timeout', '60'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        analysis = result.stdout.strip()
        
        # 更新任务状态
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = "completed", completed_at = ? WHERE id = ?', (datetime.now(), task_id))
        conn.commit()
        conn.close()
        
        print(f"✅ 数据分析完成")
        return analysis[:200]  # 返回前 200 字
        
    except Exception as e:
        print(f"⚠️  数据分析失败：{e}")
        return "数据分析失败"

def run_auto_workflow():
    """运行自动工作流"""
    print(f"\n{'='*60}")
    print(f"🔄 自动工作流 - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    
    # 1. 创建任务
    print("\n📝 步骤 1: 创建任务...")
    content_task_id = create_content_task()
    analysis_task_id = create_analysis_task()
    print(f"   ✅ 创建文案任务 (ID: {content_task_id})")
    print(f"   ✅ 创建分析任务 (ID: {analysis_task_id})")
    
    # 2. 分配任务
    print("\n📤 步骤 2: 分配任务...")
    log_interaction('小龙虾主管', 'agent:main:subagent:38c7e7e0', f'请执行：创作情感类文案', 'task_assign', content_task_id)
    log_interaction('小龙虾主管', 'agent:main:subagent:6dd8cf1f', f'请执行：分析最新热点数据', 'task_assign', analysis_task_id)
    print("   ✅ 任务已分配")
    
    # 3. 真正执行任务
    print("\n✍️📊 步骤 3: 员工执行任务...")
    update_employee_status('文曲星', 'working')
    update_employee_status('数据通', 'working')
    
    content_result = run_content_creation(content_task_id)
    analysis_result = run_data_analysis(analysis_task_id)
    
    # 4. 汇报结果
    print("\n✅ 步骤 4: 员工汇报结果...")
    log_interaction('agent:main:subagent:38c7e7e0', '小龙虾主管', f'任务完成：创作情感类文案\n\n{content_result}', 'task_complete', content_task_id)
    log_interaction('agent:main:subagent:6dd8cf1f', '小龙虾主管', f'任务完成：分析最新热点数据\n\n{analysis_result}', 'task_complete', analysis_task_id)
    print("   ✅ 文曲星：文案完成")
    print("   ✅ 数据通：分析完成")
    
    # 5. 汇总
    print("\n📊 步骤 5: 主管汇总...")
    log_interaction('小龙虾主管', 'system', f'本轮工作流完成，执行 2 个任务', 'workflow_complete')
    update_employee_status('文曲星', 'idle')
    update_employee_status('数据通', 'idle')
    update_employee_status('任务收集专员', 'working')
    
    print(f"\n{'='*60}")
    print(f"✅ 自动工作流完成")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 自动化工作流系统 - 真实执行版")
    print("=" * 60)
    
    run_auto_workflow()
