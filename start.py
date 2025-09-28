#!/usr/bin/env python3
"""
启动脚本 - 用于部署平台
"""

import os
import sys

# 设置环境变量
os.environ.setdefault('FLASK_APP', 'app.py')
os.environ.setdefault('FLASK_ENV', 'production')

# 导入并运行应用
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
