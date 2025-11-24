#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多只股票多日查询API测试脚本
测试日期: 2025年11月24日, 2025年11月21日, 2024年11月20日
"""

import tushare as ts
import pandas as pd
import time
from datetime import datetime
import json

# 设置token
with open('doc/数据调查/token.txt', 'r', encoding='utf-8') as f:
    token = f.read().strip()
ts.set_token(token)
pro = ts.pro_api()

# 测试日期
TEST_DATES = ['20251124', '20251121', '20241120']
TEST_DATE_RANGE = {'start_date': '20241120', 'end_date': '20251124'}

def test_api(api_name, api_func, params, description):
    """测试单个API接口"""
    print(f"\n{'='*60}")
    print(f"测试API: {api_name}")
    print(f"描述: {description}")
    print(f"参数: {params}")
    
    try:
        start_time = time.time()
        df = api_func(**params)
        end_time = time.time()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功 - 数据量: {len(df)}行, 耗时: {end_time-start_time:.2f}秒")
            print(f"列名: {list(df.columns)}")
            print(f"前3行数据:")
            print(df.head(3).to_string())
            return {
                'status': 'SUCCESS',
                'rows': len(df),
                'columns': list(df.columns),
                'time': round(end_time-start_time, 2),
                'sample_data': df.head(3).to_dict()
            }
        else:
            print(f"⚠️ 无数据")
            return {
                'status': 'NO_DATA',
                'rows': 0,
                'columns': [],
                'time': round(end_time-start_time, 2),
                'sample_data': {}
            }
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return {
            'status': 'ERROR',
            'error': str(e),
            'rows': 0,
            'columns': [],
            'time': 0,
            'sample_data': {}
        }

def main():
    """主测试函数"""
    print("开始测试多只股票多日查询API接口")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 基础数据测试
    print("\n" + "="*80)
    print("📊 基础数据API测试")
    print("="*80)
    
    # 1. 股票列表
    results['stock_basic'] = test_api(
        'stock_basic', 
        pro.stock_basic,
        {'exchange': '', 'list_status': 'L'},
        '获取基础信息数据，包括股票代码、名称、上市日期等'
    )
    
    # 2. 上市公司基本信息
    results['stock_company'] = test_api(
        'stock_company',
        pro.stock_company,
        {'exchange': 'SSE'},
        '获取上市公司基本信息'
    )
    
    # 3. 交易日历
    results['trade_cal'] = test_api(
        'trade_cal',
        pro.trade_cal,
        {'exchange': 'SSE', 'start_date': TEST_DATE_RANGE['start_date'], 'end_date': TEST_DATE_RANGE['end_date']},
        '获取各大交易所交易日历数据'
    )
    
    # 4. IPO新股列表
    results['new_share'] = test_api(
        'new_share',
        pro.new_share,
        {'start_date': TEST_DATE_RANGE['start_date'], 'end_date': TEST_DATE_RANGE['end_date']},
        '获取新股上市列表数据'
    )
    
    # 行情数据测试
    print("\n" + "="*80)
    print("📈 行情数据API测试")
    print("="*80)
    
    # 5. A股日线行情 - 测试单日全市场
    results['daily_single_date'] = test_api(
        'daily (单日全市场)',
        pro.daily,
        {'trade_date': '20251121'},
        'A股日线行情 - 单日全市场数据'
    )
    
    # 6. A股日线行情 - 测试多股票多日
    results['daily_multi_stock'] = test_api(
        'daily (多股票多日)',
        pro.daily,
        {'ts_code': '000001.SZ,600000.SH,000002.SZ', 'start_date': TEST_DATE_RANGE['start_date'], 'end_date': TEST_DATE_RANGE['end_date']},
        'A股日线行情 - 多股票多日数据'
    )
    
    # 7. 周线行情
    results['weekly'] = test_api(
        'weekly',
        pro.weekly,
        {'ts_code': '000001.SZ,600000.SH', 'start_date': '20241101', 'end_date': '20251124'},
        '获取A股周线行情'
    )
    
    # 8. 月线行情
    results['monthly'] = test_api(
        'monthly',
        pro.monthly,
        {'ts_code': '000001.SZ,600000.SH', 'start_date': '20240101', 'end_date': '20251124'},
        '获取A股月线行情'
    )
    
    # 9. 复权因子
    results['adj_factor'] = test_api(
        'adj_factor',
        pro.adj_factor,
        {'ts_code': '000001.SZ,600000.SH', 'start_date': TEST_DATE_RANGE['start_date'], 'end_date': TEST_DATE_RANGE['end_date']},
        '获取股票复权因子'
    )
    
    # 10. 大盘指数每日指标
    results['index_dailybasic'] = test_api(
        'index_dailybasic',
        pro.index_dailybasic,
        {'ts_code': '000001.SH,399001.SZ', 'start_date': TEST_DATE_RANGE['start_date'], 'end_date': TEST_DATE_RANGE['end_date']},
        '获取大盘指数每日指标'
    )
    
    # 分钟行情测试
    print("\n" + "="*80)
    print("⏰ 分钟行情API测试")
    print("="*80)
    
    # 11. 股票历史分钟行情
    results['stk_mins'] = test_api(
        'stk_mins',
        pro.stk_mins,
        {'ts_code': '000001.SZ', 'freq': '60min', 'start_date': '2024-11-20 09:00:00', 'end_date': '2024-11-21 15:00:00'},
        '获取A股分钟数据'
    )
    
    # 保存测试结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f'multi_stock_api_test_results_{timestamp}.json'
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # 生成测试报告
    print("\n" + "="*80)
    print("📋 测试结果汇总")
    print("="*80)
    
    success_count = 0
    error_count = 0
    no_data_count = 0
    total_rows = 0
    
    for api_name, result in results.items():
        status = result['status']
        rows = result.get('rows', 0)
        
        if status == 'SUCCESS':
            success_count += 1
            total_rows += rows
            print(f"✅ {api_name}: 成功 ({rows}行)")
        elif status == 'ERROR':
            error_count += 1
            print(f"❌ {api_name}: 错误 - {result.get('error', 'Unknown error')}")
        elif status == 'NO_DATA':
            no_data_count += 1
            print(f"⚠️ {api_name}: 无数据")
    
    print(f"\n📊 统计结果:")
    print(f"总接口数: {len(results)}")
    print(f"成功: {success_count}")
    print(f"错误: {error_count}")
    print(f"无数据: {no_data_count}")
    print(f"总数据量: {total_rows:,}行")
    print(f"结果已保存到: {result_file}")

if __name__ == "__main__":
    main()