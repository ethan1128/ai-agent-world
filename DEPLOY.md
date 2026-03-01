# 🚀 部署到 GitHub 指南

## 📋 步骤说明

### 第 1 步：创建 GitHub 仓库

1. 访问 https://github.com
2. 点击右上角 **+** → **New repository**
3. 填写信息：
   - **Repository name**: `ai-agent-world`
   - **Description**: AI 员工世界 - 多智能体内容创作系统
   - **Visibility**: Public（公开）或 Private（私有）
   - **不要勾选** "Initialize this repository with a README"
4. 点击 **Create repository**

---

### 第 2 步：配置 Git 用户信息（首次使用）

```bash
cd ~/.openclaw/workspace/ai-agents-world

# 配置你的 GitHub 邮箱和用户名
git config user.email "your-github-email@example.com"
git config user.name "Your GitHub Name"
```

---

### 第 3 步：添加远程仓库并推送

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-world.git

# 推送代码
git push -u origin master
```

**如果使用 SSH**（推荐）：
```bash
# 添加 SSH 远程仓库
git remote add origin git@github.com:YOUR_USERNAME/ai-agent-world.git

# 推送代码
git push -u origin master
```

---

### 第 4 步：验证推送

访问你的 GitHub 仓库：
```
https://github.com/YOUR_USERNAME/ai-agent-world
```

应该能看到所有代码文件。

---

## 🔐 SSH 密钥配置（如果使用 SSH）

### 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com"
```

### 添加 SSH 密钥到 GitHub

1. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 访问 https://github.com/settings/keys

3. 点击 **New SSH key**

4. 粘贴公钥，保存

---

## 📝 后续维护

### 日常开发流程

```bash
# 1. 修改代码
# 编辑文件...

# 2. 查看更改
git status

# 3. 添加更改
git add .

# 4. 提交
git commit -m "feat: 添加新功能"

# 5. 推送
git push origin master
```

### 版本发布

```bash
# 打标签
git tag -a v1.0 -m "AI 员工世界 v1.0"

# 推送标签
git push origin v1.0
```

---

## 🎯 推荐做法

### 分支管理

```bash
# 创建特性分支
git checkout -b feature/new-feature

# 开发完成后合并到 master
git checkout master
git merge feature/new-feature

# 推送
git push origin master
```

### 提交信息规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 📊 GitHub Pages（可选）

如果想让监控面板可以通过网页访问：

1. 在 GitHub 仓库 → Settings → Pages
2. Source 选择 `master` 分支
3. 保存后访问：`https://YOUR_USERNAME.github.io/ai-agent-world/`

**注意**: 这需要后端 API 也部署到公网。

---

## 🔄 自动同步（可选）

配置 GitHub Actions 自动部署：

1. 创建 `.github/workflows/deploy.yml`
2. 配置 CI/CD 流程
3. 每次推送自动测试和部署

---

## 📞 常见问题

### Q: 推送失败怎么办？

A: 检查：
- Git 用户信息是否配置
- 远程仓库 URL 是否正确
- 是否有网络问题

### Q: 如何修改已提交的代码？

A: 
```bash
# 修改文件
# ...

# 添加并修改上次提交
git add .
git commit --amend -m "新的提交信息"

# 强制推送（谨慎使用）
git push -f origin master
```

### Q: 如何回滚到之前的版本？

A:
```bash
# 查看提交历史
git log

# 回滚到指定版本
git reset --hard COMMIT_HASH

# 强制推送
git push -f origin master
```

---

## 🎉 完成！

现在你的代码已经托管到 GitHub，可以：
- ✅ 长期维护和迭代
- ✅ 与他人协作
- ✅ 版本管理
- ✅ 问题追踪
- ✅ 发布版本

**下一步**：
1. 完善 README.md
2. 添加更多功能
3. 发布 v1.0 版本
4. 分享给其他人使用

---

**维护**：AI Agent World Team  
**最后更新**：2026-03-01
