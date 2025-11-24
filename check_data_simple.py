#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def check_data():
    conn = sqlite3.connect("database/stock_data.db")
    cursor = conn.cursor()
    
    print("检查数据库表和数据量")
    print("=" * 50)
    
    # 检查表
    tables = ['stock_basic', 'daily_basic', 'adj_factor', 'stock_company', 'new_share', 'trade_calendar']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} 条记录")
            
            # 检查字段
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"  字段: {', '.join(columns[:10])}...")
            
            # 检查日期范围
            if 'trade_date' in columns:
                cursor.execute(f"SELECT MIN(trade_date), MAX(trade_date) FROM {table}")
                min_date, max_date = cursor.fetchone()
                if min_date:
                    print(f"  日期范围: {min_date} ~ {max_date}")
            
        except Exception as e:
            print(f"{table}: 错误 - {e}")
        
        print()
    
    conn.close()

if __name__ == "__main__":
    check_data()