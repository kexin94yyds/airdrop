# 🚀 快速部署指南

## 推荐部署平台

### 1. Railway (最推荐) ⭐⭐⭐⭐⭐

**优点**: 对 Python 支持最好，部署简单，免费额度大

**步骤**:
1. 访问 [Railway](https://railway.app)
2. 点击 "Deploy from GitHub repo"
3. 选择仓库: `kexin94yyds/airdrop`
4. 设置环境变量:
   ```
   TWITTER_USERNAME=Kexinyyds
   TWITTER_PASSWORD=your_password
   TWITTER_EMAIL=your_email@example.com
   TWITTER_EMAIL_PASSWORD=your_email_password
   TWITTER_COOKIES=你的cookies字符串
   ```
5. 点击 Deploy

### 2. Render ⭐⭐⭐⭐

**步骤**:
1. 访问 [Render](https://render.com)
2. 点击 "New Web Service"
3. 连接 GitHub 仓库
4. 设置:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. 添加环境变量（同上）
6. 点击 Create Web Service

### 3. Heroku ⭐⭐⭐

**步骤**:
```bash
# 安装 Heroku CLI
heroku login
heroku create your-app-name

# 设置环境变量
heroku config:set TWITTER_USERNAME=Kexinyyds
heroku config:set TWITTER_PASSWORD=your_password
heroku config:set TWITTER_EMAIL=your_email@example.com
heroku config:set TWITTER_EMAIL_PASSWORD=your_email_password
heroku config:set TWITTER_COOKIES="你的cookies"

# 部署
git push heroku main
```

## 🔧 环境变量说明

### 必需的环境变量:
```
TWITTER_USERNAME=Kexinyyds
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email@example.com
TWITTER_EMAIL_PASSWORD=your_email_password
TWITTER_COOKIES=你的cookies字符串
```

### 可选的环境变量:
```
TWS_PROXY=http://your-proxy:port  # 如果需要代理
UPDATE_INTERVAL=300  # 更新间隔(秒)
```

## 📋 获取 Twitter Cookies

1. 登录 Twitter/X
2. 按 F12 打开开发者工具
3. 点击 Application/Storage 标签
4. 找到 Cookies
5. 复制所有 cookies 值，格式如:
   ```
   auth_token=xxx; ct0=yyy; guest_id=zzz; ...
   ```

## 🎯 部署后功能

- ✅ 实时爬取 @binance 推文
- ✅ 智能筛选空投信息
- ✅ 每5分钟自动更新
- ✅ 美观的Web界面
- ✅ 移动端支持
- ✅ API接口

## 🚨 常见问题

### 1. 部署失败
- 检查环境变量是否完整
- 确认 Python 版本兼容性
- 查看构建日志

### 2. 无法爬取推文
- 检查 Twitter 账号状态
- 确认 cookies 有效性
- 检查网络连接

### 3. 更新不工作
- 检查 UPDATE_INTERVAL 设置
- 查看应用日志
- 确认后台任务运行

## 📞 技术支持

如果遇到问题:
1. 检查环境变量配置
2. 查看平台日志
3. 确认 Twitter 账号状态
4. 检查网络连接

---

**推荐**: 使用 Railway 部署，最简单且稳定！
