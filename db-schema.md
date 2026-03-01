# AI 员工矩阵 - 数据库设计

**项目名**：AI-Agent-World-CN  
**创建时间**：2026-03-01  
**版本**：v0.1 MVP

---

## 📊 数据表设计

### 1. agents (智能体表)

```sql
CREATE TABLE agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,           -- 智能体名字
    role TEXT NOT NULL,           -- 角色
    avatar TEXT,                  -- 头像 URL
    status TEXT DEFAULT 'idle',   -- idle/busy/sleep
    current_task TEXT,            -- 当前任务描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 初始化 6 个智能体
INSERT INTO agents (name, role, avatar) VALUES
('Sage', '研究主管', '/avatars/sage.png'),
('Scout', '情报收集', '/avatars/scout.png'),
('Quill', '内容创作', '/avatars/quill.png'),
('Xalt', '社交媒体', '/avatars/xalt.png'),
('Observer', '质量审核', '/avatars/observer.png'),
('Growth', '数据分析', '/avatars/growth.png');
```

---

### 2. proposals (提案表)

```sql
CREATE TABLE proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',  -- pending/approved/rejected
    priority INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);
```

---

### 3. tasks (任务表)

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id INTEGER,
    agent_id INTEGER,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending/running/completed/failed
    progress INTEGER DEFAULT 0,     -- 0-100
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);
```

---

### 4. steps (步骤表)

```sql
CREATE TABLE steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending/running/completed/failed
    order_index INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

---

### 5. events (事件表)

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,             -- task_completed/proposal_created/etc
    data TEXT,                      -- JSON 数据
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### 6. content (内容表)

```sql
CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT,
    platform TEXT,                  -- douyin/kuaishu/xiaohongshu
    status TEXT DEFAULT 'draft',    -- draft/pending/published
    published_at DATETIME,
    metrics_views INTEGER DEFAULT 0,
    metrics_likes INTEGER DEFAULT 0,
    metrics_comments INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,             -- agent_id
    FOREIGN KEY (created_by) REFERENCES agents(id)
);
```

---

### 7. activity_log (活动日志表)

```sql
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER,
    action TEXT NOT NULL,           -- working/thinking/sleeping/etc
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);
```

---

## 🔄 状态流转

### 提案状态
```
pending → approved → (创建任务)
pending → rejected → (结束)
```

### 任务状态
```
pending → running → completed
pending → running → failed
```

### 智能体状态
```
idle → busy → idle
idle → sleep → idle
```

---

## 📡 API 端点设计

```
GET  /api/status          - 获取所有智能体状态
GET  /api/agents/:id      - 获取单个智能体详情
GET  /api/tasks           - 获取任务列表
GET  /api/events          - 获取事件流（SSE）
POST /api/proposals       - 创建提案
POST /api/tasks/:id/complete - 完成任务
```

---

## 🎨 前端展示

### 实时状态面板
- 6 个智能体头像 + 状态
- 当前任务进度条
- 活动日志滚动显示
- 今日数据统计

### 技术栈
- HTML + CSS + JavaScript（纯静态）
- WebSocket 或 SSE 实时更新
- 或者简单轮询（每 5 秒）

---

**维护**：小龙虾一号 | **更新**：实时
