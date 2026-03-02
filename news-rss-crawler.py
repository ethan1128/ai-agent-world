#!/usr/bin/env python3
"""
新闻 RSS 抓取脚本
无需 API，直接订阅新闻源
"""

import feedparser
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

# 新闻源列表（公开 RSS）
NEWS_SOURCES = [
    {
        'name': '央视新闻',
        'url': 'http://rss.cctv.com/1/index.shtml',
        'platform': 'cctv'
    },
    {
        'name': '澎湃新闻',
        'url': 'https://www.thepaper.cn/rss/1_110300.xml',
        'platform': 'thepaper'
    },
    {
        'name': '36 氪',
        'url': 'https://36kr.com/feed',
        'platform': '36kr'
    },
    {
        'name': '虎嗅',
        'url': 'https://www.huxiu.com/rss/0.xml',
        'platform': 'huxiu'
    },
    {
        'name': '界面新闻',
        'url': 'https://www.jiemian.com/rss/1.xml',
        'platform': 'jiemian'
    }
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_rss_feed(source):
    """抓取单个 RSS 源"""
    print(f"📰 抓取 {source['name']}...")
    
    try:
        feed = feedparser.parse(source['url'], timeout=10)
        
        news_items = []
        for entry in feed.entries[:10]:  # 每个源取最新 10 条
            news_items.append({
                'platform': source['platform'],
                'source_name': source['name'],
                'title': entry.get('title', ''),
                'author': entry.get('author', '新闻网'),
                'summary': entry.get('summary', '')[:200],
                'url': entry.get('link', ''),
                'publish_time': datetime.now(),
                'crawl_time': datetime.now()
            })
        
        print(f"✅ {source['name']} 抓取完成，共 {len(news_items)} 条")
        return news_items
        
    except Exception as e:
        print(f"❌ {source['name']} 抓取失败：{e}")
        return []

def save_to_database(news_items):
    """保存到数据库"""
    if not news_items:
        return
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建新闻表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            source_name TEXT,
            title TEXT,
            author TEXT,
            summary TEXT,
            url TEXT,
            publish_time DATETIME,
            crawl_time DATETIME
        )
    ''')
    
    for item in news_items:
        try:
            cursor.execute('''
                INSERT INTO news_feed 
                (platform, source_name, title, author, summary, url, publish_time, crawl_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['platform'],
                item['source_name'],
                item['title'],
                item['author'],
                item['summary'],
                item['url'],
                item['publish_time'],
                item['crawl_time']
            ))
        except Exception as e:
            print(f"⚠️  保存失败：{e}")
    
    conn.commit()
    conn.close()
    print(f"✅ 已保存 {len(news_items)} 条新闻到数据库")

def generate_report(news_items):
    """生成新闻汇总报告"""
    if not news_items:
        return None
    
    # 按来源分组
    source_stats = {}
    for item in news_items:
        source = item['source_name']
        if source not in source_stats:
            source_stats[source] = []
        source_stats[source].append(item)
    
    # 生成报告
    lines = [
        f"# 📰 全网新闻热点（{datetime.now().strftime('%m-%d %H:%M')}）",
        "",
        f"📊 共收集 {len(news_items)} 条新闻",
        ""
    ]
    
    for source, items in source_stats.items():
        lines.append(f"### {source}")
        lines.append(f"📈 {len(items)} 条新闻")
        lines.append("")
        
        for i, item in enumerate(items[:3], 1):  # 每个源展示 3 条
            lines.append(f"{i}. **{item['title']}**")
            if item['url']:
                lines.append(f"   🔗 {item['url'][:80]}...")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append(f"_数据来源：RSS 订阅 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    
    return "\n".join(lines)

def send_report(message):
    """发送报告"""
    if not message:
        return
    
    try:
        import subprocess
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
    print("📰 新闻 RSS 抓取（真实数据）")
    print("=" * 60)
    print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_news = []
    
    # 抓取各新闻源
    for source in NEWS_SOURCES:
        news = fetch_rss_feed(source)
        all_news.extend(news)
    
    # 保存到数据库
    save_to_database(all_news)
    
    # 生成报告
    report = generate_report(all_news)
    
    # 发送报告
    send_report(report)
    
    print()
    print("=" * 60)
    print(f"✅ 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 总计抓取：{len(all_news)} 条真实新闻")
    print("=" * 60)
