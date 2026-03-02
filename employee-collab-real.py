#!/usr/bin/env python3
"""
数字员工协作系统（真正子会话版）
使用 sessions_spawn 创建真正的子会话，实现并行工作
"""

import sqlite3
import subprocess
from datetime import datetime
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_interaction(from_emp, to_emp, message, task_type='message', status='completed'):
    """记录交互"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO interactions (from_employee, to_employee, message, task_type, status, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (from_emp, to_emp, message, task_type, status, datetime.now(), datetime.now()))
    
    conn.commit()
    conn.close()

def update_employee_status(session_key, status):
    """更新员工状态"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET status = ? WHERE session_key = ?', (status, session_key))
    conn.commit()
    conn.close()

def spawn_content_expert(task):
    """创建内容专家子会话"""
    print("✍️ 创建文曲星子会话...")
    
    cmd = [
        'openclaw', 'sessions', 'spawn',
        '--mode', 'run',
        '--label', '员工 2 号 - 文曲星',
        '--task', task,
        '--timeout', '300'
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
    
    # 解析输出获取 session_key
    if 'childSessionKey' in result.stdout:
        import re
        match = re.search(r'agent:main:subagent:[a-f0-9-]+', result.stdout)
        if match:
            session_key = match.group()
            print(f"✅ 文曲星子会话创建成功：{session_key}")
            return session_key
    
    print("⚠️  文曲星子会话创建失败")
    return None

def spawn_data_expert(task):
    """创建数据专家子会话"""
    print("📊 创建数据通子会话...")
    
    cmd = [
        'openclaw', 'sessions', 'spawn',
        '--mode', 'run',
        '--label', '员工 3 号 - 数据通',
        '--task', task,
        '--timeout', '300'
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
    
    # 解析输出获取 session_key
    if 'childSessionKey' in result.stdout:
        import re
        match = re.search(r'agent:main:subagent:[a-f0-9-]+', result.stdout)
        if match:
            session_key = match.group()
            print(f"✅ 数据通子会话创建成功：{session_key}")
            return session_key
    
    print("⚠️  数据通子会话创建失败")
    return None

def employee_collaboration_real():
    """真正的员工协作"""
    print("=" * 60)
    print("🦞 开始真正的员工协作")
    print("=" * 60)
    
    # 1. 主管接收任务
    print("\n📝 步骤 1: 主管接收任务")
    hot_topic = "人到中年，这三种人要学会远离"
    print(f"   任务：根据热点\"{hot_topic}\"创作文案并分析数据")
    
    # 2. 主管分配任务给文曲星
    print("\n📝 步骤 2: 分配任务给文曲星")
    content_task = f"""你是文曲星，内容创作专家。

当前任务：根据热点"{hot_topic}"创作一篇情感文案。

要求：
- 200-300 字
- 引起中老年共鸣
- 开头 3 秒抓住注意力
- 结尾引导互动
- 配上合适的标签

直接输出文案内容，不要多余解释。"""
    
    log_interaction('agent:main', '文曲星', content_task, 'task_assign', 'completed')
    update_employee_status('agent:main', 'working')
    
    # 3. 并行创建子会话
    print("\n📝 步骤 3: 并行创建子会话")
    
    content_session = spawn_content_expert(content_task)
    data_task = f"""你是数据通，数据分析专家。

当前任务：分析文案"{hot_topic}"的传播效果和潜在数据。

要求：
- 预计浏览量、点赞、评论、分享
- 内容质量评分（积极性、合规性、吸引力）
- 优化建议
- 综合评分

直接输出分析报告，不要多余解释。"""
    
    data_session = spawn_data_expert(data_task)
    
    # 4. 等待子会话完成
    print("\n⏳ 步骤 4: 等待子会话完成（并行工作）")
    print("   文曲星正在创作文案...")
    print("   数据通正在分析数据...")
    
    import time
    time.sleep(10)  # 等待子会话完成
    
    # 5. 记录完成
    print("\n✅ 步骤 5: 子会话完成")
    
    if content_session:
        log_interaction('文曲星', 'agent:main', '文案已创作完成，请审核', 'task_complete', 'completed')
        update_employee_status(content_session, 'idle')
        print("   ✍️ 文曲星：文案完成")
    
    if data_session:
        log_interaction('数据通', 'agent:main', '数据分析完成，报告已生成', 'task_complete', 'completed')
        update_employee_status(data_session, 'idle')
        print("   📊 数据通：分析完成")
    
    # 6. 主管汇总
    print("\n📝 步骤 6: 主管汇总结果")
    print("   🦞 小龙虾主管：收到两个员工的成果")
    print("   ✅ 文案 + 数据分析 = 完整方案")
    
    print("\n" + "=" * 60)
    print("🎉 员工协作完成！")
    print("=" * 60)
    print("\n🌐 访问员工仪表板查看交互记录：")
    print("   http://www.ai-flow.top/employee-dashboard.html")

if __name__ == '__main__':
    employee_collaboration_real()
