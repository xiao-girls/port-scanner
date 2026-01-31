#!/usr/bin/env python3
"""
Flask应用文件，提供Web界面和API接口
"""

import os
import sys
from flask import Flask, request, jsonify, render_template
from port_scanner.scanner import PortScanner

# 获取项目根目录路径
# 处理PyInstaller打包后的路径问题
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 检查是否是PyInstaller打包环境
if getattr(sys, 'frozen', False):
    # 如果是打包环境，使用sys._MEIPASS获取临时目录
    base_dir = sys._MEIPASS

# 创建Flask应用，指定模板文件夹路径
app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

# Web界面路由
@app.route('/')
def index():
    """Web界面首页"""
    return render_template('index.html')

# API扫描接口
@app.route('/api/scan', methods=['POST'])
def api_scan():
    """端口扫描API接口"""
    try:
        data = request.get_json()
        host = data.get('host')
        port = data.get('port')
        start_port = data.get('start_port')
        end_port = data.get('end_port')
        common = data.get('common', False)
        timeout = data.get('timeout', 1.0)
        threads = data.get('threads', 100)
        
        if not host:
            return jsonify({'error': '主机地址不能为空'}), 400
        
        scanner = PortScanner(timeout=timeout, threads=threads)
        
        if port:
            # 扫描单个端口
            status = scanner.scan_port(host, port)
            return jsonify({
                'host': host,
                'port': port,
                'status': status
            })
        elif start_port and end_port:
            # 扫描端口范围
            ports_range = range(start_port, end_port + 1)
            results = scanner.scan_ports(host, ports_range)
            open_ports = results.get('open_ports', [])
            scan_time = results.get('scan_time', 0)
            
            ports = []
            for port_info in results.get('ports', []):
                ports.append({'port': port_info['port'], 'status': port_info['status']})
            
            return jsonify({
                'host': host,
                'ports': ports,
                'open_ports': open_ports,
                'scan_time': scan_time
            })
        elif common:
            # 扫描常用端口
            results = scanner.scan_common_ports(host)
            open_ports = results.get('open_ports', [])
            scan_time = results.get('scan_time', 0)
            
            ports = []
            for port_info in results.get('ports', []):
                ports.append({'port': port_info['port'], 'status': port_info['status']})
            
            return jsonify({
                'host': host,
                'ports': ports,
                'open_ports': open_ports,
                'scan_time': scan_time
            })
        else:
            return jsonify({'error': '请指定扫描参数'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)