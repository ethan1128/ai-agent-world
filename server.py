#!/usr/bin/env python3
"""
AI 员工世界 - API 服务器 v2.0
像素风 + 中文名 + 4 核心角色
"""

import sqlite3
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'agents-world.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/status':
            self.send_json(get_status())
        elif parsed.path == '/api/agents':
            self.send_json(get_agents())
        elif parsed.path == '/api/tasks':
            self.send_json(get_tasks())
        elif parsed.path == '/api/logs':
            self.send_json(get_logs())
        elif parsed.path == '/api/trigger-task':
            self.send_json(trigger_task())
        elif parsed.path == '/api/content':
            self.send_json(get_content())
        elif parsed.path == '/api/events':
            query = parse_qs(parsed.query)
            limit = int(query.get('limit', [10])[0])
            self.send_json(get_events(limit))
        elif parsed.path == '/api/monitor-data':
            query = parse_qs(parsed.query)
            platform = query.get('platform', ['all'])[0]
            self.send_json(get_monitor_data(platform))
        elif parsed.path == '/monitor-platforms.html':
            self.path = '/content.html'
            super().do_GET()
        elif parsed.path == '/monitor.html':
            self.path = '/monitor.html'
            super().do_GET()
        elif parsed.path == '/':
            self.path = '/index.html'
            super().do_GET()
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/api/proposal':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            self.send_json(create_proposal(post_data))
        elif parsed.path == '/api/start-work':
            self.send_json(start_real_work())
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def get_status():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM agents")
    total_agents = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'busy'")
    active_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed' AND date(completed_at) = date('now')")
    completed_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM content WHERE status = 'published'")
    content_created = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_agents': total_agents,
        'active_tasks': active_tasks,
        'completed_today': completed_today,
        'content_created': content_created,
        'timestamp': datetime.now().isoformat()
    }

def get_agents():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents ORDER BY id")
    agents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'agents': agents}

def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.*, a.name as agent_name 
        FROM tasks t 
        LEFT JOIN agents a ON t.agent_id = a.id 
        ORDER BY t.created_at DESC 
        LIMIT 20
    """)
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'tasks': tasks}

def get_logs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.*, a.name as agent_name, a.avatar 
        FROM activity_log l 
        LEFT JOIN agents a ON l.agent_id = a.id 
        ORDER BY l.created_at DESC 
        LIMIT 50
    """)
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'logs': logs}

def get_content():
    """获取生成的内容"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, a.name as creator_name
        FROM content c
        LEFT JOIN agents a ON c.created_by = a.id
        ORDER BY c.created_at DESC
        LIMIT 20
    """)
    content = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'content': content}

def get_events(limit=10):
    """获取事件记录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'events': events}

def get_monitor_data(platform='all'):
    """获取监控数据"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取统计数据
    if platform == 'all':
        cursor.execute("SELECT platform, COUNT(*) as count FROM platform_monitor GROUP BY platform")
    else:
        cursor.execute("SELECT platform, COUNT(*) as count FROM platform_monitor WHERE platform = ? GROUP BY platform", (platform,))
    
    stats = {'total': 0}
    for row in cursor.fetchall():
        stats[row['platform']] = row['count']
        stats['total'] += row['count']
    
    # 获取内容列表
    if platform == 'all':
        cursor.execute("""
            SELECT * FROM platform_monitor 
            ORDER BY crawl_time DESC 
            LIMIT 50
        """)
    else:
        cursor.execute("""
            SELECT * FROM platform_monitor 
            WHERE platform = ? 
            ORDER BY crawl_time DESC 
            LIMIT 50
        """, (platform,))
    
    content = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {'stats': stats, 'content': content}

def trigger_task():
    """触发一个新任务（用于测试）"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 随机选择一个空闲的智能体
    cursor.execute("SELECT * FROM agents WHERE status = 'idle' LIMIT 1")
    agent = cursor.fetchone()
    
    if agent:
        agent = dict(agent)
        
        # 创建提案
        cursor.execute("""
            INSERT INTO proposals (agent_id, title, description, status)
            VALUES (?, ?, ?, 'approved')
        """, (agent['id'], f"{agent['name']}的任务", "自动触发的测试任务", ))
        proposal_id = cursor.lastrowid
        
        # 任务池
        tasks_pool = [
            '收集中老年情感热点话题',
            '监控竞品账号爆款内容',
            '撰写情感类文案草稿',
            '审核内容质量和合规性'
        ]
        task_title = tasks_pool[agent['id'] - 1]
        
        # 创建任务
        cursor.execute("""
            INSERT INTO tasks (proposal_id, agent_id, title, status, progress, started_at)
            VALUES (?, ?, ?, 'running', 0, ?)
        """, (proposal_id, agent['id'], task_title, datetime.now()))
        task_id = cursor.lastrowid
        
        # 更新智能体状态
        cursor.execute("""
            UPDATE agents SET status = 'busy', current_task = ?, updated_at = ?
            WHERE id = ?
        """, (task_title, datetime.now(), agent['id']))
        
        # 添加活动日志
        cursor.execute("""
            INSERT INTO activity_log (agent_id, action, message)
            VALUES (?, 'working', ?)
        """, (agent['id'], f'开始任务：{task_title}'))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'message': f"已为 {agent['name']} 分配任务",
            'task_id': task_id,
            'agent_name': agent['name']
        }
    else:
        conn.close()
        return {
            'success': False,
            'message': '所有智能体都在忙'
        }

def start_real_work():
    """启动真正的 AI 工作流（预留接口）"""
    # TODO: 集成 OpenClaw sessions_spawn
    return {
        'success': True,
        'message': '工作流启动接口 - 待集成 OpenClaw',
        'workflow': {
            '天枢': '搜索热点话题',
            '地衡': '监控竞品数据',
            '文曲': '创作文案内容',
            '明镜': '审核内容质量'
        }
    }

if __name__ == '__main__':
    port = 8888
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    print(f"🚀 AI 员工世界 API 服务器 v2.0 启动！")
    print(f"📊 监控面板：http://localhost:{port}")
    print(f"🔌 API 端点：http://localhost:{port}/api/status")
    print(f"🤖 AI 员工：天枢 | 地衡 | 文曲 | 明镜")
    print(f"按 Ctrl+C 停止服务器")
    server.serve_forever()
