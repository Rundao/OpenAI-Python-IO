# OpenAI Python I/O

[English](README.md) | [简体中文](README-CN.md)

A lightweight Python module that replaces native input and print functions with SSE streaming capabilities compliant with OpenAI Chat Completion specifications.

## Features

- SSE streaming output support
- Compliant with OpenAI Chat Completion API format
- Supports Chinese and UTF-8 encoding
- Automatic message pagination (using "---" separator)
- Simple message queue management
- Plug-and-play API design

## Installation

```bash
conda create -n OpenAIio python=3.12
conda activate OpenAIio

# Install dependencies using requirements.txt
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Quick Start

1. Use in your code:

```python
from openai_python_io import sse_print, sse_input

# Output message
sse_print("Hello, World!")

# Get user input
name = sse_input("What's your name? ")
sse_print(f"Nice to meet you, {name}!")
```

2. Frontend connection:

Send POST request to `http://localhost:2122/v1/chat/completions` with SSE connection. Request format:

```json
{
  "stream": true,
  "messages": [{"role": "user", "content": "Hello"}]
}
```

## API Reference

### sse_print(content: str)
Stream content to frontend via SSE. Messages are automatically paginated.

### sse_input(prompt: str = "") -> str
Wait for and get user input. Sends a special marker to notify frontend that user input is required.

## Examples

Check `openai_python_io/example.py` for complete usage examples including:
- Basic message output
- User input handling
- Chinese support test
- Simple calculator application

## Project Structure

```
openai_python_io/
├── __init__.py    # Main interface
├── server.py      # SSE server implementation
├── utils.py       # Utility classes and message queue
└── example.py     # Usage examples
```

## License

MIT License