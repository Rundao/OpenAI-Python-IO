"""
OpenAI Python I/O Module
将 Python 的原生 input 和 print 函数替换为符合 OpenAI Chat Completion 规范的 SSE 流式交互功能。
"""

import asyncio
import threading
from typing import Optional
from .server import start_server, send_message, wait_for_input

_server_thread: Optional[threading.Thread] = None
_server_started = threading.Event()

def ensure_server_running():
    """确保服务器正在运行"""
    global _server_thread
    if _server_thread is None:
        _server_thread = threading.Thread(
            target=lambda: asyncio.run(start_server(_server_started)),
            daemon=True
        )
        _server_thread.start()
        _server_started.wait()  # 等待服务器启动完成

def sse_print(*values, sep: str = " ", end: str = "\n") -> None:
    """
    替代 Python 的 print 函数，将内容以 SSE 流式方式发送给前端。
    
    Args:
        *values: 要打印的值
        sep: 值之间的分隔符,默认是空格
        end: 结尾字符,默认是换行符
    """
    ensure_server_running()
    # 将多个值转换为字符串并用分隔符连接
    content = sep.join(str(value) for value in values)
    # 根据 end 参数决定是否添加分行符
    if end == "\n":
        content += "\n\n---\n\n"
    else:
        content += end
    asyncio.run(send_message(content))

def sse_input(prompt: str = "") -> str:
    """
    替代 Python 的 input 函数，从前端获取用户输入。
    
    Args:
        prompt: 输入提示文字
        
    Returns:
        str: 用户输入的内容
    """
    ensure_server_running()
    if prompt:
        asyncio.run(send_message(prompt))
    result = asyncio.run(wait_for_input())
    # 发送确认消息
    asyncio.run(send_message("Input received\n\n---\n\n"))
    return result

__all__ = ['sse_print', 'sse_input']