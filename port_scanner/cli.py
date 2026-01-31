import click
from port_scanner.scanner import PortScanner

@click.group()
def cli():
    """端口扫描工具"""
    pass

@cli.command()
@click.argument('host')
@click.option('--port', '-p', type=int, help='指定单个端口')
@click.option('--start-port', '-s', type=int, default=1, help='起始端口')
@click.option('--end-port', '-e', type=int, default=1024, help='结束端口')
@click.option('--common', '-c', is_flag=True, help='扫描常用端口')
@click.option('--timeout', '-t', type=float, default=1.0, help='超时时间(秒)')
@click.option('--threads', '-n', type=int, default=100, help='线程数')
def scan(host, port, start_port, end_port, common, timeout, threads):
    """扫描指定主机的端口"""
    scanner = PortScanner(timeout=timeout)
    
    if port:
        # 扫描单个端口
        result = scanner.scan_port(host, port)
        status = result['status']
        click.echo(f"端口 {port}: {status}")
        if 'message' in result:
            click.echo(f"  错误: {result['message']}")
    
    elif common:
        # 扫描常用端口
        result = scanner.scan_common_ports(host)
        click.echo(f"扫描结果 (主机: {result['host']})")
        click.echo(f"扫描时间: {result['scan_time']}秒")
        click.echo(f"开放端口: {len(result['open_ports'])}个")
        for r in result['ports']:
            if r['status'] == 'open':
                click.echo(f"  端口 {r['port']}: {r['status']}")
    
    else:
        # 扫描端口范围
        ports = range(start_port, end_port + 1)
        result = scanner.scan_ports(host, ports, max_workers=threads)
        click.echo(f"扫描结果 (主机: {result['host']})")
        click.echo(f"扫描时间: {result['scan_time']}秒")
        click.echo(f"扫描端口: {len(ports)}个")
        click.echo(f"开放端口: {len(result['open_ports'])}个")
        if result['open_ports']:
            click.echo(f"开放端口列表: {', '.join(map(str, result['open_ports']))}")

if __name__ == '__main__':
    cli()
