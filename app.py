#!/usr/bin/env python3
"""
简化版 Binance 空投信息平台 - 部署版本
不依赖 twscrape，使用静态数据演示
"""

import json
import sqlite3
import time
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# 配置
DB_PATH = "airdrop_data.db"

# 空投相关关键词
AIRDROP_KEYWORDS = [
    'airdrop', 'airdrops', 'air drop', 'air drops',
    'free tokens', 'free crypto', 'claim', 'claiming',
    'distribution', 'reward', 'rewards', 'bonus',
    'giveaway', 'giveaways', 'contest', 'competition',
    'launch', 'launching', 'new token', 'new coin',
    'listing', 'new listing', 'trading', 'trade',
    'stake', 'staking', 'farm', 'farming',
    'liquidity', 'pool', 'mining', 'yield'
]

# 示例数据
SAMPLE_TWEETS = [
    {
        'id': '1971495540191039743',
        'content': '#Binance is excited to announce the Falcon Finance (FF) HODLer Airdrop – @FalconStable $FF.\n\nBNB Holders, get ready! The Airdrop page will be available on the Binance Airdrop Portal in 24 hours. Plus, this token will be listed on Binance soon!',
        'url': 'https://x.com/binance/status/1971495540191039743',
        'date': '2025-09-26T08:42:20+00:00',
        'likes': 902,
        'retweets': 196,
        'replies': 244,
        'keywords': ['airdrop']
    },
    {
        'id': '1971157525748969513',
        'content': '#Binance is excited to announce the Mira (MIRA) HODLer Airdrop – @Mira_Network $MIRA.\n\nBNB Holders, get ready! The Airdrop page will be available on the Binance Airdrop Portal in 24 hours. Plus, this token will be listed on Binance soon!',
        'url': 'https://x.com/binance/status/1971157525748969513',
        'date': '2025-09-25T10:19:11+00:00',
        'likes': 2197,
        'retweets': 412,
        'replies': 438,
        'keywords': ['airdrop']
    },
    {
        'id': '1972028471208452474',
        'content': 'The Hotcoin Futures Festival is now live!\n\nTrade for a chance to win a share of 200,000 WCT + 440,000 $SHELL in rewards.',
        'url': 'https://x.com/binance/status/1972028471208452474',
        'date': '2025-09-27T20:00:00+00:00',
        'likes': 348,
        'retweets': 61,
        'replies': 164,
        'keywords': ['reward', 'rewards', 'trade']
    },
    {
        'id': '1971122552929124440',
        'content': 'New to crypto and want to grab some BNB?\n\nJoin Binance using the link below and complete KYC to claim up to $10 in BNB — while supplies last.\n\n$300,000 in BNB rewards up for grabs!',
        'url': 'https://x.com/binance/status/1971122552929124440',
        'date': '2025-09-25T08:00:12+00:00',
        'likes': 825,
        'retweets': 184,
        'replies': 250,
        'keywords': ['claim', 'reward', 'rewards']
    },
    {
        'id': '1971303695540421108',
        'content': 'Complete simple tasks to unlock a share of 255,600 @HoloworldAI HOLO token rewards!',
        'url': 'https://x.com/binance/status/1971303695540421108',
        'date': '2025-09-25T20:00:00+00:00',
        'likes': 387,
        'retweets': 62,
        'replies': 75,
        'keywords': ['reward', 'rewards']
    }
]

class SimpleAirdropPlatform:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
        self.load_sample_data()
        
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airdrop_tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE,
                content TEXT,
                url TEXT,
                date TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                is_airdrop BOOLEAN,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """加载示例数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM airdrop_tweets')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 插入示例数据
            for tweet in SAMPLE_TWEETS:
                cursor.execute('''
                    INSERT OR REPLACE INTO airdrop_tweets 
                    (tweet_id, content, url, date, likes, retweets, replies, is_airdrop, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tweet['id'],
                    tweet['content'],
                    tweet['url'],
                    tweet['date'],
                    tweet['likes'],
                    tweet['retweets'],
                    tweet['replies'],
                    True,
                    ','.join(tweet['keywords'])
                ))
        
        conn.commit()
        conn.close()
    
    def get_airdrop_tweets(self, limit: int = 20):
        """从数据库获取空投相关推文"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tweet_id, content, url, date, likes, retweets, replies, keywords
            FROM airdrop_tweets 
            WHERE is_airdrop = 1 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        tweets = []
        for row in cursor.fetchall():
            tweets.append({
                'id': row[0],
                'content': row[1],
                'url': row[2],
                'date': row[3],
                'likes': row[4],
                'retweets': row[5],
                'replies': row[6],
                'keywords': row[7].split(',') if row[7] else []
            })
        
        conn.close()
        return tweets
    
    def get_stats(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总推文数
        cursor.execute('SELECT COUNT(*) FROM airdrop_tweets')
        total_tweets = cursor.fetchone()[0]
        
        # 空投推文数
        cursor.execute('SELECT COUNT(*) FROM airdrop_tweets WHERE is_airdrop = 1')
        airdrop_tweets = cursor.fetchone()[0]
        
        # 今日新增
        today = datetime.now().date()
        cursor.execute('SELECT COUNT(*) FROM airdrop_tweets WHERE DATE(created_at) = ?', (today,))
        today_tweets = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_tweets': total_tweets,
            'airdrop_tweets': airdrop_tweets,
            'today_tweets': today_tweets,
            'airdrop_rate': round((airdrop_tweets / total_tweets * 100), 2) if total_tweets > 0 else 0,
            'last_update': datetime.now().isoformat()
        }

# 全局平台实例
platform = SimpleAirdropPlatform()

@app.route('/')
def index():
    """主页"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Binance 空投信息平台</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            .tweet-card { border-left: 4px solid #28a745; margin-bottom: 1rem; transition: all 0.3s ease; }
            .tweet-card:hover { border-left-color: #20c997; background-color: #f8f9fa; }
            .keyword-badge { background: linear-gradient(45deg, #ff6b6b, #4ecdc4); color: white; font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 12px; margin: 0.125rem; display: inline-block; }
            .status-indicator { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 0.5rem; }
            .status-online { background-color: #28a745; animation: pulse 2s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <i class="fab fa-bitcoin"></i> Binance 空投信息平台
                </a>
                <div class="navbar-nav ms-auto">
                    <span class="navbar-text">
                        <span class="status-indicator status-online"></span>
                        <span id="last-update">演示版本</span>
                    </span>
                </div>
            </div>
        </nav>
        
        <div class="container mt-4">
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body">
                            <h4 class="card-title" id="total-tweets">-</h4>
                            <p class="card-text">总推文数</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                            <h4 class="card-title" id="airdrop-tweets">-</h4>
                            <p class="card-text">空投推文</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body">
                            <h4 class="card-title" id="today-tweets">-</h4>
                            <p class="card-text">今日新增</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-white">
                        <div class="card-body">
                            <h4 class="card-title" id="airdrop-rate">-</h4>
                            <p class="card-text">空投比例</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-info" role="alert">
                <i class="fas fa-info-circle"></i>
                <strong>演示版本</strong> - 这是 Binance 空投信息平台的演示版本，展示最新的空投相关信息。完整版本支持实时爬取功能。
            </div>
            
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5><i class="fas fa-gift text-success"></i> 空投相关信息</h5>
                            <button class="btn btn-sm btn-outline-primary" onclick="loadTweets()">
                                <i class="fas fa-sync-alt"></i> 刷新
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="tweets-container">
                                <div class="text-center py-5">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">加载中...</span>
                                    </div>
                                    <p class="mt-3 text-muted">正在加载空投信息...</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            async function loadTweets() {
                try {
                    const response = await fetch('/api/airdrop-tweets');
                    const data = await response.json();
                    
                    if (data.success) {
                        updateStats(data.stats);
                        renderTweets(data.data);
                        updateLastUpdateTime(data.stats.last_update);
                    }
                } catch (error) {
                    console.error('加载推文失败:', error);
                }
            }
            
            function updateStats(stats) {
                document.getElementById('total-tweets').textContent = stats.total_tweets.toLocaleString();
                document.getElementById('airdrop-tweets').textContent = stats.airdrop_tweets.toLocaleString();
                document.getElementById('today-tweets').textContent = stats.today_tweets.toLocaleString();
                document.getElementById('airdrop-rate').textContent = stats.airdrop_rate + '%';
            }
            
            function updateLastUpdateTime(timestamp) {
                if (timestamp) {
                    const updateTime = new Date(timestamp);
                    const timeString = updateTime.toLocaleTimeString('zh-CN');
                    document.getElementById('last-update').textContent = `最后更新: ${timeString}`;
                }
            }
            
            function renderTweets(tweets) {
                const container = document.getElementById('tweets-container');
                
                if (tweets.length === 0) {
                    container.innerHTML = '<div class="text-center py-5"><h5 class="text-muted">暂无空投相关信息</h5></div>';
                    return;
                }
                
                const tweetsHTML = tweets.map(tweet => `
                    <div class="card tweet-card">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <p class="card-text">${tweet.content}</p>
                                    <div class="text-muted small">
                                        <i class="fab fa-twitter text-primary"></i> 
                                        <strong>@binance</strong> • ${new Date(tweet.date).toLocaleString('zh-CN')}
                                    </div>
                                    <div class="mt-2">
                                        ${tweet.keywords.map(keyword => 
                                            `<span class="keyword-badge">${keyword}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                                <div class="ms-3">
                                    <a href="${tweet.url}" target="_blank" class="btn btn-primary btn-sm">
                                        <i class="fab fa-twitter"></i> 查看
                                    </a>
                                </div>
                            </div>
                            <div class="mt-2">
                                <small class="text-muted">
                                    <i class="fas fa-heart text-danger"></i> ${tweet.likes.toLocaleString()} 
                                    <i class="fas fa-retweet text-success ms-2"></i> ${tweet.retweets.toLocaleString()}
                                    <i class="fas fa-reply text-info ms-2"></i> ${tweet.replies.toLocaleString()}
                                </small>
                            </div>
                        </div>
                    </div>
                `).join('');
                
                container.innerHTML = tweetsHTML;
            }
            
            // 页面加载时获取数据
            loadTweets();
            
            // 每30秒自动刷新
            setInterval(loadTweets, 30000);
        </script>
    </body>
    </html>
    """

@app.route('/api/airdrop-tweets')
def get_airdrop_tweets():
    """获取空投推文 API"""
    limit = request.args.get('limit', 20, type=int)
    tweets = platform.get_airdrop_tweets(limit)
    stats = platform.get_stats()
    
    return jsonify({
        'success': True,
        'data': tweets,
        'stats': stats
    })

if __name__ == '__main__':
    print("🚀 Binance 空投信息平台启动中...")
    print("📊 功能特性:")
    print("   • 展示 Binance 空投相关信息")
    print("   • Web 界面展示")
    print("   • 演示版本")
    print()
    print("🌐 访问地址: http://localhost:8000")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    # 启动 Flask 应用
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
