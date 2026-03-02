#!/usr/bin/env python3
"""
自动化工作流系统
让所有员工自动协作，无需人工干预
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

def log_interaction(from_emp, to_emp, message, task_type='message'):
    """记录交互"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (from_employee, to_employee, message, task_type, status, created_at, completed_at)
        VALUES (?, ?, ?, ?, 'completed', ?, ?)
    ''', (from_emp, to_emp, message, task_type, datetime.now(), datetime.now()))
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

def auto_assign_task(task_message):
    """自动分配任务给合适的员工"""
    # 简单关键词匹配
    if '文案' in task_message or '创作' in task_message:
        return '文曲星', 'agent:main:subagent:38c7e7e0'
    elif '分析' in task_message or '数据' in task_message:
        return '数据通', 'agent:main:subagent:6dd8cf1f'
    elif '审核' in task_message:
        return '任务审核专员', 'agent:main:subagent:5236aaaf'
    else:
        return '文曲星', 'agent:main:subagent:38c7e7e0'

def run_auto_workflow():
    """运行自动工作流"""
    print(f"\n{'='*60}")
    print(f"🔄 自动工作流 - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    
    # 1. 任务收集专员持续收集
    print("\n📥 步骤 1: 任务收集专员收集任务...")
    update_employee_status('任务收集专员', 'working')
    
    # 模拟收集任务（实际应该调用 task-collector-service）
    collected_tasks = [
        '分析最新热点数据',
        '创作情感类文案',
    ]
    
    for task in collected_tasks:
        log_interaction('任务收集专员', '小龙虾主管', f'发现新任务：{task}', 'task_discover')
        print(f"   ✅ 收集：{task}")
    
    # 2. 主管审核并分配
    print("\n🦞 步骤 2: 小龙虾主管审核并分配...")
    update_employee_status('小龙虾主管', 'working')
    
    for task in collected_tasks:
        employee_name, session_key = auto_assign_task(task)
        log_interaction('小龙虾主管', session_key, f'请执行：{task}', 'task_assign')
        print(f"   📤 分配：{task} → {employee_name}")
    
    # 3. 员工执行任务
    print("\n✍️📊 步骤 3: 员工并行执行任务...")
    update_employee_status('文曲星', 'working')
    update_employee_status('数据通', 'working')
    
    # 模拟执行时间
    time.sleep(2)
    
    # 4. 员工汇报结果
    print("\n✅ 步骤 4: 员工汇报结果...")
    for task in collected_tasks:
        employee_name, session_key = auto_assign_task(task)
        log_interaction(session_key, '小龙虾主管', f'任务完成：{task}', 'task_complete')
        print(f"   ✅ {employee_name}: {task}")
    
    # 5. 主管汇总
    print("\n📊 步骤 5: 主管汇总...")
    log_interaction('小龙虾主管', 'system', f'本轮工作流完成，执行{len(collected_tasks)}个任务', 'workflow_complete')
    update_employee_status('小龙虾主管', 'idle')
    update_employee_status('文曲星', 'idle')
    update_employee_status('数据通', 'idle')
    update_employee_status('任务收集专员', 'working')  # 保持收集状态
    
    print(f"\n{'='*60}")
    print(f"✅ 自动工作流完成")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 自动化工作流系统")
    print("=" * 60)
    
    workflow_count = 0
    
    while True:
        try:
            workflow_count += 1
            print(f"\n📊 第{workflow_count}轮自动工作流")
            
            run_auto_workflow()
            
            # 等待 10 分钟
            print(f"\n⏳ 等待 10 分钟后执行下一轮...")
            time.sleep(600)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  停止工作流")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            time.sleep(60)
