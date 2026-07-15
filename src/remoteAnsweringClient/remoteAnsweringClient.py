import keyboard
import pyperclip
import json
import socket
import time
import threading
import sys
import os
import logging

# --- Windows 权限检查和提升模块 ---
import ctypes
import subprocess

logging.basicConfig(level=logging.DEBUG)


def is_admin():
    """检查当前用户是否具有管理员权限"""
    try:
        # 尝试获取进程的Token，如果成功则通常是管理员或UAC已授权
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """使用UAC提示符重新运行程序，申请管理员权限"""
    if sys.platform == 'win32' and not is_admin():
        # 获取当前的 Python 解释器路径和脚本路径
        python_executable = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        
        # 构建命令参数，将脚本路径作为参数传递给解释器
        cmd = [python_executable] + sys.argv
        
        # 使用 shell execute API (ShellExecuteW) 运行程序并请求 'runas' 动词
        # 'runas' 会触发 UAC 对话框
        try:
            print("尝试提升权限，请在弹出的窗口中点击'是'。")
            
            # 使用 ShellExecuteW 启动一个新的进程，请求管理员权限
            # hwnd=0 (无父窗口), verb='runas', file=python解释器, 
            # parameters=脚本路径及参数, dir=当前目录, showCmd=1 (正常显示窗口)
            ctypes.windll.shell32.ShellExecuteW(
                None,  # 窗口句柄
                "runas",  # 动词: 请求管理员权限
                python_executable,
                # 将参数列表转换为单个字符串
                " ".join(sys.argv[1:] + [script_path]),
                None,  # 工作目录
                1      # 显示方式 (SW_SHOWNORMAL)
            )
            # 退出当前非管理员进程
            sys.exit(0)
        except Exception as e:
            print(f"权限提升失败: {e}")
            sys.exit(1)
            
# ------------------------------------

CONFIG_FILE = 'config.json'

# ... (load_config, send_clipboard_data, on_ctrl_c_press 函数保持不变) ...
def load_config():
    """从JSON文件加载目标IP和端口"""
    # try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
        return config.get('target_ip'), config.get('target_port')
    # except FileNotFoundError:
    #     logging.error(f"错误: 找不到配置文件 {CONFIG_FILE}")
    #     sys.exit(1)
    # except json.JSONDecodeError:
    #     logging.error(f"错误: 配置文件 {CONFIG_FILE} 格式错误")
    #     sys.exit(1)
    # except Exception as e:
    #     logging.error(f"加载配置时发生未知错误: {e}")
    #     sys.exit(1)

def send_clipboard_data(ip, port, data):
    """通过socket发送剪贴板数据"""
    # ... (代码不变) ...
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            message = data.encode('utf-8')
            s.sendall(message)
            print(f"成功发送 {len(message)} 字节数据到 {ip}:{port}")
    except ConnectionRefusedError:
        print(f"连接失败: 目标服务器 {ip}:{port} 拒绝连接。")
    except socket.timeout:
        print(f"连接超时: 无法连接到 {ip}:{port}。")
    except Exception as e:
        print(f"发送数据时发生错误: {e}")

def on_ctrl_c_press():
    """Ctrl+C 按下后的回调函数"""
    # ... (代码不变) ...
    print("\n--- 检测到 Ctrl+C 快捷键 ---")
    time.sleep(0.1) 
    
    try:
        clipboard_content = pyperclip.paste()
        print(f"剪贴板内容已获取 (长度: {len(clipboard_content)})")
        print(f"内容: {clipboard_content}")
        
        target_ip, target_port = load_config()
        if target_ip and target_port:
            threading.Thread(target=send_clipboard_data, 
                             args=(target_ip, target_port, clipboard_content)).start()
        else:
            print("配置信息不完整，无法发送数据。")

    except pyperclip.PyperclipException as e:
        print(f"获取剪贴板内容时发生错误: {e}")
    except Exception as e:
        print(f"处理 Ctrl+C 事件时发生错误: {e}")

def on_key_event(event):
    """键盘事件处理函数，检查 Ctrl+C 释放"""
    if event.event_type == keyboard.KEY_UP:
        if event.name == 'c' and keyboard.is_pressed('ctrl'):
            on_ctrl_c_press()


def start_monitor():
    """开始监听 Ctrl+C 快捷键"""
    print("剪贴板监控程序启动...")
    print("正在监听 'Ctrl+C' 快捷键...")
    print("按 'Ctrl+Alt+Shift+Q' 退出程序。")
    
    # keyboard.hook(lambda event: on_key_event(event))
    keyboard.add_hotkey('ctrl+c', lambda : on_ctrl_c_press())
    # 退出热键
    keyboard.add_hotkey('ctrl+alt+shift+q', lambda: sys.exit(0))
    
    keyboard.wait()
    

if __name__ == '__main__':
    # --- 核心修改: 在启动时检查权限 ---
    if not is_admin():
        logging.info("当前不是管理员权限。正在请求提升权限...")
        run_as_admin() 
        # 如果 run_as_admin 成功，当前进程会退出，新进程会启动。
    else:
        #检查配置文件是否存在且可用
        try :
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if not (type (config[""])) == str:
                    Exception(f"数据类型不一致")
        except FileNotFoundError:
            logging.warning(f"错误: 找不到配置文件 {CONFIG_FILE}")
        except json.JSONDecodeError:
            logging.warning(f"错误: 配置文件 {CONFIG_FILE} 格式错误")
        except Exception as e:
            logging.error(f"加载配置时发生未知错误: {e}")


        logging.info("已检测到管理员权限。程序继续运行。")
        try:
            start_monitor()
        except KeyboardInterrupt:
            print("\n程序已通过 Ctrl+C (或退出热键) 终止。")
        except Exception as e:
            print(f"\n程序发生异常: {e}")