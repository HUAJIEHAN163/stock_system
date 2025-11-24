#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试控制台日志功能
"""

import sys
import os
import logging
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Windows控制台显示
if os.name == 'nt':  # Windows系统
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.AllocConsole()
    
    # 重定向标准输出到控制台
    sys.stdout = open('CONOUT$', 'w', encoding='utf-8')
    sys.stderr = open('CONOUT$', 'w', encoding='utf-8')
    sys.stdin = open('CONIN$', 'r', encoding='utf-8')
    
    # 设置控制台标题
    kernel32.SetConsoleTitleW("股票分析系统 - 日志控制台")

def setup_logging():
    """设置日志系统"""
    # 确保logs目录存在
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            # 文件处理器
            logging.FileHandler(
                os.path.join(log_dir, f'stock_system_{datetime.now().strftime("%Y%m%d")}.log'),
                encoding='utf-8'
            ),
            # 控制台处理器
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 创建应用日志记录器
    logger = logging.getLogger('StockSystem')
    logger.info("日志系统初始化完成")
    return logger

def main():
    """主函数"""
    print("=" * 60)
    print("股票分析系统 - 控制台日志测试")
    print("=" * 60)
    print("控制台日志已启用，可在此窗口查看系统运行日志")
    print("提示: 请保持此控制台窗口打开以查看实时日志")
    print("=" * 60)
    
    # 设置日志系统
    logger = setup_logging()
    
    logger.info("系统启动 - 股票分析系统测试")
    logger.info("控制台日志功能测试")
    
    print("测试日志输出:")
    logger.info("这是一条INFO级别的日志")
    logger.warning("这是一条WARNING级别的日志")
    logger.error("这是一条ERROR级别的日志")
    
    print("\n日志文件保存位置: logs/stock_system_YYYYMMDD.log")
    print("控制台日志测试完成!")
    
    # 模拟一些操作
    import time
    for i in range(5):
        logger.info(f"模拟操作 {i+1}/5")
        time.sleep(1)
    
    logger.info("测试完成")
    print("\n按任意键退出...")
    input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"\n程序异常: {e}")
        import traceback
        traceback.print_exc()