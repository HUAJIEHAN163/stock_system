@echo off
chcp 65001 >nul
title 股票分析系统 - 控制台日志

echo.
echo ========================================
echo 股票分析系统启动中...
echo ========================================
echo.
echo 提示：此窗口将显示系统运行日志
echo 请保持此窗口打开以查看实时日志
echo.

cd /d "%~dp0"

python launch_gui_with_console.py

echo.
echo ========================================
echo 程序已退出，按任意键关闭窗口
echo ========================================
pause >nul