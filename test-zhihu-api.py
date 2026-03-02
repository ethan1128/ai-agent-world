#!/usr/bin/env python3
"""
测试知乎数据获取方法
"""

import requests
from datetime import datetime

def test_method_1():
    """方法 1：直接 API 调用（需要登录）"""
    print("📝 方法 1：直接 API 调用...")
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if 'data' in data:
            print(f"✅ 成功！获取到 {len(data['data'])} 条热榜")
            return True
        else:
            print(f"❌ 失败：{data}")
            return False
    except Exception as e:
        print(f"❌ 失败：{e}")
        return False

def test_method_2():
    """方法 2：使用公开 API（无需登录）"""
    print("📝 方法 2：公开 API...")
    try:
        # 尝试使用第三方聚合 API
        url = "https://api.zhihu.com/topstory/hots"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"状态码：{response.status_code}")
        return False
    except Exception as e:
        print(f"❌ 失败：{e}")
        return False

def test_method_3():
    """方法 3：使用微博热搜替代（公开）"""
    print("📝 方法 3：微博热搜（公开数据）...")
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if 'data' in data and 'realtime' in data['data']:
            hot_list = data['data']['realtime'][:10]
            print(f"✅ 成功！获取到 {len(hot_list)} 条微博热搜")
            for i, item in enumerate(hot_list[:5], 1):
                print(f"  {i}. {item.get('note', '')}")
            return True
        else:
            print(f"❌ 失败：{data}")
            return False
    except Exception as e:
        print(f"❌ 失败：{e}")
        return False

def test_method_4():
    """方法 4：使用百度热搜（公开）"""
    print("📝 方法 4：百度热搜（公开数据）...")
    try:
        # 百度热搜有公开 API
        url = "https://top.baidu.com/board?tab=realtime"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"状态码：{response.status_code}")
        # 需要解析 HTML，这里只测试连通性
        if response.status_code == 200:
            print("✅ 可以访问百度热搜页面")
            return True
        return False
    except Exception as e:
        print(f"❌ 失败：{e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 测试知乎数据获取方法")
    print("=" * 60)
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    results.append(("知乎 API（需登录）", test_method_1()))
    results.append(("知乎公开 API", test_method_2()))
    results.append(("微博热搜（公开）", test_method_3()))
    results.append(("百度热搜（公开）", test_method_4()))
    
    print()
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ 可用" if success else "❌ 不可用"
        print(f"{status} · {name}")
    
    print()
    print("💡 建议：")
    print("1. 微博热搜 - 完全公开，推荐使用")
    print("2. 百度热搜 - 需要解析 HTML，但可用")
    print("3. 知乎 - 需要登录，有封号风险")
    print("=" * 60)
