#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析系统GUI启动脚本 - 简化版
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
    from ctypes import wintypes
    
    kernel32 = ctypes.windll.kernel32
    
    # 分配控制台
    if kernel32.AllocConsole():
        # 重定向标准输出到控制台
        import io
        sys.stdout = io.TextIOWrapper(io.FileIO(kernel32.GetStdHandle(-11), 'w'), encoding='utf-8')
        sys.stderr = io.TextIOWrapper(io.FileIO(kernel32.GetStdHandle(-12), 'w'), encoding='utf-8')
        
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
    try:
        print("=" * 60)
        print("股票分析系统启动中...")
        print("=" * 60)
        print("控制台日志已启用")
        print("请保持此控制台窗口打开以查看实时日志")
        print("=" * 60)
        sys.stdout.flush()
    except:
        pass
    
    # 设置日志系统
    logger = setup_logging()
    
    # 测试控制台输出
    try:
        print("测试控制台输出...")
        logger.info("测试日志输出...")
        sys.stdout.flush()
    except Exception as e:
        print(f"控制台输出错误: {e}")
    
    try:
        # 导入并运行主程序
        print("导入主程序...")
        from src.main import main as app_main
        logger.info("开始启动GUI应用程序")
        print("调用主程序...")
        sys.stdout.flush()
        return app_main()
    except ImportError as e:
        error_msg = f"导入错误: {e}"
        print(error_msg)
        logger.error(error_msg)
        print("请确保已安装所有依赖包：pip install -r requirements.txt")
        return 1
    except Exception as e:
        error_msg = f"启动失败: {e}"
        print(error_msg)
        logger.error(error_msg, exc_info=True)
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序异常退出: {e}")
        sys.exit(1)