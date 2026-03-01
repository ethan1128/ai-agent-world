#!/usr/bin/env python3
"""
多平台内容抓取脚本
支持：小红书、抖音、快手、知乎、视频号
每 10 分钟执行一次
"""

import sqlite3
import json
import os
from datetime import datetime
import time

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 模拟数据（实际应该调用各平台 API）
MOCK_DATA = {
    'xiaohongshu': [
        {
            'title': '人到中年，这三种人要学会远离',
            'author': '暖心大叔',
            'author_avatar': 'https://example.com/avatar1.jpg',
            'author_url': 'https://www.xiaohongshu.com/user/profile/xxx',
            'views': 125000,
            'likes': 8500,
            'comments': 320,
            'shares': 1200,
            'content_url': 'https://www.xiaohongshu.com/discovery/item/xxx',
            'thumbnail_url': 'https://example.com/thumb1.jpg',
            'description': '人到中年，经历过风雨，也看透了人心。这三种人，一定要学会远离。',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#中年 #情感 #人生感悟'
        },
        {
            'title': '退休后，千万别做这 3 件傻事',
            'author': '岁月如歌',
            'author_avatar': 'https://example.com/avatar2.jpg',
            'author_url': 'https://www.xiaohongshu.com/user/profile/yyy',
            'views': 98000,
            'likes': 6200,
            'comments': 280,
            'shares': 890,
            'content_url': 'https://www.xiaohongshu.com/discovery/item/yyy',
            'thumbnail_url': 'https://example.com/thumb2.jpg',
            'description': '退休是人生新起点，但有些事千万别做。',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#退休 #生活 #建议'
        }
    ],
    'douyin': [
        {
            'title': '老了才明白，最好的关系不是天天见面',
            'author': '老李聊人生',
            'author_avatar': 'https://example.com/avatar3.jpg',
            'author_url': 'https://www.douyin.com/user/xxx',
            'views': 250000,
            'likes': 15000,
            'comments': 520,
            'shares': 2100,
            'content_url': 'https://www.douyin.com/video/xxx',
            'thumbnail_url': 'https://example.com/thumb3.jpg',
            'description': '年轻时，总觉得朋友要多，关系要勤维护。老了才明白...',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#友情 #关系 #人生'
        }
    ],
    'kuaishou': [
        {
            'title': '农村老人的真实生活',
            'author': '乡村记录者',
            'author_avatar': 'https://example.com/avatar4.jpg',
            'author_url': 'https://www.kuaishou.com/profile/xxx',
            'views': 180000,
            'likes': 12000,
            'comments': 450,
            'shares': 1500,
            'content_url': 'https://www.kuaishou.com/short-video/xxx',
            'thumbnail_url': 'https://example.com/thumb4.jpg',
            'description': '记录农村老人的日常生活，真实而感人。',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#农村 #老人 #生活'
        }
    ],
    'zhihu': [
        {
            'title': '人到中年是一种怎样的体验？',
            'author': '知乎用户',
            'author_avatar': 'https://example.com/avatar5.jpg',
            'author_url': 'https://www.zhihu.com/people/xxx',
            'views': 320000,
            'likes': 2800,
            'comments': 890,
            'shares': 450,
            'content_url': 'https://www.zhihu.com/question/xxx',
            'thumbnail_url': 'https://example.com/thumb5.jpg',
            'description': '人到中年，上有老下有小，责任重大但也收获满满。',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#中年 #人生 #体验'
        }
    ],
    'videonumber': [
        {
            'title': '夫妻走到最后，靠的不是爱情',
            'author': '情感驿站',
            'author_avatar': 'https://example.com/avatar6.jpg',
            'author_url': 'https://channels.weixin.qq.com/xxx',
            'views': 150000,
            'likes': 9800,
            'comments': 380,
            'shares': 1100,
            'content_url': 'https://channels.weixin.qq.com/xxx',
            'thumbnail_url': 'https://example.com/thumb6.jpg',
            'description': '年轻时的爱情，轰轰烈烈。中年后的婚姻，平平淡淡。',
            'cover_url': '',
            'publish_time': datetime.now(),
            'tags': '#婚姻 #夫妻 #相处'
        }
    ]
}

def save_monitor_data(platform, data_list):
    """保存抓取的数据到数据库"""
    conn = get_db()
    cursor = conn.cursor()
    
    for data in data_list:
        cursor.execute('''
            INSERT INTO platform_monitor 
            (platform, title, author, author_avatar, author_url, 
             views, likes, comments, shares, 
             content_url, thumbnail_url, description,
             cover_url, publish_time, tags, crawl_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            platform,
            data['title'],
            data['author'],
            data.get('author_avatar', ''),
            data.get('author_url', ''),
            data['views'],
            data['likes'],
            data['comments'],
            data['shares'],
            data['content_url'],
            data.get('thumbnail_url', ''),
            data.get('description', ''),
            data.get('cover_url', ''),
            data['publish_time'],
            data['tags'],
            datetime.now()
        ))
    
    # 更新最后抓取时间
    cursor.execute('''
        UPDATE platform_config 
        SET last_crawl = ? 
        WHERE platform = ?
    ''', (datetime.now(), platform))
    
    conn.commit()
    conn.close()

def crawl_platform(platform):
    """抓取单个平台数据（模拟）"""
    print(f"🕷️  开始抓取 {platform}...")
    
    # TODO: 实际应该调用各平台 API
    # 这里使用模拟数据
    data = MOCK_DATA.get(platform, [])
    
    if data:
        save_monitor_data(platform, data)
        print(f"✅ {platform} 抓取完成，共 {len(data)} 条")
    else:
        print(f"⚠️  {platform} 无数据")
    
    return len(data)

def crawl_all_platforms():
    """抓取所有启用的平台"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT platform, name FROM platform_config WHERE enabled = 1")
    platforms = cursor.fetchall()
    conn.close()
    
    total = 0
    for platform in platforms:
        count = crawl_platform(platform[0])
        total += count
        time.sleep(1)  # 避免请求过快
    
    print(f"\n📊 本次抓取总计：{total} 条内容")
    return total

if __name__ == '__main__':
    print("=" * 60)
    print("🕷️  多平台内容抓取")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    crawl_all_platforms()
    
    print()
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
