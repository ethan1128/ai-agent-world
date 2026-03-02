#!/usr/bin/env python3
"""
任务收集专员 - 真实数据版
收集真实任务，避免重复
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')
SESSION_KEY = 'agent:main:subagent:4f20a4b3'
LAST_TASKS_FILE = os.path.join(os.path.dirname(__file__), 'logs/last_tasks.json')

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

def load_last_tasks():
    """加载上轮收集的任务（用于去重）"""
    import json
    try:
        with open(LAST_TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_last_tasks(tasks):
    """保存本轮任务"""
    import json
    os.makedirs(os.path.dirname(LAST_TASKS_FILE), exist_ok=True)
    with open(LAST_TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def collect_system_status():
    """收集系统状态任务"""
    tasks = []
    
    # 检查服务状态
    import subprocess
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
        if 'python3 server.py' not in result.stdout:
            tasks.append({
                'title': '⚠️ API 服务未运行',
                'source': '系统监控',
                'description': '检测到 API 服务未运行，需要重启',
                'priority': 1
            })
    except:
        pass
    
    # 检查磁盘空间
    try:
        import shutil
        total, used, free = shutil.disk_usage('/')
        if free < 1024 * 1024 * 1024:  # 小于 1GB
            tasks.append({
                'title': '⚠️ 磁盘空间不足',
                'source': '系统监控',
                'description': f'剩余空间：{free / 1024 / 1024 / 1024:.1f}GB',
                'priority': 1
            })
    except:
        pass
    
    return tasks

def collect_database_tasks():
    """从数据库收集任务"""
    tasks = []
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查失败的任务
    cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE status = "failed"')
    failed = cursor.fetchone()['count']
    if failed > 0:
        tasks.append({
            'title': f'修复 {failed} 个失败任务',
            'source': '数据库',
            'description': f'有{failed}个任务执行失败，需要检查',
            'priority': 2
        })
    
    # 检查待审核任务
    cursor.execute('SELECT COUNT(*) as count FROM tasks WHERE status = "pending"')
    pending = cursor.fetchone()['count']
    if pending > 0:
        tasks.append({
            'title': f'审核 {pending} 个待处理任务',
            'source': '数据库',
            'description': f'有{pending}个任务等待审核',
            'priority': 2
        })
    
    # 检查最新热点数据
    cursor.execute('SELECT COUNT(*) as count FROM platform_monitor WHERE crawl_time >= datetime("now", "-1 hour")')
    recent = cursor.fetchone()['count']
    if recent > 0:
        tasks.append({
            'title': f'分析 {recent} 条最新热点',
            'source': '数据库',
            'description': f'过去 1 小时新增{recent}条热点数据',
            'priority': 3
        })
    
    # 检查待发布内容
    cursor.execute('SELECT COUNT(*) as count FROM content WHERE status = "draft"')
    drafts = cursor.fetchone()['count']
    if drafts > 0:
        tasks.append({
            'title': f'发布 {drafts} 条待发布内容',
            'source': '数据库',
            'description': f'有{drafts}条内容等待发布',
            'priority': 2
        })
    
    conn.close()
    return tasks

def collect_log_errors():
    """从日志收集错误"""
    tasks = []
    log_files = ['logs/hot-topics.log', 'logs/crawler.log', 'logs/server.log']
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-50:]  # 最后 50 行
            
            for line in lines:
                if '失败' in line or 'Error' in line or 'Exception' in line:
                    # 去重：只收集最近的错误
                    task_key = f"{log_file}:{line.strip()[:50]}"
                    if not any(t.get('key') == task_key for t in tasks):
                        tasks.append({
                            'title': f'修复日志错误',
                            'source': log_file,
                            'description': line.strip()[:200],
                            'priority': 2,
                            'key': task_key
                        })
        except:
            pass
    
    return tasks[:5]  # 最多 5 个错误

def collect_heartbeat_tasks():
    """从 HEARTBEAT.md 收集"""
    tasks = []
    try:
        with open('/home/admin/.openclaw/workspace/HEARTBEAT.md', 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if content and not content.startswith('#') and len(content) > 10:
            tasks.append({
                'title': '处理 HEARTBEAT 任务',
                'source': 'HEARTBEAT.md',
                'description': content[:200],
                'priority': 1
            })
    except:
        pass
    
    return tasks

def collect_time_based_tasks():
    """基于时间的任务"""
    tasks = []
    now = datetime.now()
    
    # 晚上 10 点后提醒
    if now.hour >= 22:
        tasks.append({
            'title': '⏰ 时间提醒',
            'source': '时间检查',
            'description': f'当前时间{now.hour}点，建议早点休息',
            'priority': 3
        })
    
    # 整点提醒
    if now.minute == 0:
        tasks.append({
            'title': '⏰ 整点检查',
            'source': '时间检查',
            'description': f'{now.hour}点整，检查系统状态',
            'priority': 3
        })
    
    return tasks

def run_collection():
    """执行一轮收集"""
    print(f"\n📝 [{datetime.now().strftime('%H:%M:%S')}] 开始收集任务...")
    
    new_tasks = []
    
    # 1. 系统状态
    sys_tasks = collect_system_status()
    new_tasks.extend(sys_tasks)
    for t in sys_tasks:
        print(f"   ✅ 系统：{t['title']}")
    
    # 2. 数据库
    db_tasks = collect_database_tasks()
    new_tasks.extend(db_tasks)
    for t in db_tasks:
        print(f"   ✅ 数据库：{t['title']}")
    
    # 3. 日志错误
    log_tasks = collect_log_errors()
    new_tasks.extend(log_tasks)
    for t in log_tasks:
        print(f"   ✅ 日志：{t['title']}")
    
    # 4. HEARTBEAT
    hb_tasks = collect_heartbeat_tasks()
    new_tasks.extend(hb_tasks)
    for t in hb_tasks:
        print(f"   ✅ HEARTBEAT: {t['title']}")
    
    # 5. 时间任务
    time_tasks = collect_time_based_tasks()
    new_tasks.extend(time_tasks)
    for t in time_tasks:
        print(f"   ✅ 时间：{t['title']}")
    
    # 去重
    last_tasks = load_last_tasks()
    unique_tasks = []
    for t in new_tasks:
        task_key = f"{t['source']}:{t['title']}"
        if task_key not in last_tasks:
            unique_tasks.append(t)
    
    # 记录交互
    if unique_tasks:
        message = f"✅ 收集完成\n\n发现 {len(unique_tasks)} 个新任务：\n\n"
        for i, t in enumerate(unique_tasks[:10], 1):
            message += f"{i}. {t['title']} ({t['source']})\n"
            message += f"   {t['description'][:100]}\n\n"
        
        if len(unique_tasks) > 10:
            message += f"... 还有{len(unique_tasks)-10}个任务\n"
        
        log_interaction(SESSION_KEY, 'agent:main', message, 'task_report')
        print(f"   📊 本轮发现：{len(unique_tasks)} 个新任务")
        
        # 保存任务 key 用于去重
        save_last_tasks([f"{t['source']}:{t['title']}" for t in unique_tasks])
    else:
        print(f"   ⏸️ 本轮无新任务")
    
    # 保持工作状态
    update_employee_status('working')
    
    return len(unique_tasks)

if __name__ == '__main__':
    print("=" * 60)
    print("📥 任务收集专员 - 真实数据版")
    print("=" * 60)
    
    update_employee_status('working')
    
    collection_count = 0
    while True:
        try:
            collection_count += 1
            print(f"\n{'='*60}")
            print(f"📊 第{collection_count}轮收集")
            print(f"{'='*60}")
            
            count = run_collection()
            
            # 等待 5 分钟
            print(f"\n   ⏳ 等待 5 分钟后继续...")
            import time
            time.sleep(300)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  停止收集")
            update_employee_status('idle')
            break
        except Exception as e:
            print(f"   ❌ 错误：{e}")
            import time
            time.sleep(60)
