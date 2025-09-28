#!/usr/bin/env python3
"""
初始化账号脚本
用于部署时自动设置账号
"""

import os
import asyncio
from twscrape import API

async def init_accounts():
    """初始化账号"""
    # 从环境变量获取账号信息
    username = os.environ.get('TWITTER_USERNAME')
    password = os.environ.get('TWITTER_PASSWORD')
    email = os.environ.get('TWITTER_EMAIL')
    email_password = os.environ.get('TWITTER_EMAIL_PASSWORD')
    cookies = os.environ.get('TWITTER_COOKIES')
    
    if not all([username, password, email, email_password, cookies]):
        print("❌ 缺少必要的环境变量:")
        print("   TWITTER_USERNAME")
        print("   TWITTER_PASSWORD") 
        print("   TWITTER_EMAIL")
        print("   TWITTER_EMAIL_PASSWORD")
        print("   TWITTER_COOKIES")
        return False
    
    try:
        api = API()
        
        # 添加账号
        await api.pool.add_account(
            username, password, email, email_password, 
            cookies=cookies
        )
        
        print(f"✅ 账号 {username} 添加成功")
        return True
        
    except Exception as e:
        print(f"❌ 账号初始化失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(init_accounts())
