#!/usr/bin/env python3
"""
百度热搜爬虫
无需 API，直接抓取公开数据
"""

import requests
import re
import json
from datetime import datetime
import subprocess

DB_PATH = '/home/admin/.openclaw/workspace/ai-agents-world/agents-world.db'

def fetch_baidu_hot_search():
    """抓取百度热搜"""
    print("🔍 抓取百度热搜...")
    
    try:
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 提取热搜数据
        hot_topics = []
        
        # 简单提取热搜词条
        pattern = r'"word":"([^"]+)"'
        matches = re.findall(pattern, response.text)
        
        for i, word in enumerate(matches[:20], 1):
            hot_topics.append({
                'platform': 'baidu',
                'title': word,
                'rank': i,
                'hot_value': 0,
                'author': '百度热搜',
                'views': 0,
                'likes': 0,
                'comments': 0,
                'content_url': f'https://www.baidu.com/s?wd={word}',
                'tags': '#百度热搜',
                'publish_time': datetime.now(),
                'crawl_time': datetime.now()
            })
        
        print(f"✅ 百度热搜抓取完成，共 {len(hot_topics)} 条")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
        return []

def save_to_database(hot_topics):
    """保存到数据库"""
    if not hot_topics:
        return
    
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        for topic in hot_topics:
            try:
                cursor.execute("""
                    INSERT INTO platform_monitor 
                    (platform, title, author, views, likes, comments, 
                     content_url, tags, publish_time, crawl_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    topic['platform'],
                    topic['title'],
                    topic['author'],
                    topic['views'],
                    topic['likes'],
                    topic['comments'],
                    topic['content_url'],
                    topic['tags'],
                    topic['publish_time'],
                    topic['crawl_time']
                ))
            except Exception as e:
                print(f"⚠️  保存失败：{e}")
        
        conn.commit()
        conn.close()
        print(f"✅ 已保存 {len(hot_topics)} 条数据到数据库")
        
    except Exception as e:
        print(f"❌ 数据库操作失败：{e}")

def generate_report(hot_topics):
    """生成报告"""
    if not hot_topics:
        return None
    
    lines = [
        f"# 🔥 百度热搜榜（{datetime.now().strftime('%m-%d %H:%M')}）",
        "",
        f"📊 共 {len(hot_topics)} 条热搜",
        "",
        "### TOP 10 热搜",
        ""
    ]
    
    for i, topic in enumerate(hot_topics[:10], 1):
        lines.append(f"{i}. **{topic['title']}**")
        lines.append(f"   🔥 热度：{topic['hot_value']}")
        lines.append(f"   🔗 [搜索](https://www.baidu.com/s?wd={topic['title']})")
        lines.append("")
    
    lines.append("---")
    lines.append(f"_抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    
    return "\n".join(lines)

def send_report(message):
    """发送报告"""
    if not message:
        return
    
    try:
        subprocess.run([
            'openclaw', 'message', 'send',
            '--target', '035327583959855978',
            '--channel', 'dingtalk',
            '--message', message
        ], timeout=30)
        print("✅ 报告已发送")
    except Exception as e:
        print(f"❌ 发送失败：{e}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 百度热搜抓取")
    print("=" * 60)
    
    # 抓取
    hot_topics = fetch_baidu_hot_search()
    
    # 保存
    save_to_database(hot_topics)
    
    # 生成报告
    report = generate_report(hot_topics)
    
    # 发送
    send_report(report)
    
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
