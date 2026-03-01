# 🌐 域名解析部署指南

**域名**: www.ai-flow.top  
**服务器 IP**: 172.24.52.117 (内网)  
**服务端口**: 8888

---

## 📋 方案选择

### 方案 A: 有公网 IP（推荐）

如果你的服务器有公网 IP：

1. 在域名注册商处添加 A 记录
2. 配置 nginx 反向代理
3. 申请 HTTPS 证书

### 方案 B: 无公网 IP（内网穿透）

如果服务器在内网：

1. 使用内网穿透工具（frp/ngrok/cloudflared）
2. 或使用 Cloudflare Tunnel

### 方案 C: 云服务器

如果是阿里云/腾讯云等：

1. 配置安全组开放端口
2. 绑定弹性公网 IP
3. DNS 解析

---

## 🔧 方案 A: 有公网 IP

### 第 1 步：DNS 解析配置

登录你的域名注册商（阿里云/腾讯云等），添加 DNS 记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| A | www | 你的公网 IP | 10 分钟 |
| A | @ | 你的公网 IP | 10 分钟 |

**操作步骤**（以阿里云为例）：

1. 登录 https://dns.console.aliyun.com
2. 找到 `ai-flow.top` 域名
3. 点击「添加记录」
4. 填写：
   - 记录类型：A
   - 主机记录：www
   - 记录值：你的公网 IP
   - TTL：10 分钟
5. 保存

**验证解析**：
```bash
# 等待几分钟后测试
ping www.ai-flow.top
nslookup www.ai-flow.top
```

---

### 第 2 步：安装 nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# CentOS/Alibaba Cloud Linux
sudo yum install nginx -y

# 启动 nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

### 第 3 步：配置 nginx 反向代理

```bash
sudo nano /etc/nginx/sites-available/ai-flow.top
```

添加配置：

```nginx
server {
    listen 80;
    server_name www.ai-flow.top ai-flow.top;

    location / {
        proxy_pass http://localhost:8888;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/ai-flow.top /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 nginx
sudo systemctl restart nginx
```

---

### 第 4 步：申请 HTTPS 证书（Let's Encrypt）

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx -y

# 申请证书
sudo certbot --nginx -d ai-flow.top -d www.ai-flow.top

# 自动续期（已自动添加 cron 任务）
sudo certbot renew --dry-run
```

---

### 第 5 步：验证访问

打开浏览器访问：
- http://www.ai-flow.top
- https://www.ai-flow.top（证书生效后）

---

## 🔧 方案 B: 无公网 IP（内网穿透）

### 使用 Cloudflare Tunnel（推荐）

**优点**：免费、安全、无需公网 IP

#### 第 1 步：安装 cloudflared

```bash
# 下载
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

# 赋予执行权限
chmod +x cloudflared-linux-amd64

# 移动到系统路径
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

#### 第 2 步：配置 Cloudflare

1. 将域名 DNS 托管到 Cloudflare
2. 登录 https://dash.cloudflare.com
3. 进入 Zero Trust → Tunnels
4. 创建 Tunnel
5. 安装 connector
6. 配置 Public Hostname：
   - Domain: www.ai-flow.top
   - Service: http://localhost:8888

#### 第 3 步：启动 Tunnel

```bash
cloudflared tunnel --url http://localhost:8888
```

---

### 使用 frp 内网穿透

#### 第 1 步：准备一台有公网 IP 的服务器

```bash
# 在 VPS 上安装 frps
wget https://github.com/fatedier/frp/releases/download/v0.52.0/frp_0.52.0_linux_amd64.tar.gz
tar -xzf frp_0.52.0_linux_amd64.tar.gz
cd frp_0.52.0_linux_amd64
```

#### 第 2 步：配置 frps（VPS 端）

```ini
# frps.ini
[common]
bind_port = 7000
token = your_token
```

#### 第 3 步：配置 frpc（本地服务器）

```ini
# frpc.ini
[common]
server_addr = your_vps_ip
server_port = 7000
token = your_token

[web]
type = http
local_port = 8888
custom_domains = www.ai-flow.top
```

#### 第 4 步：启动 frp

```bash
# VPS 端
./frps -c frps.ini

# 本地端
./frpc -c frpc.ini
```

---

## 🔧 方案 C: 云服务器（阿里云/腾讯云）

### 第 1 步：配置安全组

登录云服务器控制台：

1. 找到你的实例
2. 进入「安全组」
3. 添加入站规则：
   - 端口：80, 443, 8888
   - 授权对象：0.0.0.0/0
   - 协议：TCP

### 第 2 步：绑定弹性公网 IP

1. 申请弹性公网 IP
2. 绑定到你的实例
3. 记录公网 IP

### 第 3 步：DNS 解析

在域名注册商处添加 A 记录：
- 主机记录：www
- 记录值：你的公网 IP

---

## 📊 当前服务器信息

| 项目 | 值 |
|------|-----|
| **内网 IP** | 172.24.52.117 |
| **服务端口** | 8888 |
| **域名** | www.ai-flow.top |
| **状态** | 🟢 运行中 |

---

## ✅ 快速检查清单

- [ ] 确认服务器有公网 IP（或选择内网穿透）
- [ ] 在域名注册商添加 DNS 记录
- [ ] 安装 nginx
- [ ] 配置反向代理
- [ ] 申请 HTTPS 证书
- [ ] 测试访问
- [ ] 配置防火墙/安全组
- [ ] 设置开机自启动

---

## 🛠️ 常用命令

### nginx 管理

```bash
# 启动
sudo systemctl start nginx

# 停止
sudo systemctl stop nginx

# 重启
sudo systemctl restart nginx

# 查看状态
sudo systemctl status nginx

# 测试配置
sudo nginx -t
```

### 证书管理

```bash
# 查看证书信息
sudo certbot certificates

# 手动续期
sudo certbot renew

# 删除证书
sudo certbot delete --cert-name ai-flow.top
```

### 日志查看

```bash
# nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

---

## 📞 需要帮助？

**告诉我**：
1. 你的域名在哪里注册的？
2. 服务器有公网 IP 吗？
3. 是阿里云/腾讯云/其他？

**我可以帮你**：
- 配置 nginx 反向代理
- 申请 HTTPS 证书
- 设置内网穿透
- 配置防火墙

---

**最后更新**: 2026-03-01
