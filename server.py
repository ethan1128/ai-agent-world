#!/usr/bin/env python3
"""AI 员工世界 - API 服务器"""

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
        elif parsed.path == '/api/employees':
            self.send_json(get_employees())
        elif parsed.path == '/api/interactions':
            query = parse_qs(parsed.query)
            limit = int(query.get('limit', [50])[0])
            self.send_json(get_interactions(limit))
        elif parsed.path == '/api/agents':
            self.send_json(get_agents())
        elif parsed.path == '/api/content':
            self.send_json(get_content())
        elif parsed.path == '/api/monitor-data':
            query = parse_qs(parsed.query)
            platform = query.get('platform', ['all'])[0]
            self.send_json(get_monitor_data(platform))
        elif parsed.path == '/employee-dashboard.html':
            self.path = '/employee-dashboard.html'
            super().do_GET()
        elif parsed.path == '/dashboard.html':
            self.path = '/dashboard.html'
            super().do_GET()
        elif parsed.path == '/':
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def log_message(self, format, *args):
        pass

def get_employees():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'employees': employees}

def get_interactions(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, e1.name as from_name, e1.avatar as from_avatar,
               e2.name as to_name, e2.avatar as to_avatar
        FROM interactions i
        LEFT JOIN employees e1 ON i.from_employee = e1.session_key
        LEFT JOIN employees e2 ON i.to_employee = e2.session_key
        ORDER BY i.created_at DESC LIMIT ?
    ''', (limit,))
    interactions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'interactions': interactions}

def get_status():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM agents")
    total = cursor.fetchone()[0]
    conn.close()
    return {'total_agents': total, 'active_tasks': 0}

def get_agents():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents")
    agents = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'agents': agents}

def get_content():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM content ORDER BY created_at DESC LIMIT 20")
    content = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'content': content}

def get_monitor_data(platform='all'):
    conn = get_db()
    cursor = conn.cursor()
    if platform == 'all':
        cursor.execute("SELECT * FROM platform_monitor ORDER BY crawl_time DESC LIMIT 50")
    else:
        cursor.execute("SELECT * FROM platform_monitor WHERE platform=? ORDER BY crawl_time DESC LIMIT 50", (platform,))
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {'stats': {'total': len(data)}, 'content': data}

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8888), APIHandler)
    print("🚀 Server started on port 8888")
    server.serve_forever()
