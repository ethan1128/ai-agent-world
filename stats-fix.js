// 修复统计数据计算
function updateStats(data) {
    // 交互次数 = 总交互数
    document.getElementById('stat-interactions').textContent = data.interactions.length;
    
    // 进行中任务 = task_assign 且未完成
    const pendingTasks = data.interactions.filter(int => 
        int.task_type === 'task_assign' && int.status === 'pending'
    ).length;
    document.getElementById('stat-tasks').textContent = pendingTasks;
    
    // 已完成任务 = task_complete
    const completedTasks = data.interactions.filter(int => 
        int.task_type === 'task_complete'
    ).length;
    document.getElementById('stat-completed').textContent = completedTasks;
}
