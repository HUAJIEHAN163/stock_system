#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API配置测试
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data.api_config import BATCH_1_APIS, BATCH_2_APIS, BATCH_3_APIS, get_time_range

def test_batch_configs():
    """测试批次配置"""
    print("Testing batch configurations...")
    
    # 测试第1批配置
    print(f"Batch 1 APIs: {len(BATCH_1_APIS)}")
    for api_key, config in BATCH_1_APIS.items():
        print(f"  - {api_key}: {config['description']}")
        assert 'api_name' in config
        assert 'table' in config
        assert 'params' in config
        assert 'description' in config
    
    # 测试第2批配置
    print(f"Batch 2 APIs: {len(BATCH_2_APIS)}")
    for api_key, config in BATCH_2_APIS.items():
        print(f"  - {api_key}: {config['description']}")
        assert 'api_name' in config
        assert 'table' in config
        assert 'params' in config
    
    # 测试第3批配置
    print(f"Batch 3 APIs: {len(BATCH_3_APIS)}")
    for api_key, config in BATCH_3_APIS.items():
        print(f"  - {api_key}: {config['description']}")
        assert 'api_name' in config
        assert 'table' in config
        assert 'params' in config
    
    print("All batch configurations are valid")
    return True

def test_time_ranges():
    """测试时间范围配置"""
    print("Testing time range configurations...")
    
    ranges = ['last_1_year', 'last_2_years', 'last_5_years']
    
    for range_type in ranges:
        start_date, end_date = get_time_range(range_type)
        print(f"  {range_type}: {start_date} to {end_date}")
        
        # 验证日期格式
        assert len(start_date) == 8
        assert len(end_date) == 8
        assert start_date.isdigit()
        assert end_date.isdigit()
        assert start_date < end_date
    
    print("All time ranges are valid")
    return True

def test_required_fields():
    """测试必需字段"""
    print("Testing required fields...")
    
    # 检查第1批是否都标记为必需
    for api_key, config in BATCH_1_APIS.items():
        if config.get('required', False):
            print(f"  {api_key}: required")
        else:
            print(f"  {api_key}: optional")
    
    # 检查是否有足够的必需API
    required_count = sum(1 for config in BATCH_1_APIS.values() if config.get('required', False))
    print(f"Required APIs in batch 1: {required_count}")
    
    return True

def test_table_mappings():
    """测试表映射"""
    print("Testing table mappings...")
    
    all_tables = set()
    
    # 收集所有表名
    for batch in [BATCH_1_APIS, BATCH_2_APIS, BATCH_3_APIS]:
        for config in batch.values():
            all_tables.add(config['table'])
    
    print(f"Total unique tables: {len(all_tables)}")
    for table in sorted(all_tables):
        print(f"  - {table}")
    
    # 验证表名格式
    for table in all_tables:
        assert isinstance(table, str)
        assert len(table) > 0
        assert '_' in table or table.isalpha()
    
    print("All table mappings are valid")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("API Configuration Test")
    print("=" * 50)
    
    try:
        # 1. 测试批次配置
        test_batch_configs()
        print()
        
        # 2. 测试时间范围
        test_time_ranges()
        print()
        
        # 3. 测试必需字段
        test_required_fields()
        print()
        
        # 4. 测试表映射
        test_table_mappings()
        
        print("\nAll API configuration tests completed successfully")
        
    except Exception as e:
        print(f"API configuration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()