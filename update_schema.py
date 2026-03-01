#!/usr/bin/env python3
"""
更新数据库表结构 - 添加多渠道监控支持
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def update_schema():
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建多渠道监控表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS platform_monitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            keyword TEXT,
            content_type TEXT,
            title TEXT,
            author TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            content_url TEXT,
            cover_url TEXT,
            publish_time DATETIME,
            crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            tags TEXT,
            metadata TEXT
        )
    ''')
    
    # 创建平台配置表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS platform_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            icon TEXT,
            enabled INTEGER DEFAULT 1,
            crawl_interval INTEGER DEFAULT 600,
            keywords TEXT,
            last_crawl DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入平台配置
    platforms = [
        ('xiaohongshu', '小红书', '📕', 1, 600, '中老年，情感，养生，生活技巧'),
        ('douyin', '抖音', '🎵', 1, 600, '中老年，情感，正能量，生活'),
        ('kuaishou', '快手', '📹', 1, 600, '中老年，情感，生活，农村'),
        ('zhihu', '知乎', '📖', 1, 600, '中年，情感，人生，职场'),
        ('videonumber', '视频号', '📺', 1, 600, '中老年，情感，正能量')
    ]
    
    for platform in platforms:
        cursor.execute('''
            INSERT OR IGNORE INTO platform_config 
            (platform, name, icon, enabled, crawl_interval, keywords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', platform)
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform ON platform_monitor(platform)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_crawl_time ON platform_monitor(crawl_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_time ON platform_monitor(publish_time)')
    
    conn.commit()
    conn.close()
    print("✅ 数据库表结构已更新")

if __name__ == '__main__':
    update_schema()
