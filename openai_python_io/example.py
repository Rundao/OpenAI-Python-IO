"""
OpenAI Python I/O 使用示例。
演示如何使用 sse_print 和 sse_input 函数与前端进行交互。
"""

from openai_python_io import sse_print, sse_input
import asyncio
import time

def main():
    """主函数，展示基本用法"""
    print("服务已启动，请在前端发起 /v1/chat/completions 请求以建立 SSE 连接...")
    
    # 演示基本输出
    sse_print("这是一条测试消息")
    time.sleep(1)  # 模拟一些处理时间
    
    # 演示多条消息
    sse_print("这是\n\n第一条消息")
    time.sleep(0.5)
    sse_print("这是第二\n\n条消息")
    time.sleep(0.5)
    sse_print("这是第三条\n\n消息")
    
    # 演示用户输入
    name = sse_input("请输入您的名字：")
    sse_print(f"你好，{name}！")
    
    # 演示计算器功能
    while True:
        expression = sse_input(
            "请输入一个算术表达式（例如：1 + 1），输入 'q' 退出："
        )
        
        if expression.lower() == 'q':
            break
            
        try:
            # 注意：在实际应用中应该使用更安全的方式计算表达式
            result = eval(expression)
            sse_print(f"计算结果：{result}")
        except Exception as e:
            sse_print(f"计算错误：{str(e)}")
    
    sse_print("演示结束，感谢使用！")

def test_chinese():
    """测试中文支持"""
    sse_print("测试中文输出功能")
    sse_print("这是一段中文文本，包含特殊字符：！@#￥%……&*（）")
    name = sse_input("请输入一些中文：")
    sse_print(f"您输入的中文是：{name}")

if __name__ == "__main__":
    main()
    # 取消注释下面的行来测试中文支持
    # test_chinese()