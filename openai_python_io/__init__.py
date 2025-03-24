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

def sse_print(content: str) -> None:
    """
    替代 Python 的 print 函数，将内容以 SSE 流式方式发送给前端。
    
    Args:
        content: 要发送的内容
    """
    ensure_server_running()
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
    return asyncio.run(wait_for_input())

__all__ = ['sse_print', 'sse_input']