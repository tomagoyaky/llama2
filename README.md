# Ollama Chat - Python命令行聊天程序

一个简单的Python命令行程序，用于与本地Ollama服务进行交互式聊天。

## 功能特点

- 🚀 连接到本地Ollama服务
- 💬 支持流式响应，实时显示回复
- 🔄 维护对话历史记录
- 🎯 支持切换不同模型
- 📋 显示可用模型列表
- 🧹 清除对话历史功能

## 安装要求

1. **Python 3.6+**
2. **Ollama服务** - 需要先安装并运行
3. **依赖包** - requests库

## 安装步骤

### 1. 安装Ollama

访问 [Ollama官网](https://ollama.ai) 下载并安装Ollama。

### 2. 启动Ollama服务

```bash
# 启动Ollama服务
ollama serve
```

### 3. 下载模型

```bash
# 下载一个模型（例如llama2）
ollama pull llama2

# 或者下载其他模型
ollama pull mistral
ollama pull codellama
```

### 4. 安装Python依赖

```bash
cd ollama-chat
pip install -r requirements.txt
```

## 使用方法

### 运行程序

基本运行：
```bash
python chat.py
```

使用参数运行：
```bash
python chat.py --model llama2 --url http://localhost:11434 --thinking --no-stream
```

### 基本使用

程序启动后会自动检测Ollama服务和可用模型。然后你可以直接输入消息开始对话。

### 可用命令

在聊天过程中，你可以使用以下命令：

- `/help` - 显示帮助信息
- `/clear` - 清除对话历史
- `/models` - 显示所有可用模型
- `/model <模型名>` - 切换到指定模型
- `/exit` 或 `/quit` - 退出程序

### 示例对话

```
🤖 Ollama Chat - 命令行聊天程序
==================================================
✅ 已连接到Ollama，可用模型: llama2, mistral
当前使用模型: llama2

输入 /help 查看可用命令
输入 /exit 或 /quit 退出程序
--------------------------------------------------

你: 你好，请介绍一下自己
助手: 你好！我是一个AI助手，基于llama2模型。我可以帮助你回答问题、提供信息、协助解决问题等。

你: /model mistral
已切换到模型: mistral

你: 现在用新模型回答：Python的优点是什么？
助手: Python有很多优点，包括：
1. 语法简洁易读
2. 丰富的标准库和第三方库
3. 跨平台兼容性
...
```

## 故障排除

### 连接问题

如果程序显示"无法连接到Ollama服务"，请检查：

1. Ollama服务是否正在运行：`ollama serve`
2. 服务地址是否正确（默认 http://localhost:11434）
3. 防火墙是否阻止了连接

### 模型问题

如果没有找到可用模型：

1. 使用 `ollama list` 查看已下载的模型
2. 使用 `ollama pull <模型名>` 下载新模型

### 命令行参数

程序支持以下命令行参数：

```bash
# 指定模型
python chat.py --model llama2

# 指定服务地址
python chat.py --url http://localhost:11434

# 启用thinking模式
python chat.py --thinking

# 禁用流式响应
python chat.py --no-stream

# 组合使用
python chat.py --model mistral --url http://192.168.1.100:11434 --thinking --no-stream
```

### 启动脚本参数

Windows (run.cmd):
```cmd
run.bat -m llama2 -t --no-stream
run.bat --model mistral --thinking
```

Linux/Mac (run.sh):
```bash
./run.sh -m llama2 -t
./run.sh --model mistral --url http://localhost:11434 --thinking
```

### 修改默认设置

你可以在创建 `OllamaChat` 实例时修改默认设置：

```python
chat = OllamaChat(
    base_url="http://localhost:11434",  # Ollama服务地址
    model="mistral"  # 默认模型
)
```

## 技术细节

- 使用Ollama的Chat API (`/api/chat`)
- 支持流式响应，提供更好的用户体验
- 自动维护对话上下文
- 错误处理和连接检测

## 许可证

MIT License - 可自由使用和修改
