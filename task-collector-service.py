#!/usr/bin/env python3
"""
任务收集专员 - 持续运行
自动收集任务，保持工作状态
"""

import sqlite3
import subprocess
import time
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')
SESSION_KEY = 'agent:main:subagent:4f20a4b3'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def update_employee_status(status):
    """更新员工状态"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET status = ? WHERE session_key = ?', (status, SESSION_KEY))
    conn.commit()
    conn.close()

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

def collect_from_heartbeat():
    """从 HEARTBEAT.md 收集任务"""
    try:
        with open('/home/admin/.openclaw/workspace/HEARTBEAT.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.strip() and not content.startswith('#'):
            return {
                'title': 'HEARTBEAT 任务',
                'source': 'HEARTBEAT.md',
                'description': content[:200],
                'priority': 2
            }
    except:
        pass
    return None

def collect_from_logs():
    """从日志文件收集任务"""
    tasks = []
    log_files = [
        'logs/hot-topics.log',
        'logs/crawler.log',
        'logs/daily-report.log'
    ]
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-10:]  # 最后 10 行
            
            for line in lines:
                if '失败' in line or 'Error' in line or '❌' in line:
                    tasks.append({
                        'title': '修复日志错误',
                        'source': log_file,
                        'description': line.strip()[:200],
                        'priority': 3
                    })
        except:
            pass
    
    return tasks

def collect_from_database():
    """从数据库收集任务"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查失败的任务
    cursor.execute('SELECT * FROM tasks WHERE status = "failed" OR status = "pending" LIMIT 5')
    tasks = cursor.fetchall()
    conn.close()
    
    return [{'title': f'任务 ID:{t["id"]}', 'source': 'database', 'description': t['title'], 'priority': 2} for t in tasks]

def collect_from_hot_topics():
    """从热点数据发现机会"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查最新热点
    cursor.execute('SELECT platform, title, views FROM platform_monitor ORDER BY crawl_time DESC LIMIT 5')
    hot_topics = cursor.fetchall()
    conn.close()
    
    tasks = []
    for topic in hot_topics:
        if topic['views'] and topic['views'] > 100000:
            tasks.append({
                'title': f'跟进热点：{topic["title"][:30]}',
                'source': f'热点监控 ({topic["platform"]})',
                'description': f'浏览量：{topic["views"]}',
                'priority': 2
            })
    
    return tasks

def run_continuous_collection():
    """持续收集任务"""
    print("=" * 60)
    print("📥 任务收集专员 - 持续运行")
    print("=" * 60)
    print(f"⏰ 启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    update_employee_status('working')
    log_interaction('小龙虾主管', SESSION_KEY, '请持续收集任务，保持工作状态', 'task_assign')
    
    collection_count = 0
    
    while True:
        try:
            print(f"\n📝 [{datetime.now().strftime('%H:%M:%S')}] 开始第{collection_count+1}轮收集...")
            
            new_tasks = []
            
            # 1. 从 HEARTBEAT 收集
            task = collect_from_heartbeat()
            if task:
                new_tasks.append(task)
                print(f"   ✅ HEARTBEAT: {task['title']}")
            
            # 2. 从日志收集
            log_tasks = collect_from_logs()
            new_tasks.extend(log_tasks)
            for t in log_tasks:
                print(f"   ✅ 日志错误：{t['title']}")
            
            # 3. 从数据库收集
            db_tasks = collect_from_database()
            new_tasks.extend(db_tasks)
            for t in db_tasks:
                print(f"   ✅ 数据库：{t['title']}")
            
            # 4. 从热点收集
            hot_tasks = collect_from_hot_topics()
            new_tasks.extend(hot_tasks)
            for t in hot_tasks:
                print(f"   ✅ 热点机会：{t['title']}")
            
            # 记录交互
            if new_tasks:
                message = f"✅ 第{collection_count+1}轮收集完成\n\n发现 {len(new_tasks)} 个任务：\n"
                for i, t in enumerate(new_tasks[:5], 1):
                    message += f"{i}. {t['title']} (优先级：{t['priority']})\n"
                
                log_interaction(SESSION_KEY, 'agent:main', message, 'task_report')
                collection_count += 1
                print(f"   📊 本轮发现：{len(new_tasks)} 个任务")
            else:
                print(f"   ⏸️ 本轮无新任务")
            
            # 更新状态（保持工作中）
            update_employee_status('working')
            
            # 等待 5 分钟
            print(f"   ⏳ 等待 5 分钟后继续...")
            time.sleep(300)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  停止收集")
            update_employee_status('idle')
            break
        except Exception as e:
            print(f"   ❌ 错误：{e}")
            time.sleep(60)

if __name__ == '__main__':
    run_continuous_collection()
