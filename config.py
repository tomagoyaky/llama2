"""
配置文件 - 可以在此修改默认设置
"""

# Ollama服务配置
DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:0.6b"

# 请求配置
REQUEST_TIMEOUT = 60  # 秒
STREAM_CHUNK_SIZE = 1024  # 字节

# 显示配置
SHOW_WELCOME_MESSAGE = True
SHOW_MODEL_INFO = True
ENABLE_STREAMING = True

# 颜色配置（ANSI颜色代码）
class Colors:
    USER = "\033[94m"      # 蓝色
    ASSISTANT = "\033[92m"  # 绿色
    SYSTEM = "\033[93m"    # 黄色
    ERROR = "\033[91m"     # 红色
    RESET = "\033[0m"      # 重置
