#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def generate_field_coverage_report():
    """生成字段覆盖报告"""
    
    # API字段定义（多只股票多日查询）
    api_fields = {
        'stock_basic': {
            'expected': ['ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'enname', 
                        'cnspell', 'market', 'exchange', 'curr_type', 'list_status', 'list_date', 
                        'delist_date', 'is_hs', 'act_name', 'act_ent_type'],
            'table': 'stock_basic'
        },
        'daily': {
            'expected': ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 
                        'change', 'pct_chg', 'vol', 'amount'],
            'table': 'daily_basic'
        },
        'daily_basic': {
            'expected': ['ts_code', 'trade_date', 'close', 'turnover_rate', 'turnover_rate_f', 
                        'volume_ratio', 'pe', 'pe_ttm', 'pb', 'ps', 'ps_ttm', 'dv_ratio', 
                        'dv_ttm', 'total_share', 'float_share', 'free_share', 'total_mv', 'circ_mv'],
            'table': 'daily_basic'
        },
        'adj_factor': {
            'expected': ['ts_code', 'trade_date', 'adj_factor'],
            'table': 'adj_factor'
        },
        'stock_company': {
            'expected': ['ts_code', 'com_name', 'com_id', 'exchange', 'chairman', 'manager', 
                        'secretary', 'reg_capital', 'setup_date', 'province', 'city', 
                        'introduction', 'website', 'email', 'office', 'employees', 
                        'main_business', 'business_scope'],
            'table': 'stock_company'
        },
        'new_share': {
            'expected': ['ts_code', 'sub_code', 'name', 'ipo_date', 'issue_date', 'amount', 
                        'market_amount', 'price', 'pe', 'limit_amount', 'funds', 'ballot'],
            'table': 'new_share'
        },
        'trade_cal': {
            'expected': ['exchange', 'cal_date', 'is_open', 'pretrade_date'],
            'table': 'trade_calendar'
        }
    }
    
    conn = sqlite3.connect("database/stock_data.db")
    cursor = conn.cursor()
    
    print("多只股票多日查询API字段覆盖报告")
    print("=" * 60)
    
    total_apis = len(api_fields)
    fully_covered = 0
    
    for api_name, config in api_fields.items():
        expected_fields = config['expected']
        table_name = config['table']
        
        try:
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not cursor.fetchone():
                print(f"\n{api_name} -> {table_name}: 表不存在")
                continue
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            db_columns = [row[1] for row in cursor.fetchall()]
            
            # 检查字段覆盖
            covered_fields = []
            missing_fields = []
            
            for field in expected_fields:
                if field in db_columns:
                    covered_fields.append(field)
                else:
                    missing_fields.append(field)
            
            coverage_rate = len(covered_fields) / len(expected_fields) * 100
            
            print(f"\n{api_name} -> {table_name}")
            print(f"  覆盖率: {coverage_rate:.1f}% ({len(covered_fields)}/{len(expected_fields)})")
            
            if coverage_rate == 100:
                fully_covered += 1
                print(f"  状态: 完全覆盖")
            else:
                print(f"  缺失字段: {', '.join(missing_fields)}")
                
        except Exception as e:
            print(f"\n{api_name}: 检查失败 - {e}")
    
    print(f"\n总结:")
    print(f"  完全覆盖: {fully_covered}/{total_apis} ({fully_covered/total_apis*100:.1f}%)")
    
    conn.close()

def check_data_quality():
    """检查数据质量"""
    
    conn = sqlite3.connect("database/stock_data.db")
    cursor = conn.cursor()
    
    print("\n\n数据质量检查报告")
    print("=" * 60)
    
    # 检查daily_basic表数据质量
    print("\n1. daily_basic表数据质量:")
    cursor.execute("SELECT COUNT(*) FROM daily_basic")
    total_records = cursor.fetchone()[0]
    print(f"   总记录数: {total_records:,}")
    
    # 检查空值情况
    quality_fields = ['open', 'high', 'low', 'close', 'vol', 'amount', 'pe', 'pb']
    for field in quality_fields:
        cursor.execute(f"SELECT COUNT(*) FROM daily_basic WHERE {field} IS NULL")
        null_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM daily_basic WHERE {field} = 0")
        zero_count = cursor.fetchone()[0]
        
        null_rate = null_count / total_records * 100 if total_records > 0 else 0
        zero_rate = zero_count / total_records * 100 if total_records > 0 else 0
        
        print(f"   {field}: 空值{null_count}({null_rate:.2f}%), 零值{zero_count}({zero_rate:.2f}%)")
    
    # 检查日期覆盖
    cursor.execute("SELECT MIN(trade_date), MAX(trade_date), COUNT(DISTINCT trade_date) FROM daily_basic")
    min_date, max_date, date_count = cursor.fetchone()
    print(f"   日期范围: {min_date} ~ {max_date} (共{date_count}个交易日)")
    
    # 检查股票覆盖
    cursor.execute("SELECT COUNT(DISTINCT ts_code) FROM daily_basic")
    stock_count = cursor.fetchone()[0]
    print(f"   股票数量: {stock_count}只")
    
    conn.close()

if __name__ == "__main__":
    generate_field_coverage_report()
    check_data_quality()