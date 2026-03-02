#!/usr/bin/env python3
"""
网页爬虫方案 - 抓取腾讯新闻
无需 API，直接抓取公开新闻
"""

import requests
import re
from datetime import datetime
import json

def fetch_tencent_news():
    """抓取腾讯新闻热点"""
    print("📰 抓取腾讯新闻热点...")
    
    try:
        # 腾讯新闻热点页面
        url = "https://news.qq.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # 简单提取标题（实际应该用 BeautifulSoup）
        news_items = []
        
        # 正则提取新闻标题和链接
        title_pattern = r'title="([^"]+)"'
        url_pattern = r'href="(https?://news\.qq\.com/[^"]+)"'
        
        titles = re.findall(title_pattern, response.text)[:20]
        urls = re.findall(url_pattern, response.text)[:20]
        
        for i, title in enumerate(titles):
            if len(title) > 10 and len(title) < 100:  # 过滤无效标题
                news_items.append({
                    'platform': 'tencent',
                    'title': title,
                    'author': '腾讯新闻',
                    'url': urls[i] if i < len(urls) else '',
                    'publish_time': datetime.now(),
                    'crawl_time': datetime.now()
                })
        
        print(f"✅ 腾讯新闻抓取完成，共 {len(news_items)} 条")
        return news_items
        
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
        return []

def fetch_sina_news():
    """抓取新浪新闻热点"""
    print("📰 抓取新浪新闻热点...")
    
    try:
        url = "https://news.sina.com.cn/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        news_items = []
        # 简单提取
        title_pattern = r'title="([^"]+)"'
        titles = re.findall(title_pattern, response.text)[:15]
        
        for title in titles:
            if len(title) > 10 and len(title) < 100:
                news_items.append({
                    'platform': 'sina',
                    'title': title,
                    'author': '新浪新闻',
                    'url': 'https://news.sina.com.cn/',
                    'publish_time': datetime.now(),
                    'crawl_time': datetime.now()
                })
        
        print(f"✅ 新浪新闻抓取完成，共 {len(news_items)} 条")
        return news_items
        
    except Exception as e:
        print(f"❌ 抓取失败：{e}")
        return []

def generate_report(news_items):
    """生成新闻报告"""
    if not news_items:
        return None
    
    lines = [
        f"# 📰 全网新闻热点（{datetime.now().strftime('%m-%d %H:%M')}）",
        "",
        f"📊 共收集 {len(news_items)} 条新闻",
        ""
    ]
    
    # 按平台分组
    platform_stats = {}
    for item in news_items:
        platform = item['platform']
        if platform not in platform_stats:
            platform_stats[platform] = []
        platform_stats[platform].append(item)
    
    for platform, items in platform_stats.items():
        platform_names = {'tencent': '腾讯新闻', 'sina': '新浪新闻'}
        lines.append(f"### {platform_names.get(platform, platform)}")
        lines.append(f"📈 {len(items)} 条新闻")
        lines.append("")
        
        for i, item in enumerate(items[:5], 1):
            lines.append(f"{i}. **{item['title']}**")
            lines.append(f"   🔗 {item['url'][:80]}...")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append(f"_抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    
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
    print("📰 新闻网页爬虫（真实数据）")
    print("=" * 60)
    
    all_news = []
    all_news.extend(fetch_tencent_news())
    all_news.extend(fetch_sina_news())
    
    report = generate_report(all_news)
    send_report(report)
    
    print("=" * 60)
    print(f"✅ 总计抓取：{len(all_news)} 条真实新闻")
    print("=" * 60)
