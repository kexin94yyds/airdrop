# 🚀 部署指南 - Binance 空投信息平台

## 📋 部署前准备

### 1. 环境变量配置

在部署平台设置以下环境变量：

```bash
# Twitter 账号信息 (必需)
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email@example.com
TWITTER_EMAIL_PASSWORD=your_email_password
TWITTER_COOKIES=your_cookies_string

# 可选配置
TWS_PROXY=http://your-proxy:port  # 如果需要代理
UPDATE_INTERVAL=300  # 更新间隔(秒)，默认5分钟
```

### 2. 获取 Twitter Cookies

1. 登录 Twitter/X
2. 打开开发者工具 (F12)
3. 在 Application/Storage 标签中找到 Cookies
4. 复制所有 cookies 值，格式如：
   ```
   auth_token=xxx; ct0=yyy; guest_id=zzz; ...
   ```

## 🌐 部署方式

### 方式1: Netlify 部署 (推荐)

1. **连接 GitHub 仓库**
   - 访问 [Netlify](https://netlify.com)
   - 点击 "New site from Git"
   - 选择 GitHub 仓库: `kexin94yyds/airdrop`

2. **配置构建设置**
   ```
   Build command: pip install -r requirements.txt && python init_accounts.py
   Publish directory: /
   ```

3. **设置环境变量**
   - 在 Netlify 控制台添加上述环境变量
   - 确保所有 Twitter 相关变量都已设置

4. **部署**
   - 点击 "Deploy site"
   - 等待构建完成

### 方式2: Heroku 部署

1. **安装 Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # 或下载安装包
   https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **登录并创建应用**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **设置环境变量**
   ```bash
   heroku config:set TWITTER_USERNAME=your_username
   heroku config:set TWITTER_PASSWORD=your_password
   heroku config:set TWITTER_EMAIL=your_email@example.com
   heroku config:set TWITTER_EMAIL_PASSWORD=your_email_password
   heroku config:set TWITTER_COOKIES="auth_token=xxx;ct0=yyy"
   ```

4. **部署**
   ```bash
   git push heroku main
   heroku ps:scale web=1
   ```

### 方式3: VPS 部署

1. **准备服务器**
   ```bash
   # 更新系统
   sudo apt update && sudo apt upgrade -y
   
   # 安装 Python 3.11
   sudo apt install python3.11 python3.11-venv python3.11-dev -y
   
   # 安装其他依赖
   sudo apt install git nginx -y
   ```

2. **克隆并设置项目**
   ```bash
   git clone https://github.com/kexin94yyds/airdrop.git
   cd airdrop
   
   # 创建虚拟环境
   python3.11 -m venv .venv
   source .venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   export TWITTER_USERNAME=your_username
   export TWITTER_PASSWORD=your_password
   export TWITTER_EMAIL=your_email@example.com
   export TWITTER_EMAIL_PASSWORD=your_email_password
   export TWITTER_COOKIES="auth_token=xxx;ct0=yyy"
   ```

4. **启动应用**
   ```bash
   # 使用 Gunicorn
   gunicorn --bind 0.0.0.0:8000 app:app
   
   # 或使用 systemd 服务
   sudo nano /etc/systemd/system/airdrop-platform.service
   ```

## 🔧 实时爬取功能说明

### 自动更新机制
- **更新频率**: 每5分钟自动爬取新推文
- **后台运行**: 独立线程，不影响Web服务
- **智能筛选**: 自动识别空投相关关键词
- **数据持久化**: SQLite数据库存储

### 空投关键词识别
平台会自动识别包含以下关键词的推文：
- airdrop, airdrops, air drop
- free tokens, free crypto
- claim, claiming, distribution
- reward, rewards, bonus
- giveaway, giveaways
- contest, competition
- launch, launching
- new token, new coin
- listing, new listing
- stake, staking, farm, farming
- liquidity, pool, mining, yield

### API 接口
- `GET /` - 主页
- `GET /api/airdrop-tweets` - 获取空投推文
- `GET /api/force-update` - 手动触发更新

## 🚨 常见问题

### 1. 部署失败
- 检查环境变量是否完整设置
- 确认 Python 版本兼容性
- 查看构建日志中的错误信息

### 2. 无法爬取推文
- 检查 Twitter 账号是否正常
- 确认 cookies 是否有效
- 检查网络连接和代理设置

### 3. 更新频率问题
- 调整 `UPDATE_INTERVAL` 环境变量
- 注意 Twitter API 速率限制
- 避免过于频繁的请求

## 📊 监控和维护

### 日志查看
```bash
# Heroku
heroku logs --tail

# Netlify
# 在控制台查看函数日志

# VPS
journalctl -u airdrop-platform -f
```

### 手动更新
访问 `/api/force-update` 端点手动触发更新

### 数据库管理
```bash
# 查看数据库
sqlite3 airdrop_data.db
.tables
SELECT COUNT(*) FROM airdrop_tweets;
```

## 🎯 性能优化建议

1. **更新频率**: 根据需求调整更新间隔
2. **数据清理**: 定期清理旧数据
3. **缓存策略**: 考虑添加 Redis 缓存
4. **负载均衡**: 高并发时使用多实例

## 📞 技术支持

如有问题，请检查：
1. 环境变量配置
2. 网络连接状态
3. Twitter 账号状态
4. 平台日志信息

---

**注意**: 请遵守相关法律法规和平台服务条款，合理使用爬虫功能。
