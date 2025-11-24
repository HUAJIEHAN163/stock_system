#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试index_dailybasic API数据类型问题
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
            print("❌ Token配置文件不存在")
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
        print(f"❌ 加载token配置失败: {e}")
        return None

def test_index_dailybasic_api():
    """测试index_dailybasic API并分析数据"""
    print("🔍 开始测试index_dailybasic API...")
    
    # 1. 加载配置
    token_config = load_token_config()
    if not token_config:
        return
    
    # 2. 初始化API
    try:
        if token_config.get('token_type') == 'tudata':
            import tudata as ts
            print("📊 使用tudata库")
        else:
            import tushare as ts
            print("📊 使用tushare库")
            
        ts.set_token(token_config['token'])
        pro = ts.pro_api()
        print("✅ API连接成功")
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        return
    
    # 3. 调用API获取数据
    try:
        # 使用与初始化相同的参数
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y%m%d')
        
        print(f"📅 查询时间范围: {start_date} 到 {end_date}")
        
        df = pro.index_dailybasic(
            ts_code='000001.SH,399001.SZ',
            start_date=start_date,
            end_date=end_date,
            fields='ts_code,trade_date,total_mv,float_mv,total_share,float_share,free_share,turnover_rate,turnover_rate_f,pe,pe_ttm,pb'
        )
        
        print(f"✅ API调用成功，获取 {len(df)} 条记录")
        
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        return
    
    # 4. 分析数据结构
    print("\n📊 数据结构分析:")
    print(f"DataFrame形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print(f"数据类型:\n{df.dtypes}")
    
    # 5. 检查问题数据
    print("\n🔍 检查问题数据:")
    
    # 检查每列的特殊值
    for col in df.columns:
        print(f"\n列 '{col}':")
        print(f"  数据类型: {df[col].dtype}")
        print(f"  空值数量: {df[col].isnull().sum()}")
        
        if df[col].dtype in ['float64', 'int64']:
            # 检查数值列的特殊值
            inf_count = (df[col] == float('inf')).sum()
            neg_inf_count = (df[col] == float('-inf')).sum()
            
            if inf_count > 0:
                print(f"  ⚠️  包含 {inf_count} 个正无穷大值")
            if neg_inf_count > 0:
                print(f"  ⚠️  包含 {neg_inf_count} 个负无穷大值")
                
            # 显示统计信息
            try:
                print(f"  数值范围: {df[col].min():.2f} 到 {df[col].max():.2f}")
            except:
                print(f"  ⚠️  数值范围计算失败（可能包含特殊值）")
                
        elif df[col].dtype == 'object':
            # 检查字符串列的特殊值
            unique_vals = df[col].unique()[:10]  # 显示前10个唯一值
            print(f"  唯一值示例: {unique_vals}")
    
    # 6. 显示前几行数据
    print(f"\n📋 前5行数据:")
    print(df.head())
    
    # 7. 尝试数据库插入测试
    print(f"\n🗄️  测试数据库插入:")
    
    try:
        # 创建临时数据库连接
        conn = sqlite3.connect(':memory:')
        
        # 创建测试表
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE test_index_dailybasic (
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
        
        # 添加update_time列
        df_test = df.copy()
        df_test['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 尝试插入原始数据
        print("  测试原始数据插入...")
        df_test.to_sql('test_index_dailybasic', conn, if_exists='replace', index=False)
        print("  ✅ 原始数据插入成功")
        
        conn.close()
        
    except Exception as e:
        print(f"  ❌ 原始数据插入失败: {e}")
        
        # 尝试数据清理后插入
        try:
            print("  🔧 尝试数据清理后插入...")
            
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE test_index_dailybasic (
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
            
            df_clean = df.copy()
            df_clean['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 清理数据
            numeric_cols = ['total_mv', 'float_mv', 'total_share', 'float_share', 'free_share', 
                           'turnover_rate', 'turnover_rate_f', 'pe', 'pe_ttm', 'pb']
            
            for col in numeric_cols:
                if col in df_clean.columns:
                    # 转换为数值类型
                    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    # 替换无穷大值
                    df_clean[col] = df_clean[col].replace([float('inf'), float('-inf')], None)
            
            # 处理字符串列
            for col in df_clean.columns:
                if df_clean[col].dtype == 'object':
                    df_clean[col] = df_clean[col].astype(str).replace(['nan', 'None'], None)
            
            df_clean.to_sql('test_index_dailybasic', conn, if_exists='replace', index=False)
            print("  ✅ 清理后数据插入成功")
            
            conn.close()
            
        except Exception as clean_error:
            print(f"  ❌ 清理后数据插入仍失败: {clean_error}")
    
    # 8. 生成诊断报告
    print(f"\n📋 诊断报告:")
    print(f"- 数据获取: ✅ 成功")
    print(f"- 数据量: {len(df)} 条记录")
    print(f"- 列数: {len(df.columns)} 列")
    
    # 检查是否有问题数据
    has_inf = False
    has_object_issues = False
    
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            if (df[col] == float('inf')).any() or (df[col] == float('-inf')).any():
                has_inf = True
        elif df[col].dtype == 'object':
            if df[col].isnull().any():
                has_object_issues = True
    
    if has_inf:
        print(f"- ⚠️  发现无穷大值，需要数据清理")
    if has_object_issues:
        print(f"- ⚠️  发现字符串列空值问题")
    
    if not has_inf and not has_object_issues:
        print(f"- ✅ 数据质量良好，无明显问题")

if __name__ == "__main__":
    test_index_dailybasic_api()