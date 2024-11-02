import socket
import ipaddress

def scan_network(network, port):
    for ip in ipaddress.IPv4Network(network):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # 设置超时
        result = sock.connect_ex((str(ip), port))
        if result == 0:
            print(f'找到接收端: {ip}')
        sock.close()

if __name__ == '__main__':
    scan_network('192.168.1.0/24', 5001)  # 替换为你的网络地址范围
