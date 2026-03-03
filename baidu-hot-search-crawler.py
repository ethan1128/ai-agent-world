#!/usr/bin/env python3
"""
百度热搜爬虫 - 真实数据源
每 10 分钟抓取一次百度热搜
"""

import requests
import sqlite3
import os
from datetime import datetime
from bs4 import BeautifulSoup

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_baidu_hot_search():
    """抓取百度热搜真实数据"""
    print("🔍 开始抓取百度热搜...")
    
    try:
        # 百度热搜 API（公开接口）
        url = 'https://top.baidu.com/board?tab=realtime'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取热搜数据
        hot_topics = []
        
        # 查找热搜条目
        items = soup.find_all('div', class_='category-wrap')
        
        for item in items[:20]:  # 取前 20 个
            try:
                title_elem = item.find('a', class_='title')
                if title_elem:
                    title = title_elem.get('title', '').strip()
                    
                    # 提取热度
                    hot_elem = item.find('span', class_='hot-text')
                    hot_value = 0
                    if hot_elem:
                        hot_text = hot_elem.get_text().strip()
                        # 转换为数字
                        if '亿' in hot_text:
                            hot_value = int(float(hot_text.replace('亿', '')) * 100000000)
                        elif '万' in hot_text:
                            hot_value = int(float(hot_text.replace('万', '')) * 10000)
                        else:
                            try:
                                hot_value = int(hot_text)
                            except:
                                pass
                    
                    hot_topics.append({
                        'title': title,
                        'hot_value': hot_value,
                        'platform': 'baidu',
                        'crawl_time': datetime.now()
                    })
            except Exception as e:
                continue
        
        print(f"✅ 抓取到 {len(hot_topics)} 条百度热搜")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
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
                topic['platform'],
                topic['title'],
                '百度热搜',
                topic['hot_value'],
                0,
                0,
                f'https://www.baidu.com/s?wd={topic["title"]}',
                '#百度热搜',
                datetime.now(),
                topic['crawl_time']
            ))
            saved_count += 1
        except Exception as e:
            print(f"⚠️  保存失败：{e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"✅ 保存 {saved_count} 条数据到数据库")
    return saved_count

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 百度热搜爬虫 - 真实数据源")
    print("=" * 60)
    
    hot_topics = fetch_baidu_hot_search()
    saved = save_to_database(hot_topics)
    
    print("=" * 60)
    print(f"✅ 完成：抓取 {len(hot_topics)} 条，保存 {saved} 条")
    print("=" * 60)
