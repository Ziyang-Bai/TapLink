import socket
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
def hex_to_ip(hex_num):
    return socket.inet_ntoa(struct.pack('!I', int(hex_num, 16)))

def send_file(hex_ip, port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = hex_to_ip(hex_ip)  # 将16进制号码转换回IP地址
    sock.connect((ip, port))
    
    sock.send(filename.encode())  # 发送文件名
    
    with open(filename, 'rb') as f:
        data = f.read(1024)
        while data:
            sock.send(data)
            data = f.read(1024)
    sock.close()
    print('文件发送完毕！')

if __name__ == '__main__':
    print(ostd)
    print("ver - " + version)
    hex_ip = input('请输入接收端的16进制号码: ')  # 用户输入16进制号码
    filename = input('请输入要发送的文件名: ')  # 用户输入文件名
    send_file(hex_ip, 5001, filename)  # 使用用户输入的文件名
