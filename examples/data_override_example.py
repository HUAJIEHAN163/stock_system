#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据覆盖使用示例
演示如何在增量更新时保证当日数据被正确覆盖
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.incremental_updater import IncrementalUpdater

def demo_data_override():
    """演示数据覆盖功能"""
    
    updater = IncrementalUpdater()
    trade_date = "20241201"  # 示例日期
    
    print("🚀 数据覆盖功能演示")
    print("=" * 50)
    
    # 1. 智能覆盖（推荐）- 自动判断覆盖策略
    print("\n1️⃣ 智能覆盖模式")
    success, records, message = updater.ensure_data_override('daily_basic', trade_date)
    print(f"结果: {message}")
    
    # 2. 强制全量覆盖
    print("\n2️⃣ 强制全量覆盖模式")
    success, records, message = updater.ensure_data_override('daily_basic', trade_date, force_override=True)
    print(f"结果: {message}")
    
    # 3. 指定覆盖类型
    print("\n3️⃣ 指定覆盖类型")
    
    # 全量覆盖
    success, records, message = updater.update_date_data_with_override('daily_basic', trade_date, 'full')
    print(f"全量覆盖: {message}")
    
    # 部分覆盖
    success, records, message = updater.update_date_data_with_override('daily_basic', trade_date, 'partial')
    print(f"部分覆盖: {message}")
    
    # 只补充缺失
    success, records, message = updater.update_date_data_with_override('daily_basic', trade_date, 'missing_only')
    print(f"补充缺失: {message}")

if __name__ == "__main__":
    try:
        # demo_data_override()  # 需要有效的tushare token
        print("数据覆盖示例已创建")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")