#!/usr/bin/env python3
"""
AI 员工世界 - 改进版工作流
带内容保存和展示
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
    1: '''你是一个中老年情感内容研究专家。请找出 5 个可能成为爆款的情感话题。

对于每个话题，提供：
1. 标题（吸引人）
2. 火爆原因
3. 关键词

请以 JSON 格式输出：
{
  "topics": [
    {"title": "标题 1", "reason": "原因", "keywords": ["词 1", "词 2"]},
    ...
  ]
}''',
    
    2: '''你是一个社交媒体情报分析师。请分析抖音/快手上中老年情感类账号的爆款内容特点。

请总结：
1. 3 个对标账号
2. 5 个可复用的模式

请以 JSON 格式输出：
{
  "accounts": [{"name": "账号", "style": "风格"}],
  "patterns": ["模式 1", "模式 2", ...]
}''',
    
    3: '''你是一个中老年情感内容创作者。请根据以下话题写一篇抖音/快手情感类短视频文案：

话题：人到中年，这三种人要学会远离

要求：
1. 开头 3 秒抓住注意力
2. 内容引起共鸣
3. 结尾引导互动
4. 200-300 字
5. 配上标签

请以 JSON 格式输出：
{
  "title": "文案标题",
  "content": "完整文案",
  "tags": ["#标签 1", "#标签 2"]
}''',
    
    4: '''你是一个内容质量审核专家。请审核以下内容：

审核维度：
1. 积极性（0-100 分）
2. 合规性（0-100 分）
3. 吸引力（0-100 分）

请以 JSON 格式输出：
{
  "passed": true/false,
  "scores": {"positive": 80, "compliance": 90, "appeal": 85},
  "feedback": "修改建议",
  "reason": "通过/不通过原因"
}'''
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

def save_content(title, body, agent_id, platform='douyin', metadata=None):
    """保存生成的内容"""
    conn = get_db()
    cursor = conn.cursor()
    
    metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata else None
    
    cursor.execute("""
        INSERT INTO content (title, body, platform, status, created_by, created_at, metrics_views)
        VALUES (?, ?, ?, 'draft', ?, ?, ?)
    """, (title, body, platform, agent_id, datetime.now(), 0 if metadata is None else 0))
    
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
    
    # 调用 OpenClaw（简化版，直接返回模拟输出用于演示）
    output = generate_mock_output(agent_id)
    
    # 保存内容
    if agent_id == 1:  # 天枢 - 研究
        save_content(
            f"{agent['name']}的热点报告",
            json.dumps(output, ensure_ascii=False),
            agent_id,
            platform='research',
            metadata=output
        )
    elif agent_id == 2:  # 地衡 - 情报
        save_content(
            f"{agent['name']}的情报分析",
            json.dumps(output, ensure_ascii=False),
            agent_id,
            platform='intelligence',
            metadata=output
        )
    elif agent_id == 3:  # 文曲 - 创作
        save_content(
            output.get('title', '文案'),
            output.get('content', ''),
            agent_id,
            platform='douyin',
            metadata=output
        )
    elif agent_id == 4:  # 明镜 - 审核
        save_content(
            f"{agent['name']}的审核报告",
            json.dumps(output, ensure_ascii=False),
            agent_id,
            platform='review',
            metadata=output
        )
    
    # 更新状态
    update_agent(agent_id, 'idle', None, 100)
    add_log(agent_id, 'completed', f'任务完成')
    print(f"✅ {agent['name']} 完成")
    
    return {'success': True, 'output': output}

def generate_mock_output(agent_id):
    """生成模拟输出（用于演示）"""
    if agent_id == 1:  # 天枢
        return {
            "topics": [
                {"title": "人到中年，这三种人要学会远离", "reason": "引起共鸣，实用建议", "keywords": ["中年", "人际关系", "断舍离"]},
                {"title": "老了才明白，最好的关系不是天天见面", "reason": "情感共鸣，人生感悟", "keywords": ["友情", "关系", "人生"]},
                {"title": "退休后，千万别做这 3 件傻事", "reason": "警示性，实用", "keywords": ["退休", "建议", "生活"]},
                {"title": "夫妻走到最后，靠的不是爱情", "reason": "反差，深度", "keywords": ["婚姻", "夫妻", "相处"]},
                {"title": "人这一辈子，最亏欠的其实是自己", "reason": "情感共鸣，反思", "keywords": ["人生", "自己", "感悟"]}
            ]
        }
    elif agent_id == 2:  # 地衡
        return {
            "accounts": [
                {"name": "暖心大叔", "style": "人生感悟"},
                {"name": "岁月如歌", "style": "情感故事"},
                {"name": "老李聊人生", "style": "生活智慧"}
            ],
            "patterns": [
                "开头 3 秒抛出痛点",
                "用真实故事引起共鸣",
                "结尾引导点赞评论",
                "配乐选择怀旧经典",
                "文案简洁有节奏感"
            ]
        }
    elif agent_id == 3:  # 文曲
        return {
            "title": "人到中年，这三种人要学会远离",
            "content": """人到中年，经历过风雨，也看透了人心。

这三种人，一定要学会远离：

1️⃣ 总是抱怨的人——负能量会传染
2️⃣ 借钱不还的人——真心换不来珍惜
3️⃣ 见不得你好的人——表面朋友最可怕

余生不长，和舒服的人在一起，才是最好的养生。

💬 你觉得呢？评论区聊聊

#人到中年 #人生感悟 #情感语录 #远离负能量""",
            "tags": ["#人到中年", "#人生感悟", "#情感语录", "#远离负能量"]
        }
    elif agent_id == 4:  # 明镜
        return {
            "passed": True,
            "scores": {"positive": 90, "compliance": 95, "appeal": 88},
            "feedback": "内容积极正向，建议发布",
            "reason": "内容符合平台规范，具有正向引导作用，能引起目标群体共鸣"
        }
    return {}

# ============================================
# 完整工作流
# ============================================

def run_full_workflow():
    """执行完整工作流"""
    print("=" * 60)
    print("🚀 AI 员工世界 - 完整工作流启动")
    print("=" * 60)
    print(f"⏰ 启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    workflow_start = time.time()
    results = {}
    
    # 1. 天枢 - 研究热点
    results[1] = run_agent(1, PROMPTS[1])
    time.sleep(1)
    
    # 2. 地衡 - 收集情报
    results[2] = run_agent(2, PROMPTS[2])
    time.sleep(1)
    
    # 3. 文曲 - 创作文案
    results[3] = run_agent(3, PROMPTS[3])
    time.sleep(1)
    
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
