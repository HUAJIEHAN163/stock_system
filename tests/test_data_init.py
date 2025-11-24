#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据初始化测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data.database_manager import DatabaseManager
from src.data.data_initializer import DataInitializer

def test_database_creation():
    """测试数据库创建"""
    print("Testing database creation...")
    
    db_manager = DatabaseManager()
    db_manager.create_all_tables()
    
    print("Database tables created successfully")

def test_token_config():
    """测试Token配置"""
    print("Testing token configuration...")
    
    initializer = DataInitializer()
    token_config = initializer.load_token_config()
    
    if token_config:
        print(f"Token config loaded successfully: {token_config['token_type']}")
        return token_config
    else:
        print("Token config not found")
        return None

def test_batch1_init():
    """测试第1批数据初始化"""
    print("Testing batch 1 data initialization...")
    
    token_config = test_token_config()
    if not token_config:
        print("Skipping initialization test - missing token config")
        return
    
    # 创建初始化器
    initializer = DataInitializer(['batch_1'], token_config)
    
    # 连接信号（简单打印）
    def on_progress(progress, message):
        print(f"[{progress}%] {message}")
    
    def on_batch_completed(batch_name, success, message):
        status = "SUCCESS" if success else "FAILED"
        print(f"{status} {batch_name}: {message}")
    
    def on_finished(success, message, results):
        print(f"\nInitialization completed: {message}")
        if results:
            for batch_name, result in results.items():
                print(f"  {batch_name}: {result['completed_apis']}/{result['total_apis']} APIs, {result['total_records']} records")
    
    initializer.progress_updated.connect(on_progress)
    initializer.batch_completed.connect(on_batch_completed)
    initializer.finished_signal.connect(on_finished)
    
    # 执行初始化
    initializer.run()

def main():
    """主函数"""
    print("=" * 50)
    print("Data Initialization Test")
    print("=" * 50)
    
    try:
        # 1. 测试数据库创建
        test_database_creation()
        
        # 2. 测试Token配置
        test_token_config()
        
        # 3. 测试第1批初始化（如果有Token）
        # test_batch1_init()  # 取消注释以测试实际初始化
        
        print("\nAll tests completed successfully")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    main()