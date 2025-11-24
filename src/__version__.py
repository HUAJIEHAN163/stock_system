#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本信息模块
"""

__version__ = "0.6.0-beta"
__version_info__ = (0, 6, 0, "beta")

# 版本详细信息
VERSION_MAJOR = 0
VERSION_MINOR = 6
VERSION_PATCH = 0
VERSION_PRERELEASE = "beta"

# 构建信息
BUILD_DATE = "2024-12"
BUILD_TYPE = "development"

# 应用信息
APP_NAME = "股票分析系统"
APP_NAME_EN = "Stock Analysis System"
APP_DESCRIPTION = "基于Tushare和Tudata的股票数据分析系统"
APP_AUTHOR = "Stock System Team"
APP_COPYRIGHT = "© 2024 Stock System Team"

# 版本字符串
def get_version():
    """获取完整版本字符串"""
    if VERSION_PRERELEASE:
        return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-{VERSION_PRERELEASE}"
    else:
        return f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

def get_version_info():
    """获取版本信息字典"""
    return {
        "version": get_version(),
        "major": VERSION_MAJOR,
        "minor": VERSION_MINOR,
        "patch": VERSION_PATCH,
        "prerelease": VERSION_PRERELEASE,
        "build_date": BUILD_DATE,
        "build_type": BUILD_TYPE,
        "app_name": APP_NAME,
        "description": APP_DESCRIPTION,
        "author": APP_AUTHOR,
        "copyright": APP_COPYRIGHT
    }

# 兼容性检查
def check_compatibility():
    """检查版本兼容性"""
    import sys
    
    # Python版本检查
    if sys.version_info < (3, 8):
        return False, "需要Python 3.8或更高版本"
    
    # 依赖包检查
    try:
        import PyQt5
        import pandas
        import numpy
    except ImportError as e:
        return False, f"缺少依赖包: {e}"
    
    return True, "版本兼容性检查通过"

if __name__ == "__main__":
    print(f"版本: {get_version()}")
    print(f"应用: {APP_NAME}")
    print(f"描述: {APP_DESCRIPTION}")
    
    compatible, message = check_compatibility()
    print(f"兼容性: {message}")