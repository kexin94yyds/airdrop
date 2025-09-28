# Binance 空投信息平台

🚀 实时监控和展示 Binance 官方推文中的空投相关信息

## ✨ 功能特性

- **实时爬取** @binance 推文
- **智能筛选** 空投相关信息
- **Web 界面** 美观展示
- **自动更新** 每5分钟自动更新
- **数据存储** SQLite 数据库持久化
- **响应式设计** 支持移动端

## 🎯 空投关键词识别

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

## 🚀 快速开始

### 本地运行

1. **克隆仓库**
```bash
git clone https://github.com/kexin94yyds/airdrop.git
cd airdrop
```

2. **安装依赖**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **配置账号**
```bash
# 创建账号文件
cat > accounts.txt << 'EOF'
username:password:email:email_password:_:cookies
EOF

# 导入账号
twscrape add_accounts accounts.txt username:password:email:email_password:_:cookies
```

4. **启动平台**
```bash
python realtime_platform.py
```

5. **访问平台**
打开浏览器访问: http://localhost:9000

### 部署到生产环境

#### Heroku 部署
```bash
# 安装 Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
```

#### VPS 部署
```bash
# 使用 Gunicorn
gunicorn --bind 0.0.0.0:8000 realtime_platform:app
```

#### Docker 部署
```bash
docker build -t binance-airdrop-platform .
docker run -p 8000:8000 binance-airdrop-platform
```

## 📊 API 接口

- `GET /` - 主页
- `GET /api/airdrop-tweets` - 获取空投推文
- `GET /api/force-update` - 手动触发更新

## 🔧 配置说明

### 环境变量
- `TWS_PROXY`: 代理地址（可选）
- `PORT`: 端口号（Heroku 自动设置）
- `UPDATE_INTERVAL`: 更新间隔（秒，默认300）

### 数据库
- 使用 SQLite 数据库存储推文
- 自动创建数据库文件 `airdrop_data.db`
- 支持数据持久化

## 📈 技术栈

- **后端**: Python, Flask, twscrape
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite
- **部署**: Gunicorn, Docker, Heroku

## 🎨 界面预览

- 响应式设计，支持桌面和移动端
- 实时统计信息展示
- 空投推文卡片式布局
- 关键词标签高亮显示
- 自动刷新机制

## 📝 更新日志

### v1.0.0
- ✅ 基础爬取功能
- ✅ 空投信息筛选
- ✅ Web 界面展示
- ✅ 实时更新机制
- ✅ 数据库存储

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## ⚠️ 免责声明

本项目仅供学习和研究使用，请遵守相关法律法规和平台服务条款。

## 📞 联系方式

- GitHub: [@kexin94yyds](https://github.com/kexin94yyds)
- 项目地址: [https://github.com/kexin94yyds/airdrop](https://github.com/kexin94yyds/airdrop)