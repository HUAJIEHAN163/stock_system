#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境测试脚本
"""

def test_imports():
    """测试核心库导入"""
    print("测试核心库导入...")
    
    try:
        import tushare as ts
        print(f"tushare版本: {ts.__version__}")
    except ImportError as e:
        print(f"❌ tushare导入失败: {e}")
        return False
    
    try:
        import tudata
        print("tudata导入成功")
    except ImportError as e:
        print(f"❌ tudata导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        print(f"pandas版本: {pd.__version__}")
    except ImportError as e:
        print(f"❌ pandas导入失败: {e}")
        return False
    
    try:
        import numpy as np
        print(f"numpy版本: {np.__version__}")
    except ImportError as e:
        print(f"❌ numpy导入失败: {e}")
        return False
    
    try:
        import requests
        print(f"requests版本: {requests.__version__}")
    except ImportError as e:
        print(f"❌ requests导入失败: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("beautifulsoup4导入成功")
    except ImportError as e:
        print(f"❌ beautifulsoup4导入失败: {e}")
        return False
    
    return True

def test_tushare_connection():
    """测试tushare连接"""
    print("\n测试Tushare连接...")
    
    try:
        import tushare as ts
        
        # 检查是否设置了token
        try:
            pro = ts.pro_api()
            # 尝试获取交易日历（不需要积分的接口）
            df = pro.trade_cal(exchange='SSE', start_date='20240101', end_date='20240105')
            if not df.empty:
                print("Tushare连接成功!")
                print(f"获取到 {len(df)} 条交易日历数据")
                return True
            else:
                print("Tushare连接成功但未获取到数据")
                return False
        except Exception as e:
            print(f"Tushare连接失败: {e}")
            print("请确保已设置正确的token:")
            print("   ts.set_token('your_token_here')")
            return False
            
    except ImportError:
        print("tushare未安装")
        return False

def test_tudata():
    """测试tudata功能"""
    print("\n测试tudata功能...")
    
    try:
        import tudata as td
        
        # 测试获取股票列表
        df = td.get_stock_list()
        if not df.empty:
            print("tudata功能正常!")
            print(f"获取到 {len(df)} 只股票信息")
            return True
        else:
            print("tudata连接成功但未获取到数据")
            return False
            
    except Exception as e:
        print(f"tudata测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Tushare股票系统环境测试")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("\n基础库导入测试失败，请检查安装")
        return
    
    print("\n所有核心库导入成功!")
    
    # 测试tushare连接
    tushare_ok = test_tushare_connection()
    
    # 测试tudata
    tudata_ok = test_tudata()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结:")
    print(f"核心库导入: 成功")
    print(f"Tushare连接: {'成功' if tushare_ok else '失败'}")
    print(f"Tudata功能: {'成功' if tudata_ok else '失败'}")
    
    if tushare_ok and tudata_ok:
        print("\n环境测试完全通过! 可以开始使用股票数据系统了!")
    else:
        print("\n部分功能测试失败，请检查配置")
        if not tushare_ok:
            print("Tushare使用提示:")
            print("   1. 注册账号: https://tushare.pro/register")
            print("   2. 获取token: https://tushare.pro/user/token")
            print("   3. 设置token: ts.set_token('your_token_here')")

if __name__ == "__main__":
    main()