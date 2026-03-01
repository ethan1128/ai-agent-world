#!/usr/bin/env python3
"""
全网热点收集脚本
每 2 小时执行一次，收集各平台热点并推送
"""

import sqlite3
import json
import os
from datetime import datetime
import subprocess

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def collect_hot_topics():
    """收集全网热点"""
    print(f"🔥 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始收集全网热点...")
    
    # 从数据库获取最近的热点内容
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取最近 2 小时的热点
    cursor.execute("""
        SELECT platform, title, author, views, likes, content_url, tags
        FROM platform_monitor
        WHERE crawl_time >= datetime('now', '-2 hours')
        ORDER BY views DESC
        LIMIT 20
    """)
    
    hot_topics = cursor.fetchall()
    conn.close()
    
    if not hot_topics:
        print("⚠️  暂无热点数据")
        return None
    
    # 按平台分组统计
    platform_stats = {}
    for topic in hot_topics:
        platform = topic['platform']
        if platform not in platform_stats:
            platform_stats[platform] = {
                'count': 0,
                'total_views': 0,
                'topics': []
            }
        platform_stats[platform]['count'] += 1
        platform_stats[platform]['total_views'] += topic['views']
        platform_stats[platform]['topics'].append({
            'title': topic['title'],
            'author': topic['author'],
            'views': topic['views'],
            'likes': topic['likes'],
            'url': topic['content_url'],
            'tags': topic['tags']
        })
    
    # 生成汇总报告
    report = generate_report(platform_stats, len(hot_topics))
    
    print(f"✅ 收集完成，共 {len(hot_topics)} 条热点")
    
    return report

def generate_report(platform_stats, total_count):
    """生成热点汇总报告"""
    platform_names = {
        'xiaohongshu': '📕 小红书',
        'douyin': '🎵 抖音',
        'kuaishou': '📹 快手',
        'zhihu': '📖 知乎',
        'videonumber': '📺 视频号'
    }
    
    report = {
        'title': f'🔥 全网热点汇总（{datetime.now().strftime("%m-%d %H:%M")}）',
        'summary': f'过去 2 小时共收集 {total_count} 条热点内容',
        'platforms': []
    }
    
    for platform, data in platform_stats.items():
        platform_report = {
            'name': platform_names.get(platform, platform),
            'count': data['count'],
            'total_views': data['total_views'],
            'top_topics': sorted(data['topics'], key=lambda x: x['views'], reverse=True)[:5]
        }
        report['platforms'].append(platform_report)
    
    return report

def send_report(report):
    """推送报告给用户"""
    if not report:
        print("⚠️  无报告可发送")
        return
    
    # 格式化报告内容
    message = format_report_message(report)
    
    # 通过钉钉发送
    send_dingtalk_message(message)
    
    print("✅ 报告已推送")

def format_report_message(report):
    """格式化报告消息"""
    lines = [
        f"# {report['title']}",
        "",
        f"📊 {report['summary']}",
        ""
    ]
    
    for platform in report['platforms']:
        lines.append(f"### {platform['name']}")
        lines.append(f"📈 {platform['count']} 条热点 · 👁️ {format_number(platform['total_views'])} 次浏览")
        lines.append("")
        
        for i, topic in enumerate(platform['top_topics'][:3], 1):
            lines.append(f"{i}. **{topic['title']}**")
            lines.append(f"   - 作者：{topic['author']}")
            lines.append(f"   - 浏览：{format_number(topic['views'])} · 点赞：{format_number(topic['likes'])}")
            if topic['url']:
                lines.append(f"   - 链接：{topic['url']}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append(f"_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return "\n".join(lines)

def format_number(num):
    """格式化数字"""
    if num >= 10000:
        return f"{num/10000:.1f}w"
    return str(num)

def send_dingtalk_message(message):
    """通过钉钉发送消息"""
    try:
        # 使用 OpenClaw message 工具发送
        subprocess.run([
            'openclaw', 'message', 'send',
            '--target', '035327583959855978',
            '--channel', 'dingtalk',
            '--message', message
        ], timeout=30)
        print("✅ 钉钉消息已发送")
    except Exception as e:
        print(f"❌ 发送失败：{e}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 全网热点收集")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 收集热点
    report = collect_hot_topics()
    
    # 推送报告
    send_report(report)
    
    print()
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
