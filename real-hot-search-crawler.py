#!/usr/bin/env python3
"""
真实热点爬虫 - 多数据源
抓取微博热搜、知乎热榜等真实数据
"""

import requests
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_weibo_hot_search():
    """抓取微博热搜 - 真实数据"""
    print("🔍 抓取微博热搜...")
    
    try:
        # 微博热搜移动版页面（不需要 API 授权）
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        hot_topics = []
        cards = data.get('data', {}).get('cards', [])
        for card in cards:
            card_group = card.get('card_group', [])
            for item in card_group:
                if item.get('card_type') == 3:  # 热搜类型
                    hot_topics.append({
                        'title': item.get('desc', ''),
                        'hot_value': item.get('desc_extr', 0),
                        'platform': 'weibo'
                    })
        
        if hot_topics:
            print(f"✅ 抓取到 {len(hot_topics)} 条微博热搜")
            return hot_topics[:10]
        
    except Exception as e:
        print(f"⚠️  微博热搜抓取失败：{e}")
    
    print(f"⚠️  微博热搜抓取失败，返回空数据")
    return []

def fetch_zhihu_hot():
    """抓取知乎热榜（公开 API）"""
    print("🔍 抓取知乎热榜...")
    
    try:
        # 知乎热榜 API
        url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20&reverse_order=0'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        hot_topics = []
        for item in data.get('data', []):
            target = item.get('target', {})
            hot_topics.append({
                'title': target.get('title', ''),
                'hot_value': target.get('view_count', 0),
                'platform': 'zhihu'
            })
        
        print(f"✅ 抓取到 {len(hot_topics)} 条知乎热榜")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 知乎热榜抓取失败：{e}")
        return []

def fetch_36kr_hot():
    """抓取 36 氪热榜（公开 API）"""
    print("🔍 抓取 36 氪热榜...")
    
    try:
        url = 'https://api.36kr.com/wd-api/web/hot-list'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        hot_topics = []
        items = data.get('data', {}).get('hotRankList', [])
        for item in items[:10]:
            hot_topics.append({
                'title': item.get('title', ''),
                'hot_value': item.get('readNum', 0),
                'platform': '36kr'
            })
        
        print(f"✅ 抓取到 {len(hot_topics)} 条 36 氪热榜")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 36 氪热榜抓取失败：{e}")
        return []

def save_to_database(hot_topics):
    """保存到数据库"""
    if not hot_topics:
        return 0
    
    conn = get_db()
    cursor = conn.cursor()
    
    saved_count = 0
    for topic in hot_topics:
        try:
            cursor.execute('''
                INSERT INTO platform_monitor 
                (platform, title, author, views, likes, comments, content_url, tags, publish_time, crawl_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                topic.get('platform', 'web'),
                topic['title'],
                '网络热榜',
                topic.get('hot_value', 0),
                0,
                0,
                f'https://www.baidu.com/s?wd={topic["title"]}',
                '#网络热榜',
                datetime.now(),
                datetime.now()
            ))
            saved_count += 1
        except Exception as e:
            continue
    
    conn.commit()
    conn.close()
    
    print(f"✅ 保存 {saved_count} 条数据到数据库")
    return saved_count



def fetch_douyin_hot():
    """抓取抖音热点"""
    print("🔍 抓取抖音热点...")
    try:
        # 抖音热点 API（公开）
        url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        hot_topics = []
        items = data.get('data', {}).get('word_list', [])
        for item in items[:10]:
            hot_topics.append({
                'title': item.get('word', ''),
                'hot_value': item.get('hot_value', 0),
                'platform': 'douyin'
            })
        
        if hot_topics:
            print(f"✅ 抓取到 {len(hot_topics)} 条抖音热点")
            return hot_topics
    except Exception as e:
        print(f"⚠️  抖音热点抓取失败：{e}")
    return []

def fetch_kuaishou_hot():
    """抓取快手热点"""
    print("🔍 抓取快手热点...")
    try:
        # 快手热点 API（公开）
        url = 'https://www.kuaishou.com/?isHome=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        # 快手需要解析 HTML，暂时返回空
        print("⚠️  快手热点需要登录，跳过")
    except Exception as e:
        print(f"⚠️  快手热点抓取失败：{e}")
    return []

def fetch_xiaohongshu_hot():
    """抓取小红书热点"""
    print("🔍 抓取小红书热点...")
    try:
        # 小红书热点 API（公开）
        url = 'https://www.xiaohongshu.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        # 小红书需要解析 HTML，暂时返回空
        print("⚠️  小红书热点需要登录，跳过")
    except Exception as e:
        print(f"⚠️  小红书热点抓取失败：{e}")
    return []

def fetch_baidu_hot():
    """抓取百度热搜"""
    print("🔍 抓取百度热搜...")
    try:
        url = 'https://top.baidu.com/board?tab=realtime'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        import re
        hot_topics = []
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
        
        if hot_topics:
            print(f"✅ 抓取到 {len(hot_topics)} 条百度热搜")
            return hot_topics
    except Exception as e:
        print(f"⚠️  百度热搜抓取失败：{e}")
    return []

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 真实热点爬虫 - 多数据源")
    print("=" * 60)
    
    all_topics = []
    
    # 抓取多个数据源
    print("\n📱 微博热搜...")
    all_topics.extend(fetch_weibo_hot_search())
    
    print("\n📱 知乎热榜...")
    all_topics.extend(fetch_zhihu_hot())
    
    print("\n📱 抖音热点...")
    all_topics.extend(fetch_douyin_hot())
    
    print("\n📱 快手热点...")
    all_topics.extend(fetch_kuaishou_hot())
    
    print("\n📱 小红书热点...")
    all_topics.extend(fetch_xiaohongshu_hot())
    
    print("\n📱 百度热搜...")
    all_topics.extend(fetch_baidu_hot())
    
    # 保存
    saved = save_to_database(all_topics)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成：抓取 {len(all_topics)} 条，保存 {saved} 条")
    print("=" * 60)
