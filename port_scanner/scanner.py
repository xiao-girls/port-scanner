import socket
import concurrent.futures
import time

class PortScanner:
    def __init__(self, timeout=1, threads=100):
        self.timeout = timeout
        self.threads = threads
    
    def scan_port(self, host, port):
        """扫描单个端口"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((host, port))
                if result == 0:
                    return {'port': port, 'status': 'open'}
                else:
                    return {'port': port, 'status': 'closed'}
        except Exception as e:
            return {'port': port, 'status': 'error', 'message': str(e)}
    
    def scan_ports(self, host, ports, max_workers=None):
        """扫描多个端口"""
        start_time = time.time()
        results = []
        
        # 如果没有指定max_workers，使用实例的threads属性
        if max_workers is None:
            max_workers = self.threads
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_port = {executor.submit(self.scan_port, host, port): port for port in ports}
            for future in concurrent.futures.as_completed(future_to_port):
                results.append(future.result())
        
        end_time = time.time()
        
        return {
            'host': host,
            'ports': results,
            'open_ports': [r['port'] for r in results if r['status'] == 'open'],
            'scan_time': round(end_time - start_time, 2)
        }
    
    def scan_common_ports(self, host):
        """扫描常用端口"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 8080, 8443]
        return self.scan_ports(host, common_ports)
