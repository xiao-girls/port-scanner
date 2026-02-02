#!/usr/bin/env python3
"""
命令行快速启动端口扫描工具包装脚本
双击运行时会交互式提示输入参数
"""

import sys
from port_scanner.cli import cli

if __name__ == '__main__':
    # 检查是否有命令行参数
    if len(sys.argv) == 1:
        # 没有命令行参数，进入交互式模式
        print("端口扫描工具")
        print("=" * 50)
        
        # 直接输入主机地址，支持单个或多个（空格分隔）
        host_input = input("请输入目标主机地址（单个或多个，用空格分隔）: ")
        if not host_input:
            print("错误: 主机地址不能为空")
            input("按回车键退出...")
            sys.exit(1)
        
        host = ""
        hosts = ""
        
        # 根据输入的主机地址数量判断使用哪种参数
        host_list = host_input.strip().split()
        if len(host_list) == 1:
            # 单个主机
            host = host_list[0]
        else:
            # 多个主机
            hosts = host_input
        
        # 选择扫描类型
        print("\n扫描类型:")
        print("1. 单个端口")
        print("2. 端口范围")
        print("3. 常用端口")
        
        scan_type = input("请选择扫描类型 (1-3): ")
        
        args = ['scan']
        # 根据主机类型设置参数
        if host:
            args.append(host)
        elif hosts:
            args.extend(['--hosts', hosts])
        
        if scan_type == '1':
            # 单个端口
            port = input("请输入端口号: ")
            if port:
                args.extend(['-p', port])
        elif scan_type == '2':
            # 端口范围
            start_port = input("请输入起始端口: ")
            end_port = input("请输入结束端口: ")
            if start_port:
                args.extend(['-s', start_port])
            if end_port:
                args.extend(['-e', end_port])
        elif scan_type == '3':
            # 常用端口
            args.extend(['-c'])
        else:
            print("错误: 无效的扫描类型")
            input("按回车键退出...")
            sys.exit(1)
        
        # 输入超时时间
        timeout = input("\n请输入超时时间(秒，默认1.0): ")
        if timeout:
            args.extend(['-t', timeout])
        
        # 输入线程数
        threads = input("请输入线程数(默认100): ")
        if threads:
            args.extend(['-n', threads])
        
        print("\n扫描参数:")
        print(f"主机: {host if host else hosts}")
        print(f"命令: scan_tool.exe {' '.join(args[1:])}")
        print("\n开始扫描...")
        print("=" * 50)
        
        # 执行扫描，使用standalone_mode=False避免click调用sys.exit()
        try:
            cli(args=args, standalone_mode=False)
        except SystemExit:
            # 捕获SystemExit异常，继续执行后续代码
            pass
        
        # 询问是否再次扫描
        while True:
            retry = input("\n是否再次扫描? (y/n): ")
            if retry.lower() == 'y':
                # 重新开始扫描流程
                print("\n" + "=" * 50)
                print("开始新的扫描")
                print("=" * 50)
                
                # 直接输入主机地址，支持单个或多个（空格分隔）
                host_input = input("请输入目标主机地址（单个或多个，用空格分隔）: ")
                if not host_input:
                    print("错误: 主机地址不能为空")
                    continue
                
                host = ""
                hosts = ""
                
                # 根据输入的主机地址数量判断使用哪种参数
                host_list = host_input.strip().split()
                if len(host_list) == 1:
                    # 单个主机
                    host = host_list[0]
                else:
                    # 多个主机
                    hosts = host_input
                
                # 选择扫描类型
                print("\n扫描类型:")
                print("1. 单个端口")
                print("2. 端口范围")
                print("3. 常用端口")
                
                scan_type = input("请选择扫描类型 (1-3): ")
                
                args = ['scan']
                # 根据主机类型设置参数
                if host:
                    args.append(host)
                elif hosts:
                    args.extend(['--hosts', hosts])
                
                if scan_type == '1':
                    # 单个端口
                    port = input("请输入端口号: ")
                    if port:
                        args.extend(['-p', port])
                elif scan_type == '2':
                    # 端口范围
                    start_port = input("请输入起始端口: ")
                    end_port = input("请输入结束端口: ")
                    if start_port:
                        args.extend(['-s', start_port])
                    if end_port:
                        args.extend(['-e', end_port])
                elif scan_type == '3':
                    # 常用端口
                    args.extend(['-c'])
                else:
                    print("错误: 无效的扫描类型")
                    continue
                
                # 输入超时时间
                timeout = input("\n请输入超时时间(秒，默认1.0): ")
                if timeout:
                    args.extend(['-t', timeout])
                
                # 输入线程数
                threads = input("请输入线程数(默认100): ")
                if threads:
                    args.extend(['-n', threads])
                
                print("\n扫描参数:")
                print(f"主机: {host if host else hosts}")
                print(f"命令: scan_tool.exe {' '.join(args[1:])}")
                print("\n开始扫描...")
                print("=" * 50)
                
                # 执行扫描，使用standalone_mode=False避免click调用sys.exit()
                try:
                    cli(args=args, standalone_mode=False)
                except SystemExit:
                    # 捕获SystemExit异常，继续执行后续代码
                    pass
            elif retry.lower() == 'n':
                print("退出程序...")
                break
            else:
                print("错误: 请输入 y 或 n")
    else:
        # 有命令行参数，直接执行
        cli.main(args=sys.argv[1:])
