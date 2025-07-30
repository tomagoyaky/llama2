#!/bin/bash

# 设置默认参数
MODEL="qwen3:0.6b"
URL="http://localhost:11434"
THINKING=false
NO_STREAM=true

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -u|--url)
            URL="$2"
            shift 2
            ;;
        -t|--thinking)
            THINKING=true
            shift
            ;;
        --no-stream)
            NO_STREAM=true
            shift
            ;;
        -h|--help)
            echo "使用方法: $0 [选项]"
            echo "选项:"
            echo "  -m, --model MODEL    指定使用的模型 (默认: llama2)"
            echo "  -u, --url URL        指定Ollama服务地址 (默认: http://localhost:11434)"
            echo "  -t, --thinking       启用thinking模式"
            echo "  --no-stream          禁用流式响应"
            echo "  -h, --help           显示帮助信息"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            echo "使用 -h 或 --help 查看帮助"
            exit 1
            ;;
    esac
done

echo "正在启动Ollama Chat..."
echo "模型: $MODEL"
echo "URL: $URL"
[ "$THINKING" = true ] && echo "思考模式: 已启用"
[ "$NO_STREAM" = true ] && echo "流式响应: 已禁用"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3未安装"
    echo "请安装Python 3.6或更高版本"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import requests" &> /dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 构建命令行参数
CMD_ARGS="--model $MODEL --url $URL"
[ "$THINKING" = true ] && CMD_ARGS="$CMD_ARGS --thinking"
[ "$NO_STREAM" = true ] && CMD_ARGS="$CMD_ARGS --no-stream"

# 运行程序
python3 chat.py $CMD_ARGS
