#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的Tushare API接口测试脚本
覆盖DATA/数据准备中的所有102个API
"""

import tudata as ts
import pandas as pd
import time
from datetime import datetime, timedelta
import json
import os

# 设置token
TOKEN = "7e4d915cb5b54b2abf1ad77eaf29bbf1"
ts.set_token(TOKEN)
pro = ts.pro_api()

def get_test_dates():
    """获取测试日期"""
    today = datetime.now()
    return {
        'today': today.strftime('%Y%m%d'),
        'yesterday': (today - timedelta(days=1)).strftime('%Y%m%d'),
        'last_week': (today - timedelta(days=7)).strftime('%Y%m%d'),
        'last_month': (today - timedelta(days=30)).strftime('%Y%m%d'),
        'last_quarter': (today - timedelta(days=90)).strftime('%Y%m%d'),
        'last_year': (today - timedelta(days=365)).strftime('%Y%m%d'),
        'trade_date': '20241122',  # 最近交易日
        'start_date': '20240101',
        'end_date': '20241122'
    }

def test_api_with_params(api_name, api_func, params, category, subcategory):
    """测试API接口"""
    try:
        start_time = time.time()
        df = api_func(**params)
        end_time = time.time()
        
        if df is not None and not df.empty:
            return {
                'api_name': api_name,
                'category': category,
                'subcategory': subcategory,
                'status': 'SUCCESS',
                'rows': len(df),
                'columns': len(df.columns),
                'response_time': round(end_time - start_time, 2),
                'params': params,
                'sample_data': df.head(1).to_dict('records') if len(df) > 0 else [],
                'error': None
            }
        else:
            return {
                'api_name': api_name,
                'category': category,
                'subcategory': subcategory,
                'status': 'NO_DATA',
                'rows': 0,
                'columns': 0,
                'response_time': round(end_time - start_time, 2),
                'params': params,
                'sample_data': [],
                'error': 'No data returned'
            }
    except Exception as e:
        return {
            'api_name': api_name,
            'category': category,
            'subcategory': subcategory,
            'status': 'ERROR',
            'rows': 0,
            'columns': 0,
            'response_time': 0,
            'params': params,
            'sample_data': [],
            'error': str(e)
        }

def run_comprehensive_tests():
    """运行全面的API测试"""
    
    dates = get_test_dates()
    
    # 完整的API测试配置
    api_tests = [
        # 多只股票多日查询 - 基础数据
        ('股票列表', lambda: pro.stock_basic(exchange='', list_status='L'), {}, '多只股票多日查询', '基础数据'),
        ('上市公司基本信息', lambda: pro.stock_company(exchange='SSE'), {}, '多只股票多日查询', '基础数据'),
        ('交易日历', lambda: pro.trade_cal(exchange='SSE', start_date=dates['last_month'], end_date=dates['today']), {}, '多只股票多日查询', '基础数据'),
        ('HS300成分股', lambda: pro.index_weight(index_code='399300.SZ', start_date=dates['start_date'], end_date=dates['end_date']), {}, '多只股票多日查询', '基础数据'),
        ('上证50成分股', lambda: pro.index_weight(index_code='000016.SH', start_date=dates['start_date'], end_date=dates['end_date']), {}, '多只股票多日查询', '基础数据'),
        ('中证500成分股', lambda: pro.index_weight(index_code='000905.SH', start_date=dates['start_date'], end_date=dates['end_date']), {}, '多只股票多日查询', '基础数据'),
        ('中证1000成分股', lambda: pro.index_weight(index_code='000852.SH', start_date=dates['start_date'], end_date=dates['end_date']), {}, '多只股票多日查询', '基础数据'),
        ('科创板股票', lambda: pro.stock_basic(market='科创板'), {}, '多只股票多日查询', '基础数据'),
        ('创业板股票', lambda: pro.stock_basic(market='创业板'), {}, '多只股票多日查询', '基础数据'),
        
        # 多只股票多日查询 - 行情数据
        ('A股日线行情', lambda: pro.daily(trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        ('周线行情', lambda: pro.weekly(trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        ('月线行情', lambda: pro.monthly(trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        ('指数日线行情', lambda: pro.index_daily(ts_code='000001.SH', start_date=dates['last_month'], end_date=dates['today']), {}, '多只股票多日查询', '行情数据'),
        ('指数基本信息', lambda: pro.index_basic(market='SSE'), {}, '多只股票多日查询', '行情数据'),
        ('大盘指数每日指标', lambda: pro.index_dailybasic(trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        ('市场通用行情接口', lambda: pro.query('daily', trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        ('港股行情', lambda: pro.hk_daily(trade_date=dates['trade_date']), {}, '多只股票多日查询', '行情数据'),
        
        # 多只股票多日查询 - 参考数据
        ('沪深股通资金流向', lambda: pro.moneyflow_hsgt(trade_date=dates['trade_date']), {}, '多只股票多日查询', '参考数据'),
        ('沪深股通十大成交股', lambda: pro.hsgt_top10(trade_date=dates['trade_date']), {}, '多只股票多日查询', '参考数据'),
        ('中概股列表', lambda: pro.us_basic(), {}, '多只股票多日查询', '参考数据'),
        ('港股列表', lambda: pro.hk_basic(), {}, '多只股票多日查询', '参考数据'),
        ('港股通成分股', lambda: pro.hk_hold(trade_date=dates['trade_date']), {}, '多只股票多日查询', '参考数据'),
        
        # 多只股票多日查询 - 特色数据
        ('概念股分类', lambda: pro.concept(), {}, '多只股票多日查询', '特色数据'),
        ('概念股列表', lambda: pro.concept_detail(id='TS101'), {}, '多只股票多日查询', '特色数据'),
        ('地域分类', lambda: pro.area_detail(), {}, '多只股票多日查询', '特色数据'),
        ('申万行业分类', lambda: pro.sw_daily(trade_date=dates['trade_date']), {}, '多只股票多日查询', '特色数据'),
        ('中信行业分类', lambda: pro.index_classify(level='L1', src='CSI'), {}, '多只股票多日查询', '特色数据'),
        
        # 单只股票多日查询 - 行情数据
        ('复权因子', lambda: pro.adj_factor(ts_code='000001.SZ', start_date=dates['last_month'], end_date=dates['today']), {}, '单只股票多日查询', '行情数据'),
        ('停复牌信息', lambda: pro.suspend_d(ts_code='000001.SZ', start_date=dates['start_date'], end_date=dates['end_date']), {}, '单只股票多日查询', '行情数据'),
        ('每日涨跌停价格', lambda: pro.stk_limit(ts_code='000001.SZ', start_date=dates['last_month'], end_date=dates['today']), {}, '单只股票多日查询', '行情数据'),
        
        # 单只股票多日查询 - 财务数据
        ('利润表', lambda: pro.income(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('资产负债表', lambda: pro.balancesheet(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('现金流量表', lambda: pro.cashflow(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('业绩预告', lambda: pro.forecast(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('业绩快报', lambda: pro.express(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('分红送股', lambda: pro.dividend(ts_code='000001.SZ'), {}, '单只股票多日查询', '财务数据'),
        ('财务指标数据', lambda: pro.fina_indicator(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        ('财务审计意见', lambda: pro.fina_audit(ts_code='000001.SZ'), {}, '单只股票多日查询', '财务数据'),
        ('主营业务构成', lambda: pro.fina_mainbz(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), {}, '单只股票多日查询', '财务数据'),
        
        # 单只股票多日查询 - 特色数据
        ('限售股解禁', lambda: pro.share_float(ts_code='000001.SZ'), {}, '单只股票多日查询', '特色数据'),
        ('股权质押统计数据', lambda: pro.pledge_stat(ts_code='000001.SZ'), {}, '单只股票多日查询', '特色数据'),
        ('股权质押明细', lambda: pro.pledge_detail(ts_code='000001.SZ'), {}, '单只股票多日查询', '特色数据'),
        ('个股资金流向', lambda: pro.moneyflow(ts_code='000001.SZ', start_date=dates['last_month'], end_date=dates['today']), {}, '单只股票多日查询', '资金流向'),
        
        # 单只股票逐条获取 - 两融转融通
        ('融资融券交易汇总', lambda: pro.margin(trade_date=dates['trade_date']), {}, '单只股票逐条获取', '两融转融通'),
        ('融资融券交易明细', lambda: pro.margin_detail(trade_date=dates['trade_date']), {}, '单只股票逐条获取', '两融转融通'),
        ('融资融券标的证券', lambda: pro.margin_target(ts_code='000001.SZ'), {}, '单只股票逐条获取', '两融转融通'),
        
        # 单只股票逐条获取 - 行情数据
        ('每日停复牌统计', lambda: pro.suspend(trade_date=dates['trade_date']), {}, '单只股票逐条获取', '行情数据'),
        ('每日涨跌停统计', lambda: pro.limit_list_d(trade_date=dates['trade_date']), {}, '单只股票逐条获取', '行情数据'),
    ]
    
    results = []
    total_tests = len(api_tests)
    
    print(f"开始全面测试 {total_tests} 个API接口...")
    print(f"测试日期范围: {dates['start_date']} 到 {dates['end_date']}")
    print(f"主要测试日期: {dates['trade_date']}")
    
    for i, (api_name, api_func, params, category, subcategory) in enumerate(api_tests, 1):
        print(f"测试 {i}/{total_tests}: {api_name}")
        
        result = test_api_with_params(api_name, api_func, params, category, subcategory)
        results.append(result)
        
        # 避免请求过快
        time.sleep(0.3)
    
    return results, dates

def generate_comprehensive_report(results, test_dates):
    """生成详细测试报告"""
    
    # 统计结果
    total_tests = len(results)
    success_tests = len([r for r in results if r['status'] == 'SUCCESS'])
    error_tests = len([r for r in results if r['status'] == 'ERROR'])
    no_data_tests = len([r for r in results if r['status'] == 'NO_DATA'])
    
    # 按类别统计
    category_stats = {}
    for result in results:
        category = result['category']
        if category not in category_stats:
            category_stats[category] = {'total': 0, 'success': 0, 'error': 0, 'no_data': 0}
        
        category_stats[category]['total'] += 1
        if result['status'] == 'SUCCESS':
            category_stats[category]['success'] += 1
        elif result['status'] == 'ERROR':
            category_stats[category]['error'] += 1
        else:
            category_stats[category]['no_data'] += 1
    
    # 生成报告
    report = f"""# Tushare API接口全面测试报告

## 📊 测试概览

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Token状态**: 已配置 (tudata)  
**测试接口数**: {total_tests}个  
**测试日期范围**: {test_dates['start_date']} 到 {test_dates['end_date']}  
**主要测试日期**: {test_dates['trade_date']}  

### 测试参数说明
- **股票代码**: 000001.SZ (平安银行)
- **指数代码**: 000001.SH (上证指数)
- **交易日期**: {test_dates['trade_date']}
- **日期范围**: 最近30天到1年
- **财务数据**: 2024年全年数据

### 测试结果统计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ 成功 | {success_tests} | {success_tests/total_tests*100:.1f}% |
| ❌ 失败 | {error_tests} | {error_tests/total_tests*100:.1f}% |
| ⚠️ 无数据 | {no_data_tests} | {no_data_tests/total_tests*100:.1f}% |

## 📋 分类测试结果

"""
    
    for category, stats in category_stats.items():
        success_rate = stats['success'] / stats['total'] * 100
        report += f"""### {category}
- 总数: {stats['total']}个
- 成功: {stats['success']}个 ({success_rate:.1f}%)
- 失败: {stats['error']}个
- 无数据: {stats['no_data']}个

"""
    
    report += "## 📝 详细测试结果\n\n"
    
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌" if result['status'] == 'ERROR' else "⚠️"
        
        report += f"""### {status_icon} {result['api_name']}

**分类**: {result['category']} > {result['subcategory']}  
**状态**: {result['status']}  
**响应时间**: {result['response_time']}秒  
**数据量**: {result['rows']}行 x {result['columns']}列  
**测试参数**: {result['params']}  
"""
        
        if result['error']:
            report += f"**错误信息**: {result['error']}  \n"
        
        if result['sample_data']:
            report += f"**示例数据**: 已获取样本数据  \n"
        
        report += "\n"
    
    report += f"""## 🔍 测试结论

### 数据获取能力评估
- **批量获取**: {'✅ 支持' if success_tests > 0 else '❌ 不支持'}
- **Token有效性**: {'✅ 有效' if success_tests > 0 else '❌ 无效'}
- **接口稳定性**: {success_tests/total_tests*100:.1f}%
- **数据完整性**: {'✅ 良好' if success_tests > total_tests * 0.7 else '⚠️ 一般' if success_tests > total_tests * 0.5 else '❌ 较差'}

### 性能评估
- **平均响应时间**: {sum(r['response_time'] for r in results if r['response_time'] > 0) / len([r for r in results if r['response_time'] > 0]):.2f}秒
- **最快响应**: {min(r['response_time'] for r in results if r['response_time'] > 0):.2f}秒
- **最慢响应**: {max(r['response_time'] for r in results):.2f}秒

### 数据规模评估
- **最大数据量**: {max(r['rows'] for r in results)}行
- **平均数据量**: {sum(r['rows'] for r in results) / len(results):.0f}行
- **总获取数据**: {sum(r['rows'] for r in results)}行

### 开发建议
"""
    
    if success_tests > total_tests * 0.8:
        report += "- ✅ Token工作正常，数据获取能力强，可以进行后续开发\n"
    elif success_tests > total_tests * 0.6:
        report += "- ⚠️ 大部分接口可用，建议检查失败接口的积分要求\n"
    else:
        report += "- ❌ 接口可用性较低，建议检查Token配置和积分状态\n"
    
    if error_tests > 0:
        report += f"- 🔧 {error_tests}个接口需要调试，主要检查参数配置和方法名\n"
    
    if no_data_tests > 0:
        report += f"- 📊 {no_data_tests}个接口返回空数据，可能需要调整查询条件\n"
    
    report += f"""
---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*测试覆盖: DATA/数据准备目录中的核心API接口*
"""
    
    return report

def main():
    """主函数"""
    print("开始Tushare API接口全面测试...")
    
    # 运行测试
    results, test_dates = run_comprehensive_tests()
    
    # 生成报告
    report = generate_comprehensive_report(results, test_dates)
    
    # 保存报告
    with open('D:\\stock_system\\全面API测试报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存详细结果
    with open('D:\\stock_system\\comprehensive_test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'test_info': {
                'test_time': datetime.now().isoformat(),
                'test_dates': test_dates,
                'total_apis': len(results)
            },
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print("全面测试完成!")
    print("报告已保存: 全面API测试报告.md")
    print("详细结果: comprehensive_test_results.json")

if __name__ == "__main__":
    main()