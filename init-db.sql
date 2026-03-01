-- 智能体表
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    avatar TEXT,
    status TEXT DEFAULT 'idle',
    current_task TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 提案表
CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id INTEGER,
    agent_id INTEGER,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- 步骤表
CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    order_index INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- 事件表
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 内容表
CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT,
    platform TEXT,
    status TEXT DEFAULT 'draft',
    published_at DATETIME,
    metrics_views INTEGER DEFAULT 0,
    metrics_likes INTEGER DEFAULT 0,
    metrics_comments INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES agents(id)
);

-- 活动日志表
CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER,
    action TEXT NOT NULL,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- 初始化 6 个智能体
INSERT INTO agents (name, role, avatar, status) VALUES
('Sage', '研究主管', '🧙', 'idle'),
('Scout', '情报收集', '🔍', 'idle'),
('Quill', '内容创作', '✍️', 'idle'),
('Xalt', '社交媒体', '📱', 'idle'),
('Observer', '质量审核', '👁️', 'idle'),
('Growth', '数据分析', '📊', 'idle');

-- 插入欢迎事件
INSERT INTO events (type, data) VALUES ('system', '{"message": "AI 员工世界初始化完成！"}');
INSERT INTO activity_log (agent_id, action, message) VALUES 
(1, 'system', 'Sage 已上线'),
(2, 'system', 'Scout 已上线'),
(3, 'system', 'Quill 已上线'),
(4, 'system', 'Xalt 已上线'),
(5, 'system', 'Observer 已上线'),
(6, 'system', 'Growth 已上线');
