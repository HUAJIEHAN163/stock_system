#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理器 - 负责数据库创建和管理
"""

import os
import sqlite3
from datetime import datetime

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path="database/stock_data.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        
    def ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
    def create_all_tables(self):
        """创建所有数据表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 基础数据表
        self._create_basic_tables(cursor)
        
        # 行情数据表
        self._create_market_tables(cursor)
        
        # 扩展数据表
        self._create_extended_tables(cursor)
        
        # 系统表
        self._create_system_tables(cursor)
        
        # 创建索引
        self._create_indexes(cursor)
        
        conn.commit()
        conn.close()
        
    def _create_basic_tables(self, cursor):
        """创建基础数据表"""
        
        # 股票基本信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_basic (
                ts_code TEXT PRIMARY KEY,
                symbol TEXT,
                name TEXT,
                area TEXT,
                industry TEXT,
                market TEXT,
                list_date TEXT,
                delist_date TEXT,
                is_hs TEXT,
                update_time TEXT
            )
        ''')
        
        # 交易日历表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_calendar (
                cal_date TEXT PRIMARY KEY,
                is_open INTEGER,
                pretrade_date TEXT,
                update_time TEXT
            )
        ''')
        
        # 指数基本信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_basic (
                ts_code TEXT PRIMARY KEY,
                name TEXT,
                market TEXT,
                publisher TEXT,
                category TEXT,
                base_date TEXT,
                base_point REAL,
                list_date TEXT,
                update_time TEXT
            )
        ''')
        
        # 行业分类表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS industry_classify (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                industry_code TEXT,
                industry_name TEXT,
                level INTEGER,
                parent_code TEXT,
                src TEXT,
                update_time TEXT,
                UNIQUE(industry_code, src)
            )
        ''')
        
        # 概念分类表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concept_classify (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_code TEXT,
                concept_name TEXT,
                src TEXT,
                update_time TEXT,
                UNIQUE(concept_code, src)
            )
        ''')
        
    def _create_market_tables(self, cursor):
        """创建行情数据表"""
        
        # A股日线行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_basic (
                ts_code TEXT,
                trade_date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                pre_close REAL,
                change REAL,
                pct_chg REAL,
                vol REAL,
                amount REAL,
                turnover_rate REAL,
                volume_ratio REAL,
                pe REAL,
                pb REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
        # 指数日线行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_daily (
                ts_code TEXT,
                trade_date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                pre_close REAL,
                change REAL,
                pct_chg REAL,
                vol REAL,
                amount REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
        # 周线行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_basic (
                ts_code TEXT,
                trade_date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                pre_close REAL,
                change REAL,
                pct_chg REAL,
                vol REAL,
                amount REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
        # 月线行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_basic (
                ts_code TEXT,
                trade_date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                pre_close REAL,
                change REAL,
                pct_chg REAL,
                vol REAL,
                amount REAL,
                update_time TEXT,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
    def _create_extended_tables(self, cursor):
        """创建扩展数据表"""
        
        # 指数成分股表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_weight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                index_code TEXT,
                con_code TEXT,
                trade_date TEXT,
                weight REAL,
                in_date TEXT,
                out_date TEXT,
                index_type TEXT,
                update_time TEXT,
                UNIQUE(index_code, con_code, trade_date)
            )
        ''')
        
        # 沪深股通资金流向表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hsgt_flow (
                trade_date TEXT PRIMARY KEY,
                ggt_ss REAL,
                ggt_sz REAL,
                hgt REAL,
                sgt REAL,
                north_money REAL,
                south_money REAL,
                update_time TEXT
            )
        ''')
        
    def _create_system_tables(self, cursor):
        """创建系统表"""
        
        # 初始化进度表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS init_progress (
                batch_name TEXT,
                api_name TEXT,
                status TEXT,
                start_time TEXT,
                end_time TEXT,
                progress INTEGER,
                total_records INTEGER,
                error_msg TEXT,
                PRIMARY KEY (batch_name, api_name)
            )
        ''')
        
        # 数据完整性日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_integrity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                trade_date TEXT,
                expected_count INTEGER,
                actual_count INTEGER,
                missing_count INTEGER,
                missing_rate REAL,
                check_time TEXT,
                status TEXT
            )
        ''')
        
    def _create_indexes(self, cursor):
        """创建索引"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_daily_code_date ON daily_basic(ts_code, trade_date)",
            "CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_basic(trade_date)",
            "CREATE INDEX IF NOT EXISTS idx_index_daily_code_date ON index_daily(ts_code, trade_date)",
            "CREATE INDEX IF NOT EXISTS idx_stock_basic_market ON stock_basic(market)",
            "CREATE INDEX IF NOT EXISTS idx_stock_basic_industry ON stock_basic(industry)",
            "CREATE INDEX IF NOT EXISTS idx_trade_calendar_date ON trade_calendar(cal_date)",
            "CREATE INDEX IF NOT EXISTS idx_industry_src ON industry_classify(src)",
            "CREATE INDEX IF NOT EXISTS idx_concept_src ON concept_classify(src)",
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
            
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
        
    def execute_query(self, query, params=None):
        """执行查询"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        results = cursor.fetchall()
        conn.close()
        return results
        
    def execute_insert(self, table_name, data_df, mode='append'):
        """批量插入数据"""
        conn = self.get_connection()
        
        # 添加更新时间
        data_df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 插入数据
        data_df.to_sql(table_name, conn, if_exists=mode, index=False)
        
        conn.close()
        return len(data_df)
        
    def clear_table_data(self, table_name, condition=None):
        """清空表数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if condition:
            cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        else:
            cursor.execute(f"DELETE FROM {table_name}")
            
        conn.commit()
        conn.close()