"""
工具模块，提供消息队列和基础数据结构。
"""

import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class Message:
    """消息类，表示一条需要发送的消息"""
    type: str  # "content" 或 "input_request"
    content: str

class MessageQueue:
    """
    消息队列类，用于管理待发送的消息。
    使用 asyncio.Queue 实现异步消息队列。
    """
    def __init__(self):
        self._queue = asyncio.Queue()
        self.last_user_input: str = ""  # 存储最后一次用户输入

    async def put(self, message: Message):
        """
        将消息放入队列
        
        Args:
            message: Message 对象
        """
        await self._queue.put(message)

    async def get(self) -> Message:
        """
        从队列获取消息
        
        Returns:
            Message: 消息对象
        """
        return await self._queue.get()