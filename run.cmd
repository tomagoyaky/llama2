@echo off
cls
setlocal enabledelayedexpansion

REM Set default parameters
set MODEL=qwen3:0.6b
set URL=http://localhost:11434
set THINKING=false
set NO_STREAM=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :continue
if "%~1"=="-m" (
    set MODEL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--model" (
    set MODEL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-u" (
    set URL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--url" (
    set URL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-t" (
    set THINKING=true
    shift
    goto :parse_args
)
if "%~1"=="--thinking" (
    set THINKING=true
    shift
    goto :parse_args
)
if "%~1"=="--no-stream" (
    set NO_STREAM=true
    shift
    goto :parse_args
)
shift
goto :parse_args

:continue

echo Starting Ollama Chat...
echo Model: %MODEL%
echo URL: %URL%
if "%THINKING%"=="true" echo Thinking mode: Enabled
if "%NO_STREAM%"=="true" echo Stream response: Disabled

echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not added to PATH
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Build command line arguments
set CMD_ARGS=--model %MODEL% --url %URL%
if "%THINKING%"=="true" set CMD_ARGS=%CMD_ARGS% --thinking
if "%NO_STREAM%"=="true" set CMD_ARGS=%CMD_ARGS% --no-stream

REM Run main program
python chat.py %CMD_ARGS%
pause
