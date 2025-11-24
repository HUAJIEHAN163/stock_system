#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库功能测试
"""

import sys
import os
import sqlite3

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data.database_manager import DatabaseManager

def test_database_creation():
    """测试数据库创建"""
    print("Testing database table creation...")
    
    db_manager = DatabaseManager("database/test_stock_data.db")
    db_manager.create_all_tables()
    
    # 验证表是否创建成功
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = [
        'stock_basic', 'trade_calendar', 'index_basic', 
        'industry_classify', 'concept_classify',
        'daily_basic', 'index_daily', 'weekly_basic', 'monthly_basic',
        'index_weight', 'hsgt_flow',
        'init_progress', 'data_integrity_log'
    ]
    
    print(f"Created tables: {len(tables)}")
    for table in tables:
        print(f"  - {table}")
    
    # 检查是否所有预期表都创建了
    missing_tables = set(expected_tables) - set(tables)
    if missing_tables:
        print(f"Missing tables: {missing_tables}")
        return False
    
    conn.close()
    print("All expected tables created successfully")
    return True

def test_database_indexes():
    """测试数据库索引"""
    print("Testing database indexes...")
    
    db_manager = DatabaseManager("database/test_stock_data.db")
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # 获取所有索引
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = [row[0] for row in cursor.fetchall()]
    
    print(f"Created indexes: {len(indexes)}")
    for index in indexes:
        print(f"  - {index}")
    
    conn.close()
    return True

def test_data_operations():
    """测试数据操作"""
    print("Testing basic data operations...")
    
    db_manager = DatabaseManager("database/test_stock_data.db")
    
    # 测试插入数据
    import pandas as pd
    
    # 创建测试数据
    test_data = pd.DataFrame({
        'ts_code': ['000001.SZ', '000002.SZ'],
        'symbol': ['000001', '000002'],
        'name': ['平安银行', '万科A'],
        'area': ['深圳', '深圳'],
        'industry': ['银行', '房地产'],
        'market': ['主板', '主板'],
        'list_date': ['19910403', '19910129']
    })
    
    # 插入数据
    records = db_manager.execute_insert('stock_basic', test_data)
    print(f"Inserted {records} records into stock_basic")
    
    # 查询数据
    results = db_manager.execute_query("SELECT COUNT(*) FROM stock_basic")
    count = results[0][0]
    print(f"Total records in stock_basic: {count}")
    
    # 清理测试数据
    db_manager.clear_table_data('stock_basic')
    print("Test data cleaned up")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("Database Functionality Test")
    print("=" * 50)
    
    try:
        # 1. 测试数据库表创建
        if not test_database_creation():
            print("Database creation test failed")
            return
        
        # 2. 测试索引创建
        test_database_indexes()
        
        # 3. 测试数据操作
        test_data_operations()
        
        print("\nAll database tests completed successfully")
        
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()