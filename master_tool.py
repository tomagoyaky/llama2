import re
from typing import Dict
from chat import OllamaChat

def get_question_type(user_input: str, ollama_chat: OllamaChat) -> str:
    """
    Use Ollama to classify the user's question type. Returns type as string, e.g. 'file', 'code', 'other'.
    The prompt asks Ollama to only return the type in the format: TYPE:<type>
    """
    prompt = (
        f"请判断以下用户需求属于哪种类型，只能返回如下格式：TYPE:<类型>。类型包括：file（文件管理相关），code（代码相关），other（其他）。\n"
        f"用户需求: {user_input}\n"
        f"不要输出任何解释或多余文本，只输出类型。"
    )
    response = ollama_chat.send_message(prompt, stream=False)
    match = re.search(r'TYPE:(\w+)', response)
    if match:
        return match.group(1).lower()
    return "other"

# Example usage:
# question_type = get_question_type(user_input, chat)
# if question_type == 'file':
#     ...
