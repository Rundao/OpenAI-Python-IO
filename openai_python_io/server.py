"""
服务器模块，处理 HTTP 请求和 SSE 连接。
实现了简单的消息队列和 SSE 流式响应。
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import AsyncGenerator, Dict
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import uvicorn
from .utils import Message, MessageQueue

app = FastAPI()
active_connection: Dict[str, MessageQueue] = {}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """处理聊天补全请求，返回 SSE 流式响应"""
    connection_id = str(uuid.uuid4())
    queue = MessageQueue()
    active_connection[connection_id] = queue
    
    # 获取请求体数据
    body = await request.json()
    # 如果是用户输入消息，存储到队列中
    if "messages" in body and len(body["messages"]) > 0:
        last_message = body["messages"][-1]
        if last_message.get("role") == "user":
            queue.last_user_input = last_message.get("content", "")
    
    return EventSourceResponse(
        handle_chat_stream(connection_id, queue),
        media_type="text/event-stream"
    )

async def handle_chat_stream(connection_id: str, queue: MessageQueue) -> AsyncGenerator[str, None]:
    """处理聊天流式响应"""
    try:
        while True:
            message = await queue.get()
            if message.type == "content":
                response = {
                    "id": str(uuid.uuid4()),
                    "object": "chat.completion.chunk",
                    "created": int(datetime.now().timestamp()),
                    "model": "openai-python-io",
                    "choices": [{
                        "index": 0,
                        "delta": {"content": message.content},
                        "finish_reason": None
                    }]
                }
                yield json.dumps(response, ensure_ascii=False)
            
            elif message.type == "input_request":
                response = {
                    "id": str(uuid.uuid4()),
                    "object": "chat.completion.chunk",
                    "created": int(datetime.now().timestamp()),
                    "model": "openai-python-io",
                    "choices": [{
                        "index": 0,
                        "delta": {},
                        "finish_reason": "input_required"
                    }]
                }
                yield json.dumps(response, ensure_ascii=False)
                yield "[DONE]"
                break  # 结束当前流，等待新的用户输入
    
    except asyncio.CancelledError:
        pass
    finally:
        if connection_id in active_connection:
            del active_connection[connection_id]

async def send_message(content: str):
    """发送消息到活动连接"""
    if not active_connection:
        print("Waiting for client connection...")
        while not active_connection:
            await asyncio.sleep(0.1)
    
    # 发送消息到最新的连接
    connection_id = next(iter(active_connection))
    await active_connection[connection_id].put(Message(type="content", content=content))

async def wait_for_input() -> str:
    """等待用户输入"""
    if not active_connection:
        print("Waiting for client connection...")
        while not active_connection:
            await asyncio.sleep(0.1)
    
    # 通知需要用户输入
    connection_id = next(iter(active_connection))
    queue = active_connection[connection_id]
    await queue.put(Message(type="input_request", content=""))
    
    # 等待新的连接（带有用户输入）
    old_id = connection_id
    while True:
        if len(active_connection) > 0:
            # 获取最新的连接ID
            new_connection_id = next(iter(active_connection))
            if new_connection_id != old_id:
                # 获取新连接的队列中存储的用户输入
                new_queue = active_connection[new_connection_id]
                user_input = new_queue.last_user_input
                old_id = new_connection_id
                return user_input
        await asyncio.sleep(0.1)

async def start_server(started_event: asyncio.Event):
    """启动服务器"""
    config = uvicorn.Config(
        app=app,
        host="127.0.0.1",
        port=2122,
        log_level="error"
    )
    server = uvicorn.Server(config)
    
    async def start():
        started_event.set()
        await server.serve()
    
    await start()