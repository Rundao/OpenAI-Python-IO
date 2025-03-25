"""
OpenAI Python I/O 使用示例。
演示如何使用 sse_print 和 sse_input 函数与前端进行交互。
"""

from openai_python_io import sse_print, sse_input
import time

def main():
    """主函数，展示SSE print和input的基本用法"""
    print("Server started. Please initiate a /v1/chat/completions request to establish SSE connection...")
    
    # 测试基本输出功能
    sse_print("Basic output test", "测试基本输出", sep=" | ")
    time.sleep(1)
    
    # 测试多个值和特殊字符
    sse_print("Numbers:", 42, 3.14, "Special chars:", "@#$%", "中文字符", sep=" -> ")
    time.sleep(1)
    
    # 测试不换行输出
    sse_print("This is ", end="")
    sse_print("a single ", end="")
    sse_print("line output")
    time.sleep(1)
    
    # 测试用户输入
    name = sse_input("Please enter your name (请输入您的名字): ")
    sse_print(f"Hello 你好, {name}!")
    
    # 测试简单的输入反馈循环
    while True:
        text = sse_input("Enter some text (or 'q' to quit): ")
        if text.lower() == 'q':
            break
        sse_print("You entered (您输入了):", text)
    
    sse_print("Demo complete! 演示结束！")

if __name__ == "__main__":
    main()