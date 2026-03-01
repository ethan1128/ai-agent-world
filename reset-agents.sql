-- 清空原有数据
DELETE FROM agents;
DELETE FROM activity_log;
DELETE FROM events;

-- 插入 4 个核心 AI 员工（中文名）
INSERT INTO agents (id, name, role, avatar, status) VALUES
(1, '天枢', '研究主管', '🧙', 'idle'),
(2, '地衡', '情报收集', '🔍', 'idle'),
(3, '文曲', '内容创作', '✍️', 'idle'),
(4, '明镜', '质量审核', '👁️', 'idle');

-- 插入初始化事件
INSERT INTO events (type, data) VALUES 
('system', '{"message": "AI 员工世界 v2.0 - 像素风启动"}');

-- 插入活动日志
INSERT INTO activity_log (agent_id, action, message) VALUES 
(1, 'system', '天枢已上线 - 研究主管'),
(2, 'system', '地衡已上线 - 情报收集'),
(3, 'system', '文曲已上线 - 内容创作'),
(4, 'system', '明镜已上线 - 质量审核');
