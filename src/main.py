#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析系统主程序入口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow
from src.__version__ import get_version_info, check_compatibility

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
    # 获取版本信息
    version_info = get_version_info()
    
    print("=" * 50)
    print(f"{version_info['app_name']} {version_info['version']}")
    print(version_info['description'])
    print(f"构建日期: {version_info['build_date']}")
    print(version_info['copyright'])
    print("=" * 50)
    
    # 创建应用程序
    app = setup_application()
    
    # 检查版本兼容性
    print("检查版本兼容性...")
    compatible, message = check_compatibility()
    if not compatible:
        QMessageBox.critical(None, "兼容性检查失败", message)
        return 1
    print(message)
        
    # 检查依赖
    print("检查系统依赖...")
    if not check_dependencies():
        return 1
        
    # 检查目录
    print("检查系统目录...")
    if not check_directories():
        return 1
        
    print("系统检查完成，启动主界面...")
    
    try:
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        print("主界面启动成功")
        print("=" * 50)
        
        # 运行应用程序
        return app.exec_()
        
    except Exception as e:
        QMessageBox.critical(None, "启动失败", f"程序启动失败:\n{str(e)}")
        print(f"启动失败: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())