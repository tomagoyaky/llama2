import re

from typing import Dict
from chat import OllamaChat

def file_prompt(user_input: str) -> str:
    """
    Wrap user input with a file management prompt, asking Ollama to output strictly in the format:
    文件名: <文件名>\n内容:\n<文件内容>\n
    Returns the wrapped prompt string.
    """
    import os
    def scan_dir(path, prefix=""):
        result = ""
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                result += f"{prefix}{entry}/\n"
                result += scan_dir(full_path, prefix + "    ")
            else:
                result += f"{prefix}{entry}\n"
        return result

    project_root = os.path.dirname(os.path.abspath(__file__))
    folder_structure = scan_dir(project_root)

    return (
        f"你是一个文件管理助手。你可以执行以下操作：文件创建、删除、随机更新、随机读取。"
        f"当前项目的文件夹结构如下：\n{folder_structure}"
        f"请根据以下用户需求，选择合适的操作并生成操作指令。"
        f"输出必须严格遵循如下格式：\n"
        f"操作类型: <创建|删除|随机更新|随机读取>\n文件名: <文件名>\n路径: <文件路径>\n内容:\n<文件内容或操作说明>\n"
        f"用户需求: {user_input}\n"
        f"不要输出任何解释或多余文本，只输出指定格式的操作类型、文件名、路径和内容。"
    )

def parse_file_response(response: str) -> Dict:
    """
    Parse Ollama's response for file creation. Returns dict with success, filename, filecontent, error.
    """
    match = re.search(
        r'操作类型[:：]\s*(.+?)\n+文件名[:：]\s*(.+?)\n+路径[:：]\s*(.+?)\n+内容[:：]?\s*\n([\s\S]+)',
        response
    )
    if match:
        op_type = match.group(1).strip()
        filename = match.group(2).strip()
        filepath = match.group(3).strip()
        filecontent = match.group(4).strip()
        full_path = os.path.join(filepath, filename) if filepath not in (".", "", "/") else filename
        try:
            if op_type == "创建":
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(filecontent)
            # 这里只实现创建，其他操作类型可扩展
            return {
                'success': True,
                'op_type': op_type,
                'filename': filename,
                'filepath': filepath,
                'filecontent': filecontent,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'op_type': op_type,
                'filename': filename,
                'filepath': filepath,
                'filecontent': filecontent,
                'error': str(e)
            }
    return {
        'success': False,
        'op_type': None,
        'filename': None,
        'filepath': None,
        'filecontent': None,
        'error': 'No valid file output detected.'
    }

# Example usage:
# prompt = file_prompt(user_input)
# response = chat.send_message(prompt)
# result = parse_file_response(response)
