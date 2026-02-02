import click
from port_scanner.scanner import PortScanner

@click.group()
def cli():
    """端口扫描工具"""
    pass

@cli.command()
@click.argument('host', required=False)
@click.option('--hosts', '-H', type=str, help='指定多个主机，用空格分隔，如：127.0.0.1 192.168.1.1')
@click.option('--port', '-p', type=int, help='指定单个端口')
@click.option('--start-port', '-s', type=int, default=1, help='起始端口')
@click.option('--end-port', '-e', type=int, default=1024, help='结束端口')
@click.option('--common', '-c', is_flag=True, help='扫描常用端口')
@click.option('--timeout', '-t', type=float, default=1.0, help='超时时间(秒)')
@click.option('--threads', '-n', type=int, default=100, help='线程数')
def scan(host, hosts, port, start_port, end_port, common, timeout, threads):
    """扫描指定主机的端口"""
    scanner = PortScanner(timeout=timeout)
    
    # 处理主机列表
    host_list = []
    if host:
        host_list = [host]
    elif hosts:
        try:
            host_list = [h.strip() for h in hosts.split()]
        except Exception:
            click.echo("错误: 主机格式无效，请输入有效的IP地址并使用空格分隔")
            return
    else:
        click.echo("错误: 请指定至少一个主机地址")
        return
    
    # 对每个主机执行扫描
    for current_host in host_list:
        click.echo(f"\n=== 扫描主机: {current_host} ===")
        
        if port:
            # 扫描单个端口
            result = scanner.scan_port(current_host, port)
            status = result['status']
            click.echo(f"端口 {port}: {status}")
            if 'message' in result:
                click.echo(f"  错误: {result['message']}")
        
        elif common:
            # 扫描常用端口
            result = scanner.scan_common_ports(current_host)
            click.echo(f"扫描结果 (主机: {result['host']})")
            click.echo(f"扫描时间: {result['scan_time']}秒")
            click.echo(f"开放端口: {len(result['open_ports'])}个")
            for r in result['ports']:
                if r['status'] == 'open':
                    click.echo(f"  端口 {r['port']}: {r['status']}")
        
        else:
            # 扫描端口范围
            ports_range = range(start_port, end_port + 1)
            result = scanner.scan_ports(current_host, ports_range, max_workers=threads)
            click.echo(f"扫描结果 (主机: {result['host']})")
            click.echo(f"扫描时间: {result['scan_time']}秒")
            click.echo(f"扫描端口: {len(ports_range)}个")
            click.echo(f"开放端口: {len(result['open_ports'])}个")
            if result['open_ports']:
                click.echo(f"开放端口列表: {', '.join(map(str, result['open_ports']))}")

if __name__ == '__main__':
    cli()
