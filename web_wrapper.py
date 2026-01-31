#!/usr/bin/env python3
"""
启动Web服务和API接口包装脚本
"""

from port_scanner.app import app

if __name__ == '__main__':
    print("正在启动Web服务...")
    print("访问地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务")
    print("\n服务日志:")
    app.run(debug=True, host='0.0.0.0', port=5000)
