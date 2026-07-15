import socket
import sys

# 从配置文件中获取端口，IP地址通常绑定到 '0.0.0.0' 以监听所有接口
HOST = '0.0.0.0' 
PORT = 65432 # 必须与 config.json 中的 target_port 一致

def start_server():
    """启动Socket服务器，接收来自客户端的数据"""
    
    # 创建一个 TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except OSError as e:
            print(f"错误: 端口 {PORT} 可能已被占用。请更改配置或关闭占用程序。{e}")
            sys.exit(1)
            
        s.listen()
        print(f"服务器正在监听 {HOST}:{PORT} ...")
        
        while True:
            # 等待客户端连接
            conn, addr = s.accept()
            with conn:
                print(f"\n--- 客户端连接: {addr} ---")
                data_chunks = []
                while True:
                    # 接收数据，一次最多 1024 字节
                    data = conn.recv(1024)
                    if not data:
                        break # 连接关闭
                    data_chunks.append(data)
                
                # 合并所有数据块并解码
                full_data = b"".join(data_chunks)
                if full_data:
                    # 假定发送的是 UTF-8 编码的文本
                    received_message = full_data.decode('utf-8', errors='replace')
                    print("✅ 接收到的剪贴板内容:")
                    print("=" * 30)
                    print(received_message)
                    print("=" * 30)
                else:
                    print("未接收到数据。")
                
                # 可选：发送一个响应给客户端
                # conn.sendall("Server received your data.".encode('utf-8'))

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n服务器程序已终止。")
    except Exception as e:
        print(f"服务器发生异常: {e}")