// 更新交互记录渲染，添加点击跳转
const oldRender = renderContent;
renderContent = function(data) {
    // 原有逻辑...
    // 添加点击事件
    document.querySelectorAll('.interaction-item').forEach(item => {
        item.addEventListener('click', function() {
            const taskId = this.dataset.taskId;
            if (taskId) {
                window.location.href = `/task-detail.html?id=${taskId}`;
            }
        });
    });
};
