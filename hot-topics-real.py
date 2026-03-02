#!/usr/bin/env python3
"""
全网热点收集脚本（真实数据版）
使用 SearXNG 搜索获取真实热点
"""

import subprocess
import json
from datetime import datetime
import re

def search_hot_topics():
    """使用 SearXNG 搜索热点"""
    print(f"🔥 [{datetime.now().strftime('%H:%M:%S')}] 开始搜索今日热点...")
    
    try:
        # 调用 SearXNG 搜索
        cmd = [
            'uv', 'run',
            'scripts/searxng.py',
            'search',
            '2026 年 3 月 1 日 热搜 热门话题 今日头条',
            '--language', 'zh',
            '-n', '15'
        ]
        
        result = subprocess.run(
            cmd,
            cwd='/home/admin/.openclaw/workspace/skills/searxng',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        # 解析搜索结果
        hot_topics = parse_search_results(result.stdout)
        
        print(f"✅ 搜索完成，共 {len(hot_topics)} 条热点")
        return hot_topics
        
    except Exception as e:
        print(f"❌ 搜索失败：{e}")
        return []

def parse_search_results(output):
    """解析搜索结果"""
    hot_topics = []
    
    # 简单解析，提取标题和链接
    lines = output.split('\n')
    for line in lines:
        if 'http' in line and len(line) > 50:
            # 提取标题
            title_match = re.search(r'\]\((.+?)\)', line)
            url_match = re.search(r'\((https?://[^\s\)]+)\)', line)
            
            if title_match and url_match:
                hot_topics.append({
                    'platform': 'web',
                    'title': title_match.group(1)[:50],
                    'author': '网络热点',
                    'views': 0,
                    'likes': 0,
                    'url': url_match.group(1),
                    'tags': '#今日热点'
                })
    
    return hot_topics[:10]  # 只取前 10 条

def format_report(hot_topics):
    """格式化报告"""
    if not hot_topics:
        return None
    
    lines = [
        f"# 🔥 全网热点汇总（{datetime.now().strftime('%m-%d %H:%M')}）",
        "",
        f"📊 共收集 {len(hot_topics)} 条热点",
        "",
        "### 今日热门话题",
        ""
    ]
    
    for i, topic in enumerate(hot_topics[:5], 1):
        lines.append(f"{i}. **{topic['title']}**")
        if topic['url']:
            lines.append(f"   🔗 {topic['url']}")
        lines.append("")
    
    lines.append("---")
    lines.append(f"_数据来源：SearXNG 搜索 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")
    
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
    print("🔥 全网热点收集（真实数据）")
    print("=" * 60)
    
    # 搜索热点
    hot_topics = search_hot_topics()
    
    # 生成报告
    report = format_report(hot_topics)
    
    # 发送报告
    send_report(report)
    
    print("=" * 60)
