import socket
import struct
import os

version = "0.1.0"
ostd = r"""
      ______            __    _       __  
     /_  __/___ _____  / /   (_)___  / /__
      / / / __ `/ __ \/ /   / / __ \/ //_/
     / / / /_/ / /_/ / /___/ / / / / ,<   
    /_/  \__,_/ .___/_____/_/_/ /_/_/|_|  
             /_/                           
"""
def extract_filename(file_path):
    if not file_path:
        raise ValueError("文件路径为空或为None")  # 添加检查，确保文件路径有效
    
    file_path = file_path.rstrip('/\\')  # 清理尾部的斜杠
    last_slash_index = max(file_path.rfind('/'), file_path.rfind('\\'))
    if last_slash_index == -1:
        return file_path  # 如果没有路径部分，直接返回文件名
    else:
        return file_path[last_slash_index + 1:]  # 提取文件名

def hex_to_ip(hex_num):
    try:
        return socket.inet_ntoa(struct.pack('!I', int(hex_num, 16)))
    except (struct.error, ValueError):
        return None

def check_receiver_online(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # 设置超时时间为5秒
    try:
        sock.connect((ip, port))
        sock.shutdown(socket.SHUT_RDWR)  # 关闭发送和接收数据
        sock.close()
        return True
    except socket.error as e:
        print(f'检查接收端在线状态时出错: {e}')
        return False

def send_file(hex_ip, port, filepath, filename):
    ip = hex_to_ip(hex_ip)  # 将16进制号码转换回IP地址
    if ip is None:
        print('输入的16进制号码不合法，请重新输入。')
        return

    # 检查接收端是否在线
    if not check_receiver_online(ip, port):
        print('无法连接到接收端，请确认接收端在线并正确设置了IP和端口。')
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
    except socket.error as e:
        print(f'连接失败: {e}')
        return

    try:
        sock.send(filename.encode('utf-8'))  # 发送文件名

        with open(filepath, 'rb') as f:
            data = f.read(1024)
            while data:
                sock.send(data)
                data = f.read(1024)

        # 等待接收确认消息
        confirmation = sock.recv(1024).decode()
        if confirmation == 'FILE_RECEIVED':
            print('文件发送成功，接收端已确认收到文件。')
        else:
            print('文件发送失败，未收到接收端的确认。')
    except socket.error as e:
        print(f'发送文件时出错: {e}')
    finally:
        sock.close()

if __name__ == '__main__':
    print(ostd)
    print("ver - " + version)
    while True:
        hex_ip = input('请输入接收端的16进制号码: ')  # 用户输入16进制号码
        if hex_to_ip(hex_ip):
            break
        else:
            print('不合法的16进制号码，请重新输入。')
    filepath = input('请输入要发送的文件路径: ')
    if not os.path.isfile(filepath):  # 检查文件路径是否有效
        print("文件路径无效，请提供有效的文件路径。")
    else:
        filename = extract_filename(filepath)  # 提取文件名
        send_file(hex_ip, 5001, filepath, filename)  # 发送文件

