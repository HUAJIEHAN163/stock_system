#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本 - 添加基于测试报告的新表结构
"""

import sqlite3
import os
from datetime import datetime

class DatabaseMigration:
    """数据库迁移管理器"""
    
    def __init__(self, db_path="database/stock_data.db"):
        self.db_path = db_path
        
    def migrate_to_latest(self):
        """迁移到最新版本"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 添加基于测试报告的新表
            self._add_stock_company_table(cursor)
            self._add_new_share_table(cursor)
            self._add_adj_factor_table(cursor)
            self._add_index_dailybasic_table(cursor)
            
            # 添加test_status字段到现有表
            self._add_test_status_fields(cursor)
            
            # 创建新索引
            self._create_new_indexes(cursor)
            
            conn.commit()
            print("数据库迁移完成")
            
        except Exception as e:
            conn.rollback()
            print(f"数据库迁移失败: {e}")
            raise
        finally:
            conn.close()
            
    def _add_stock_company_table(self, cursor):
        """添加上市公司基本信息表"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_company (
                ts_code TEXT PRIMARY KEY,
                com_name TEXT,
                chairman TEXT,
                manager TEXT,
                secretary TEXT,
                reg_capital REAL,
                setup_date TEXT,
                province TEXT,
                city TEXT,
                website TEXT,
                email TEXT,
                employees INTEGER,
                main_business TEXT,
                update_time TEXT
            )
        ''')
        
    def _add_new_share_table(self, cursor):
        """添加IPO新股列表表"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_share (
                ts_code TEXT PRIMARY KEY,
                sub_code TEXT,
                name TEXT,
                ipo_date TEXT,
                issue_date TEXT,
                amount REAL,
                market_amount REAL,
                price REAL,
                pe REAL,
                limit_amount REAL,
                funds REAL,
                ballot REAL,
                update_time TEXT
            )
        ''')
        
    def _add_adj_factor_table(self, cursor):
        """添加复权因子表"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adj_factor (
                ts_code TEXT,
                trade_date TEXT,
                adj_factor REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
    def _add_index_dailybasic_table(self, cursor):
        """添加指数每日基本指标表"""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_dailybasic (
                ts_code TEXT,
                trade_date TEXT,
                total_mv REAL,
                float_mv REAL,
                total_share REAL,
                float_share REAL,
                free_share REAL,
                turnover_rate REAL,
                turnover_rate_f REAL,
                pe REAL,
                pe_ttm REAL,
                pb REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
    def _add_test_status_fields(self, cursor):
        """为现有表添加test_status字段"""
        tables_to_update = [
            'stock_basic',
            'trade_calendar', 
            'industry_classify',
            'concept_classify'
        ]
        
        for table in tables_to_update:
            try:
                cursor.execute(f'ALTER TABLE {table} ADD COLUMN test_status TEXT')
            except sqlite3.OperationalError:
                # 字段已存在，跳过
                pass
                
    def _create_new_indexes(self, cursor):
        """创建新表的索引"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_adj_factor_code_date ON adj_factor(ts_code, trade_date)",
            "CREATE INDEX IF NOT EXISTS idx_index_dailybasic_code_date ON index_dailybasic(ts_code, trade_date)",
            "CREATE INDEX IF NOT EXISTS idx_stock_company_name ON stock_company(com_name)",
            "CREATE INDEX IF NOT EXISTS idx_new_share_date ON new_share(ipo_date)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)

if __name__ == "__main__":
    migration = DatabaseMigration()
    migration.migrate_to_latest()