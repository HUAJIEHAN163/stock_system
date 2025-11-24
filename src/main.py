#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析系统主程序入口
"""

import sys
import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow
from src.__version__ import get_version_info, check_compatibility

# Windows控制台显示
if os.name == 'nt':  # Windows系统
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.AllocConsole()
    
    # 重定向标准输出到控制台
    sys.stdout = open('CONOUT$', 'w')
    sys.stderr = open('CONOUT$', 'w')
    sys.stdin = open('CONIN$', 'r')
    
    # 设置控制台标题
    kernel32.SetConsoleTitleW("股票分析系统 - 日志控制台")

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'PyQt5',
        'pandas', 
        'numpy',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
            
    if missing_packages:
        QMessageBox.critical(None, "依赖检查失败", 
                           f"缺少以下依赖包:\n{', '.join(missing_packages)}\n\n"
                           f"请运行: pip install {' '.join(missing_packages)}")
        return False
        
    return True

def check_directories():
    """检查必要目录"""
    required_dirs = [
        'config',
        'database', 
        'logs',
        'output/exports',
        'output/reports'
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                print(f"创建目录: {dir_path}")
            except Exception as e:
                print(f"创建目录失败 {dir_path}: {e}")
                return False
                
    return True

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

def setup_application():
    """设置应用程序"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    version_info = get_version_info()
    app.setApplicationName(version_info['app_name'])
    app.setApplicationVersion(version_info['version'])
    app.setOrganizationName(version_info['author'])
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 设置应用图标（如果存在）
    icon_path = "assets/icons/app_icon.ico"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # 设置高DPI支持
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    return app

def main():
    """主函数"""
    # 设置日志系统
    logger = setup_logging()
    
    # 获取版本信息
    version_info = get_version_info()
    
    print("=" * 60)
    print(f"[系统启动] {version_info['app_name']} {version_info['version']}")
    print(f"[系统信息] {version_info['description']}")
    print(f"[构建日期] {version_info['build_date']}")
    print(f"[版权信息] {version_info['copyright']}")
    print("=" * 60)
    print("[日志系统] 控制台日志已启用，可在此窗口查看系统运行日志")
    print("[提示信息] 请保持此控制台窗口打开以查看实时日志")
    print("=" * 60)
    
    logger.info(f"系统启动 - {version_info['app_name']} {version_info['version']}")
    
    # 创建应用程序
    app = setup_application()
    logger.info("Qt应用程序初始化完成")
    
    # 检查版本兼容性
    print("[检查项目] 检查版本兼容性...")
    logger.info("开始版本兼容性检查")
    compatible, message = check_compatibility()
    if not compatible:
        logger.error(f"版本兼容性检查失败: {message}")
        QMessageBox.critical(None, "兼容性检查失败", message)
        return 1
    print(f"[检查结果] {message}")
    logger.info(f"版本兼容性检查通过: {message}")
        
    # 检查依赖
    print("[检查项目] 检查系统依赖...")
    logger.info("开始系统依赖检查")
    if not check_dependencies():
        logger.error("系统依赖检查失败")
        return 1
    print("[检查结果] 系统依赖检查通过")
    logger.info("系统依赖检查完成")
        
    # 检查目录
    print("[检查项目] 检查系统目录...")
    logger.info("开始系统目录检查")
    if not check_directories():
        logger.error("系统目录检查失败")
        return 1
    print("[检查结果] 系统目录检查通过")
    logger.info("系统目录检查完成")
        
    print("[系统状态] 系统检查完成，启动主界面...")
    logger.info("所有检查完成，开始启动主界面")
    
    try:
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        print("[启动结果] 主界面启动成功")
        print("=" * 60)
        print("[GUI状态] GUI界面已打开，可以开始使用系统功能")
        print("[日志状态] 日志将在此控制台实时显示")
        print("=" * 60)
        
        logger.info("主界面启动成功")
        logger.info("系统启动完成，进入事件循环")
        
        # 运行应用程序
        result = app.exec_()
        logger.info("应用程序退出")
        return result
        
    except Exception as e:
        error_msg = f"程序启动失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        QMessageBox.critical(None, "启动失败", f"程序启动失败:\n{str(e)}")
        print(f"[错误信息] 启动失败: {e}")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[系统退出] 用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n[异常退出] 程序异常退出: {e}")
        sys.exit(1)