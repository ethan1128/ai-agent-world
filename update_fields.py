#!/usr/bin/env python3
"""
更新数据库 - 添加内容链接和作者信息字段
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def update_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查字段是否存在，不存在则添加
    cursor.execute("PRAGMA table_info(platform_monitor)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # 添加作者头像字段
    if 'author_avatar' not in columns:
        cursor.execute('ALTER TABLE platform_monitor ADD COLUMN author_avatar TEXT')
        print("✅ 添加 author_avatar 字段")
    
    # 添加作者主页链接
    if 'author_url' not in columns:
        cursor.execute('ALTER TABLE platform_monitor ADD COLUMN author_url TEXT')
        print("✅ 添加 author_url 字段")
    
    # 添加内容缩略图
    if 'thumbnail_url' not in columns:
        cursor.execute('ALTER TABLE platform_monitor ADD COLUMN thumbnail_url TEXT')
        print("✅ 添加 thumbnail_url 字段")
    
    # 添加内容描述
    if 'description' not in columns:
        cursor.execute('ALTER TABLE platform_monitor ADD COLUMN description TEXT')
        print("✅ 添加 description 字段")
    
    # 添加原始数据 JSON
    if 'raw_data' not in columns:
        cursor.execute('ALTER TABLE platform_monitor ADD COLUMN raw_data TEXT')
        print("✅ 添加 raw_data 字段")
    
    conn.commit()
    conn.close()
    print("✅ 数据库表结构已更新")

if __name__ == '__main__':
    update_schema()
