#!/usr/bin/env python3
"""
真实数据抓取脚本
接入知乎热榜、微博热搜等公开数据
"""

import requests
import json
from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_zhihu_hot():
    """抓取知乎热榜（公开 API）"""
    print("📖 抓取知乎热榜...")
    
    try:
        # 知乎热榜 API（公开）
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20&reverse_order=0"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        hot_topics = []
        for item in data.get('data', []):
            target = item.get('target', {})
            hot_topics.append({
                'platform': 'zhihu',
                'title': target.get('title', ''),
                'author': target.get('author', {}).get('name', '知乎用户'),
                'views': target.get('view_count', 0),
                'likes': target.get('voteup_count', 0),
                'comments': target.get('comment_count', 0),
                'content_url': target.get('url', '').replace('api.', 'www.'),
                'tags': '#知乎热榜',
                'publish_time': datetime.now()
            })
        
        print(f"✅ 知乎热榜抓取完成，共 {len(hot_topics)} 条")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 知乎热榜抓取失败：{e}")
        return []

def fetch_weibo_hot():
    """抓取微博热搜（公开数据）"""
    print("🧣 抓取微博热搜...")
    
    try:
        # 微博热搜 API（公开）
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        hot_topics = []
        for item in data.get('data', {}).get('realtime', [])[:20]:
            hot_topics.append({
                'platform': 'weibo',
                'title': item.get('note', ''),
                'author': '微博热搜',
                'views': item.get('num', 0),
                'likes': 0,
                'comments': 0,
                'content_url': f"https://s.weibo.com/weibo?q={item.get('note', '')}",
                'tags': '#微博热搜',
                'publish_time': datetime.now()
            })
        
        print(f"✅ 微博热搜抓取完成，共 {len(hot_topics)} 条")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 微博热搜抓取失败：{e}")
        return []

def fetch_baidu_hot():
    """抓取百度热搜（公开数据）"""
    print("🔍 抓取百度热搜...")
    
    try:
        # 百度热搜 API（公开）
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # 简单解析 HTML（实际应该用 BeautifulSoup）
        hot_topics = []
        # 这里简化处理，实际需要解析 HTML
        
        print(f"✅ 百度热搜抓取完成")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 百度热搜抓取失败：{e}")
        return []

def save_to_database(hot_topics):
    """保存到数据库"""
    if not hot_topics:
        return
    
    conn = get_db()
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
                datetime.now()
            ))
        except Exception as e:
            print(f"⚠️  保存失败：{e}")
    
    conn.commit()
    conn.close()
    print(f"✅ 已保存 {len(hot_topics)} 条数据到数据库")

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 真实数据抓取")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_topics = []
    
    # 抓取各平台热榜
    all_topics.extend(fetch_zhihu_hot())
    all_topics.extend(fetch_weibo_hot())
    # all_topics.extend(fetch_baidu_hot())  # 百度需要解析 HTML，暂不接入
    
    # 保存到数据库
    save_to_database(all_topics)
    
    print()
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 总计抓取：{len(all_topics)} 条真实数据")
    print("=" * 60)
