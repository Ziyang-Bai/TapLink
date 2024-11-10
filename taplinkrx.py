import socket
import os
import struct
version = "0.1.0"
ostd = r"""
      ______            __    _       __  
     /_  __/___ _____  / /   (_)___  / /__
      / / / __ `/ __ \/ /   / / __ \/ //_/
     / / / /_/ / /_/ / /___/ / / / / ,<   
    /_/  \__,_/ .___/_____/_/_/ /_/_/|_|  
             /_/                          
"""
def ip_to_hex(ip):
    return format(struct.unpack("!I", socket.inet_aton(ip))[0], 'x').zfill(8)

def get_unique_filename(base_name):
    index = 1
    new_name = base_name
    while os.path.exists(new_name):
        new_name = f"{base_name}({index})"
        index += 1
    return new_name

def start_receiver(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(5)
    print(f'监听端口 {port}...')

    # 获取本机 IP 地址并转换为 16 进制
    ip_address = socket.gethostbyname(socket.gethostname())
    hex_ip = ip_to_hex(ip_address)
    print(f'接收端的16进制号码: {hex_ip}')

    while True:
        conn, addr = sock.accept()
        print(f'连接来自: {addr}')
        file_name = conn.recv(1024).decode('utf-8')  # 接收文件名
        print(file_name)
        if not file_name:  # 文件名为空，处理错误
            print('接收到的文件名为空，忽略该连接。')
            conn.close()
            continue

        unique_file_name = get_unique_filename(file_name)
        print(f'保存文件名: {unique_file_name}')

        try:
            with open(unique_file_name, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print(f'文件接收完毕，保存为: {unique_file_name}，来自: {hex_ip}')
        except Exception as e:
            print(f'保存文件时出错: {e}')
        
        conn.sendall(b'FILE_RECEIVED')
        conn.close()

if __name__ == '__main__':
    print(ostd)
    print("ver - " + version)
    start_receiver(5001)
