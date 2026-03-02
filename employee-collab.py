#!/usr/bin/env python3
"""
数字员工协作系统（模拟版）
我同时扮演多个角色，模拟员工协作
"""

import sqlite3
from datetime import datetime
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

def simulate_content_creation(hot_topic):
    """模拟文曲星创作文案"""
    return f"""
【文案草稿】

标题：{hot_topic}

内容：
人到中年，经历过风雨，也看透了人心。

这三种人，一定要学会远离：

1️⃣ 总是抱怨的人——负能量会传染
2️⃣ 借钱不还的人——真心换不来珍惜
3️⃣ 见不得你好的人——表面朋友最可怕

余生不长，和舒服的人在一起，才是最好的养生。

💬 你觉得呢？评论区聊聊

#情感 #人生感悟 #中年
"""

def simulate_data_analysis(content):
    """模拟数据通分析数据"""
    return """
【数据分析报告】

📊 内容质量评估
- 积极性：90 分 ✅
- 合规性：95 分 ✅
- 吸引力：88 分 ✅

📈 传播预测
- 预计浏览量：10w+
- 预计点赞：5000+
- 预计评论：300+
- 预计分享：1000+

💡 优化建议
1. 开头可以更吸引人
2. 增加具体案例
3. 结尾加强互动引导

✅ 综合评分：91 分 - 建议发布
"""

def employee_collaboration_demo():
    """演示员工协作"""
    print("🦞 开始员工协作演示...")
    
    # 1. 主管接收任务
    print("📝 接收任务：根据热点创作文案")
    
    # 2. 主管分配任务给文曲星
    log_interaction(
        'agent:main',
        'agent:main:subagent:38c7e7e0',
        '请根据热点"人到中年，这三种人要学会远离"创作一篇情感文案，要求 200-300 字，引起中老年共鸣',
        'task_assign',
        'completed'
    )
    print("✍️ 分配任务给文曲星...")
    
    # 3. 文曲星创作文案
    content = simulate_content_creation("人到中年，这三种人要学会远离")
    log_interaction(
        'agent:main:subagent:38c7e7e0',
        'agent:main',
        content,
        'task_complete',
        'completed'
    )
    print("✅ 文曲星完成文案...")
    
    # 4. 主管分配任务给数据通
    log_interaction(
        'agent:main',
        'agent:main:subagent:6dd8cf1f',
        '请分析这篇文案的传播效果和潜在数据',
        'task_assign',
        'completed'
    )
    print("📊 分配任务给数据通...")
    
    # 5. 数据通分析数据
    analysis = simulate_data_analysis(content)
    log_interaction(
        'agent:main:subagent:6dd8cf1f',
        'agent:main',
        analysis,
        'task_complete',
        'completed'
    )
    print("✅ 数据通完成分析...")
    
    print("🎉 员工协作演示完成！")
    print("🌐 访问员工仪表板查看交互记录")

if __name__ == '__main__':
    employee_collaboration_demo()
