#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare API接口测试脚本
"""

import tudata as ts
import pandas as pd
import time
from datetime import datetime, timedelta
import json

# 设置token
TOKEN = "7e4d915cb5b54b2abf1ad77eaf29bbf1"
ts.set_token(TOKEN)
pro = ts.pro_api()

def test_api(api_name, api_func, params, category, subcategory):
    """测试单个API接口"""
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
                'sample_data': df.head(2).to_dict('records') if len(df) > 0 else [],
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
            'sample_data': [],
            'error': str(e)
        }

def run_api_tests():
    """运行所有API测试"""
    
    # 获取测试日期
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    
    # API测试配置
    api_tests = [
        # 多只股票多日查询
        ('股票列表', lambda: pro.stock_basic(exchange='', list_status='L'), '多只股票多日查询', '基础数据'),
        ('交易日历', lambda: pro.trade_cal(exchange='SSE', start_date=start_date, end_date=end_date), '多只股票多日查询', '基础数据'),
        ('A股日线行情', lambda: pro.daily(trade_date='20241201'), '多只股票多日查询', '行情数据'),
        ('指数日线行情', lambda: pro.index_daily(trade_date='20241201'), '多只股票多日查询', '行情数据'),
        
        # 单只股票多日查询
        ('利润表', lambda: pro.income(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), '单只股票多日查询', '财务数据'),
        ('资产负债表', lambda: pro.balancesheet(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), '单只股票多日查询', '财务数据'),
        ('复权因子', lambda: pro.adj_factor(ts_code='000001.SZ', start_date=start_date, end_date=end_date), '单只股票多日查询', '行情数据'),
        
        # 单只股票逐条获取
        ('每日涨跌停统计', lambda: pro.limit_list(trade_date='20241201'), '单只股票逐条获取', '行情数据'),
        ('融资融券交易汇总', lambda: pro.margin(trade_date='20241201'), '单只股票逐条获取', '两融转融通'),
    ]
    
    results = []
    total_tests = len(api_tests)
    
    print(f"开始测试 {total_tests} 个API接口...")
    
    for i, (api_name, api_func, category, subcategory) in enumerate(api_tests, 1):
        print(f"测试 {i}/{total_tests}: {api_name}")
        
        result = test_api(api_name, api_func, {}, category, subcategory)
        results.append(result)
        
        # 避免请求过快
        time.sleep(0.5)
    
    return results

def generate_report(results):
    """生成测试报告"""
    
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
    report = f"""# Tushare API接口测试报告

## 📊 测试概览

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Token状态**: 已配置  
**测试接口数**: {total_tests}个

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
"""
        
        if result['error']:
            report += f"**错误信息**: {result['error']}  \n"
        
        if result['sample_data']:
            report += f"**示例数据**: 前2行数据已获取  \n"
        
        report += "\n"
    
    report += f"""## 🔍 测试结论

### 数据获取能力
- **批量获取**: {'✅ 支持' if success_tests > 0 else '❌ 不支持'}
- **Token有效性**: {'✅ 有效' if success_tests > 0 else '❌ 无效'}
- **接口稳定性**: {success_tests/total_tests*100:.1f}%

### 建议
"""
    
    if success_tests > total_tests * 0.8:
        report += "- ✅ Token工作正常，可以进行后续开发\n"
    elif success_tests > total_tests * 0.5:
        report += "- ⚠️ 部分接口可用，建议检查积分或权限\n"
    else:
        report += "- ❌ 大部分接口不可用，建议检查Token配置\n"
    
    if error_tests > 0:
        report += "- 🔧 建议检查失败接口的参数配置\n"
    
    report += f"""
---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report

def main():
    """主函数"""
    print("Tushare API接口测试开始...")
    
    # 运行测试
    results = run_api_tests()
    
    # 生成报告
    report = generate_report(results)
    
    # 保存报告
    with open('D:\\stock_system\\API测试报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存详细结果
    with open('D:\\stock_system\\api_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("测试完成!")
    print("报告已保存: API测试报告.md")
    print("详细结果: api_test_results.json")

if __name__ == "__main__":
    main()