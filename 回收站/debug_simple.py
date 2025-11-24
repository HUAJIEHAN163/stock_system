#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版调试脚本 - 测试index_dailybasic API数据类型问题
"""

import os
import sys
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# 添加src路径
sys.path.append('src')

def load_token_config():
    """加载token配置"""
    try:
        config_file = "config/token_config.txt"
        if not os.path.exists(config_file):
            print("Token配置文件不存在")
            return None
            
        config = {}
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except Exception as e:
        print(f"加载token配置失败: {e}")
        return None

def test_api():
    """测试API"""
    print("开始测试index_dailybasic API...")
    
    # 加载配置
    token_config = load_token_config()
    if not token_config:
        return
    
    # 初始化API
    try:
        if token_config.get('token_type') == 'tudata':
            import tudata as ts
            print("使用tudata库")
        else:
            import tushare as ts
            print("使用tushare库")
            
        ts.set_token(token_config['token'])
        pro = ts.pro_api()
        print("API连接成功")
    except Exception as e:
        print(f"API连接失败: {e}")
        return
    
    # 调用API
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y%m%d')
        
        print(f"查询时间范围: {start_date} 到 {end_date}")
        
        df = pro.index_dailybasic(
            ts_code='000001.SH,399001.SZ',
            start_date=start_date,
            end_date=end_date,
            fields='ts_code,trade_date,total_mv,float_mv,total_share,float_share,free_share,turnover_rate,turnover_rate_f,pe,pe_ttm,pb'
        )
        
        print(f"API调用成功，获取 {len(df)} 条记录")
        
    except Exception as e:
        print(f"API调用失败: {e}")
        return
    
    # 分析数据
    print(f"\n数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print(f"数据类型:\n{df.dtypes}")
    
    # 检查特殊值
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            inf_count = (df[col] == float('inf')).sum()
            neg_inf_count = (df[col] == float('-inf')).sum()
            
            if inf_count > 0:
                print(f"列 {col}: 包含 {inf_count} 个正无穷大值")
            if neg_inf_count > 0:
                print(f"列 {col}: 包含 {neg_inf_count} 个负无穷大值")
    
    # 显示前几行
    print(f"\n前3行数据:")
    print(df.head(3))
    
    # 测试数据库插入
    print(f"\n测试数据库插入:")
    
    try:
        conn = sqlite3.connect(':memory:')
        df_test = df.copy()
        df_test['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_test.to_sql('test_table', conn, if_exists='replace', index=False)
        print("原始数据插入成功")
        conn.close()
        
    except Exception as e:
        print(f"原始数据插入失败: {e}")
        
        # 尝试数据清理
        try:
            conn = sqlite3.connect(':memory:')
            df_clean = df.copy()
            df_clean['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 清理数值列
            numeric_cols = ['total_mv', 'float_mv', 'total_share', 'float_share', 'free_share', 
                           'turnover_rate', 'turnover_rate_f', 'pe', 'pe_ttm', 'pb']
            
            for col in numeric_cols:
                if col in df_clean.columns:
                    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    df_clean[col] = df_clean[col].replace([float('inf'), float('-inf')], None)
            
            df_clean.to_sql('test_table', conn, if_exists='replace', index=False)
            print("清理后数据插入成功")
            conn.close()
            
        except Exception as clean_error:
            print(f"清理后数据插入仍失败: {clean_error}")

if __name__ == "__main__":
    test_api()