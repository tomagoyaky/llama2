#!/usr/bin/env python3
"""
Ollama Chat - 一个简单的命令行聊天程序
连接到本地Ollama服务进行对话
"""

import requests
import json
import sys
import os
import argparse
from typing import Dict, List, Optional

class OllamaChat:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        初始化Ollama聊天客户端
        
        Args:
            base_url: Ollama服务的基础URL
            model: 使用的模型名称
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_url = f"{self.base_url}/api/chat"
        self.history: List[Dict[str, str]] = []
        
    def check_connection(self) -> bool:
        """检查Ollama服务是否可用"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> List[str]:
        """获取可用的模型列表"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def send_message(self, message: str, stream: bool = True) -> Optional[str]:
        """
        发送消息到Ollama并获取回复
        
        Args:
            message: 用户输入的消息
            stream: 是否使用流式响应
            
        Returns:
            模型的回复内容
        """
        payload = {
            "model": self.model,
            "messages": self.history + [{"role": "user", "content": message}],
            "stream": stream
        }
        
        try:
            if stream:
                return self._handle_streaming_response(payload)
            else:
                response = requests.post(self.api_url, json=payload, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    assistant_message = data['message']['content']
                    self.history.append({"role": "user", "content": message})
                    self.history.append({"role": "assistant", "content": assistant_message})
                    return assistant_message
                else:
                    print(f"错误: HTTP {response.status_code}")
                    return None
        except requests.exceptions.RequestException as e:
            print(f"连接错误: {e}")
            return None
    
    def _handle_streaming_response(self, payload: Dict) -> Optional[str]:
        """处理流式响应"""
        try:
            response = requests.post(self.api_url, json=payload, stream=True, timeout=60)
            if response.status_code != 200:
                print(f"错误: HTTP {response.status_code}")
                return None
            
            print("助手: ", end="", flush=True)
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'message' in data and 'content' in data['message']:
                            content = data['message']['content']
                            print(content, end="", flush=True)
                            full_response += content
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            print()  # 换行
            self.history.append({"role": "user", "content": payload["messages"][-1]["content"]})
            self.history.append({"role": "assistant", "content": full_response})
            return full_response
            
        except requests.exceptions.RequestException as e:
            print(f"连接错误: {e}")
            return None
    
    def clear_history(self):
        """清除对话历史"""
        self.history = []
        print("对话历史已清除")
    
    def set_model(self, model: str):
        """设置使用的模型"""
        available_models = self.get_available_models()
        if model in available_models:
            self.model = model
            print(f"已切换到模型: {model}")
        else:
            print(f"模型 {model} 不可用。可用模型: {', '.join(available_models)}")
    
    def print_help(self):
        """打印帮助信息"""
        print("""
可用命令:
  /help     - 显示此帮助信息
  /clear    - 清除对话历史
  /models   - 显示可用模型
  /model    - 切换模型 (例如: /model llama2)
  /exit     - 退出程序
  /quit     - 退出程序
""")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Ollama Chat - 命令行聊天程序')
    parser.add_argument('--model', '-m', default='llama2', 
                        help='使用的模型名称 (默认: llama2)')
    parser.add_argument('--url', '-u', default='http://localhost:11434',
                        help='Ollama服务地址 (默认: http://localhost:11434)')
    parser.add_argument('--thinking', '-t', action='store_true',
                        help='启用thinking模式 (显示思考过程)')
    parser.add_argument('--no-stream', action='store_true',
                        help='禁用流式响应')
    
    args = parser.parse_args()
    
    print("🤖 Ollama Chat - 命令行聊天程序")
    print("=" * 50)
    
    # 初始化聊天客户端
    chat = OllamaChat(base_url=args.url, model=args.model)
    
    # 检查连接
    if not chat.check_connection():
        print("❌ 无法连接到Ollama服务")
        print("请确保Ollama正在运行: ollama serve")
        sys.exit(1)
    
    # 获取可用模型
    models = chat.get_available_models()
    if not models:
        print("⚠️  没有找到可用的模型")
        print("请使用 'ollama pull <model-name>' 下载模型")
    else:
        print(f"✅ 已连接到Ollama，可用模型: {', '.join(models)}")
        if chat.model not in models:
            print(f"⚠️  指定模型 {chat.model} 不可用，使用第一个可用模型: {models[0]}")
            chat.model = models[0]
        print(f"当前使用模型: {chat.model}")
    
    if args.thinking:
        print("🧠 已启用thinking模式")
    
    print("\n输入 /help 查看可用命令")
    print("输入 /exit 或 /quit 退出程序")
    print("-" * 50)
    
    # 主循环
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command in ['/exit', '/quit']:
                    print("👋 再见！")
                    break
                elif command == '/help':
                    chat.print_help()
                elif command == '/clear':
                    chat.clear_history()
                elif command == '/models':
                    models = chat.get_available_models()
                    print(f"可用模型: {', '.join(models)}")
                elif command.startswith('/model '):
                    model_name = user_input[7:].strip()
                    chat.set_model(model_name)
                else:
                    print("未知命令，输入 /help 查看可用命令")
                continue
            
            # 发送消息
            response = chat.send_message(user_input, stream=not args.no_stream)
            if response is None:
                print("❌ 获取回复失败，请检查Ollama服务状态")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except EOFError:
            print("\n\n👋 再见！")
            break

if __name__ == "__main__":
    main()
