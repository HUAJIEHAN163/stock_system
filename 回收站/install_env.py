#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare股票系统环境安装脚本
"""

import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示进度"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本符合要求")
    return True

def install_requirements():
    """安装依赖包"""
    print("\n📦 开始安装依赖包...")
    
    # 核心包列表
    packages = [
        "tushare>=1.2.89",
        "tudata>=1.0.0", 
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "jupyter>=1.0.0"
    ]
    
    success_count = 0
    
    for package in packages:
        if run_command(f"pip install {package}", f"安装 {package.split('>=')[0]}"):
            success_count += 1
    
    print(f"\n📊 安装结果: {success_count}/{len(packages)} 个包安装成功")
    return success_count == len(packages)

def create_test_script():
    """创建测试脚本"""
    test_code = '''
import tushare as ts
import tudata
import pandas as pd
import requests
from bs4 import BeautifulSoup

print("🧪 环境测试结果:")
print(f"✅ tushare版本: {ts.__version__}")
print(f"✅ pandas版本: {pd.__version__}")
print(f"✅ requests版本: {requests.__version__}")
print("✅ 所有核心库导入成功!")

# 测试tushare连接（需要token）
print("\\n📡 Tushare连接测试:")
print("请在使用前设置你的tushare token:")
print("ts.set_token('your_token_here')")
print("pro = ts.pro_api()")
'''
    
    with open('test_env.py', 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    print("✅ 测试脚本已创建: test_env.py")

def main():
    """主函数"""
    print("🚀 Tushare股票系统环境安装")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 升级pip
    run_command("python -m pip install --upgrade pip", "升级pip")
    
    # 安装依赖
    if install_requirements():
        print("\n🎉 环境安装完成!")
        
        # 创建测试脚本
        create_test_script()
        
        print("\n📋 下一步操作:")
        print("1. 运行 'python test_env.py' 测试环境")
        print("2. 注册tushare账号获取token: https://tushare.pro/register")
        print("3. 设置token: ts.set_token('your_token_here')")
        print("4. 开始使用股票数据系统!")
        
    else:
        print("\n❌ 环境安装失败，请检查错误信息")

if __name__ == "__main__":
    main()