#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析系统启动脚本 - 带控制台日志
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """主函数"""
    # 设置控制台编码
    if os.name == 'nt':  # Windows系统
        os.system('chcp 65001 >nul')
    
    print("🚀 启动股票分析系统（带控制台日志）")
    print("=" * 50)
    
    try:
        # 导入并运行主程序
        from src.main import main as app_main
        return app_main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖包：pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == '__main__':
    # 设置控制台编码
    if os.name == 'nt':  # Windows系统
        os.system('chcp 65001 >nul')
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 程序异常退出: {e}")
        sys.exit(1)