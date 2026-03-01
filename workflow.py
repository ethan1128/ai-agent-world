#!/usr/bin/env python3
"""
AI 员工世界 - 完整工作流
天枢→地衡→文曲→明镜 流水线作业
"""

import sqlite3
import json
import subprocess
import os
from datetime import datetime
import time

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================
# AI 员工定义
# ============================================

AGENTS = {
    1: {'name': '天枢', 'role': '研究主管', 'task': '收集中老年情感热点话题'},
    2: {'name': '地衡', 'role': '情报收集', 'task': '监控竞品账号爆款内容'},
    3: {'name': '文曲', 'role': '内容创作', 'task': '撰写情感类文案草稿'},
    4: {'name': '明镜', 'role': '质量审核', 'task': '审核内容质量和合规性'}
}

PROMPTS = {
    1: '''你是一个中老年情感内容研究专家。请找出 5 个可能成为爆款的情感话题，每个话题配一个吸引人的标题，并说明为什么这个话题会火。输出 JSON 格式。''',
    
    2: '''你是一个社交媒体情报分析师。请分析抖音/快手上中老年情感类账号的爆款内容特点，总结 3-5 个可复用的模式。输出 JSON 格式。''',
    
    3: '''你是一个中老年情感内容创作者。请根据热点话题写一篇抖音/快手情感类短视频文案，要求：开头 3 秒抓住注意力，内容引起共鸣，结尾引导互动，200-300 字。输出 JSON 格式。''',
    
    4: '''你是一个内容质量审核专家。请审核内容是否符合平台规范，从积极性、合规性、吸引力三个维度打分（0-100），给出修改建议。输出 JSON 格式。'''
}

# ============================================
# 核心函数
# ============================================

def update_agent(agent_id, status, task=None, progress=0):
    """更新智能体状态"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE agents SET status = ?, current_task = ?, progress = ?, updated_at = ?
        WHERE id = ?
    """, (status, task, progress, datetime.now(), agent_id))
    conn.commit()
    conn.close()

def add_log(agent_id, action, message):
    """添加活动日志"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO activity_log (agent_id, action, message)
        VALUES (?, ?, ?)
    """, (agent_id, action, message))
    conn.commit()
    conn.close()

def save_content(title, body, agent_id, platform='douyin'):
    """保存生成的内容"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO content (title, body, platform, status, created_by, created_at)
        VALUES (?, ?, ?, 'draft', ?, ?)
    """, (title, body, platform, agent_id, datetime.now()))
    content_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return content_id

def run_agent(agent_id, prompt):
    """执行单个 AI 员工任务"""
    agent = AGENTS[agent_id]
    print(f"\n🤖 {agent['name']} 开始：{agent['task']}")
    
    # 更新状态
    update_agent(agent_id, 'busy', agent['task'], 0)
    add_log(agent_id, 'working', f'开始任务：{agent["task"]}')
    
    # 调用 OpenClaw
    cmd = ['openclaw', 'sessions', 'spawn', '--mode', 'run', '--label', f'{agent["name"]}', '--task', prompt]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True, timeout=300)
        output = result.stdout.strip()
        
        # 更新状态
        update_agent(agent_id, 'idle', None, 100)
        add_log(agent_id, 'completed', f'任务完成')
        print(f"✅ {agent['name']} 完成")
        
        return {'success': True, 'output': output[:500]}  # 截取 500 字
    except Exception as e:
        update_agent(agent_id, 'idle', None, 0)
        add_log(agent_id, 'failed', f'任务失败：{str(e)}')
        print(f"❌ {agent['name']} 失败：{e}")
        return {'success': False, 'error': str(e)}

# ============================================
# 完整工作流
# ============================================

def run_full_workflow():
    """
    执行完整工作流：
    天枢研究 → 地衡情报 → 文曲创作 → 明镜审核
    """
    print("=" * 60)
    print("🚀 AI 员工世界 - 完整工作流启动")
    print("=" * 60)
    print(f"⏰ 启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    workflow_start = time.time()
    results = {}
    
    # 1. 天枢 - 研究热点
    results[1] = run_agent(1, PROMPTS[1])
    time.sleep(2)  # 短暂休息
    
    # 2. 地衡 - 收集情报
    results[2] = run_agent(2, PROMPTS[2])
    time.sleep(2)
    
    # 3. 文曲 - 创作文案
    results[3] = run_agent(3, PROMPTS[3])
    time.sleep(2)
    
    # 4. 明镜 - 审核内容
    results[4] = run_agent(4, PROMPTS[4])
    
    # 统计
    workflow_end = time.time()
    duration = workflow_end - workflow_start
    success_count = sum(1 for r in results.values() if r['success'])
    
    print("\n" + "=" * 60)
    print("📊 工作流执行完成")
    print("=" * 60)
    print(f"⏱️  总耗时：{duration:.1f}秒")
    print(f"✅ 成功：{success_count}/4")
    print(f"❌ 失败：{4 - success_count}/4")
    print("=" * 60)
    
    # 保存到数据库
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (type, data)
        VALUES (?, ?)
    """, ('workflow_completed', json.dumps({
        'duration': duration,
        'success': success_count,
        'total': 4,
        'timestamp': datetime.now().isoformat()
    }, ensure_ascii=False)))
    conn.commit()
    conn.close()
    
    return results

# ============================================
# 主函数
# ============================================

if __name__ == '__main__':
    run_full_workflow()
