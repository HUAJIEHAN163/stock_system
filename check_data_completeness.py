#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据完整性脚本
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def check_database_fields():
    """检查数据库字段覆盖情况"""
    
    # API字段定义
    api_fields = {
        'stock_basic': [
            'ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'enname', 
            'cnspell', 'market', 'exchange', 'curr_type', 'list_status', 'list_date', 
            'delist_date', 'is_hs', 'act_name', 'act_ent_type'
        ],
        'daily': [
            'ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 
            'change', 'pct_chg', 'vol', 'amount'
        ],
        'daily_basic': [
            'ts_code', 'trade_date', 'close', 'turnover_rate', 'turnover_rate_f', 
            'volume_ratio', 'pe', 'pe_ttm', 'pb', 'ps', 'ps_ttm', 'dv_ratio', 
            'dv_ttm', 'total_share', 'float_share', 'free_share', 'total_mv', 'circ_mv'
        ],
        'adj_factor': [
            'ts_code', 'trade_date', 'adj_factor'
        ],
        'stock_company': [
            'ts_code', 'com_name', 'com_id', 'exchange', 'chairman', 'manager', 
            'secretary', 'reg_capital', 'setup_date', 'province', 'city', 
            'introduction', 'website', 'email', 'office', 'employees', 
            'main_business', 'business_scope'
        ],
        'new_share': [
            'ts_code', 'sub_code', 'name', 'ipo_date', 'issue_date', 'amount', 
            'market_amount', 'price', 'pe', 'limit_amount', 'funds', 'ballot'
        ],
        'trade_cal': [
            'exchange', 'cal_date', 'is_open', 'pretrade_date'
        ]
    }
    
    conn = sqlite3.connect("database/stock_data.db")
    
    print("检查数据库字段覆盖情况")
    print("=" * 60)
    
    for api_name, expected_fields in api_fields.items():
        # 获取对应的表名
        table_mapping = {
            'stock_basic': 'stock_basic',
            'daily': 'daily_basic',  # 合并到daily_basic表
            'daily_basic': 'daily_basic',
            'adj_factor': 'adj_factor',
            'stock_company': 'stock_company',
            'new_share': 'new_share',
            'trade_cal': 'trade_calendar'
        }
        
        table_name = table_mapping.get(api_name)
        if not table_name:
            continue
            
        try:
            # 检查表是否存在
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if not cursor.fetchone():
                print(f"❌ {api_name} -> {table_name}: 表不存在")
                continue
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            db_columns = [row[1] for row in cursor.fetchall()]
            
            # 检查字段覆盖
            missing_fields = []
            covered_fields = []
            
            for field in expected_fields:
                if field in db_columns:
                    covered_fields.append(field)
                else:
                    missing_fields.append(field)
            
            coverage_rate = len(covered_fields) / len(expected_fields) * 100
            
            print(f"\n📊 {api_name} -> {table_name}")
            print(f"   覆盖率: {coverage_rate:.1f}% ({len(covered_fields)}/{len(expected_fields)})")
            
            if missing_fields:
                print(f"   ❌ 缺失字段: {', '.join(missing_fields)}")
            else:
                print(f"   ✅ 所有字段已覆盖")
                
        except Exception as e:
            print(f"❌ {api_name}: 检查失败 - {e}")
    
    conn.close()

def check_data_completeness():
    """检查数据完整性"""
    
    conn = sqlite3.connect("database/stock_data.db")
    
    print("\n\n📈 检查数据完整性")
    print("=" * 60)
    
    # 检查各表数据量
    tables_to_check = [
        'stock_basic', 'daily_basic', 'adj_factor', 'stock_company', 
        'new_share', 'trade_calendar', 'index_dailybasic'
    ]
    
    for table in tables_to_check:
        try:
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"❌ {table}: 表不存在")
                continue
            
            # 获取总记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_count = cursor.fetchone()[0]
            
            if total_count == 0:
                print(f"❌ {table}: 无数据")
                continue
            
            # 获取日期范围（如果有trade_date字段）
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'trade_date' in columns:
                cursor.execute(f"SELECT MIN(trade_date), MAX(trade_date) FROM {table}")
                min_date, max_date = cursor.fetchone()
                print(f"✅ {table}: {total_count:,}条记录 ({min_date} ~ {max_date})")
                
                # 检查空值情况
                null_stats = []
                for col in ['open', 'high', 'low', 'close', 'vol', 'amount']:
                    if col in columns:
                        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL OR {col} = 0")
                        null_count = cursor.fetchone()[0]
                        if null_count > 0:
                            null_rate = null_count / total_count * 100
                            null_stats.append(f"{col}:{null_count}({null_rate:.1f}%)")
                
                if null_stats:
                    print(f"   ⚠️  空值/零值: {', '.join(null_stats)}")
                else:
                    print(f"   ✅ 数据质量良好")
                    
            else:
                print(f"✅ {table}: {total_count:,}条记录")
                
        except Exception as e:
            print(f"❌ {table}: 检查失败 - {e}")
    
    conn.close()

def check_recent_data():
    """检查最近数据情况"""
    
    conn = sqlite3.connect("database/stock_data.db")
    
    print("\n\n📅 检查最近数据情况")
    print("=" * 60)
    
    try:
        cursor = conn.cursor()
        
        # 获取最近的交易日
        cursor.execute("SELECT MAX(cal_date) FROM trade_calendar WHERE is_open = 1")
        latest_trade_date = cursor.fetchone()[0]
        
        if not latest_trade_date:
            print("❌ 无交易日历数据")
            return
        
        print(f"📅 最新交易日: {latest_trade_date}")
        
        # 检查各表最新数据
        data_tables = ['daily_basic', 'adj_factor', 'index_dailybasic']
        
        for table in data_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"❌ {table}: 表不存在")
                continue
                
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE trade_date = ?", (latest_trade_date,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"✅ {table}: {count}条最新数据")
            else:
                # 查找最近有数据的日期
                cursor.execute(f"SELECT MAX(trade_date) FROM {table}")
                last_date = cursor.fetchone()[0]
                if last_date:
                    print(f"⚠️  {table}: 最新数据日期为 {last_date}")
                else:
                    print(f"❌ {table}: 无任何数据")
    
    except Exception as e:
        print(f"❌ 检查失败: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_database_fields()
    check_data_completeness()
    check_recent_data()