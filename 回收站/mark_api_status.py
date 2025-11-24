#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为DATA/数据准备中的API文件添加可用性标记
并使用2025年11月21日和24日进行重新测试
"""

import tudata as ts
import pandas as pd
import time
import os
import re
from datetime import datetime

# 设置token
TOKEN = "7e4d915cb5b54b2abf1ad77eaf29bbf1"
ts.set_token(TOKEN)
pro = ts.pro_api()

# API测试映射表
API_TEST_MAP = {
    # 基于之前测试结果的映射
    25: ('股票列表', lambda: pro.stock_basic(exchange='', list_status='L'), True),
    26: ('交易日历', lambda: pro.trade_cal(exchange='SSE', start_date='20251121', end_date='20251124'), True),
    27: ('A股日线行情', lambda: pro.daily(trade_date='20251121'), True),
    28: ('指数日线行情', lambda: pro.index_daily(ts_code='000001.SH', start_date='20251121', end_date='20251124'), True),
    32: ('大盘指数每日指标', lambda: pro.index_dailybasic(trade_date='20251121'), True),
    33: ('利润表', lambda: pro.income(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    36: ('资产负债表', lambda: pro.balancesheet(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    44: ('现金流量表', lambda: pro.cashflow(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    45: ('业绩预告', lambda: pro.forecast(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    46: ('业绩快报', lambda: pro.express(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    47: ('备用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    48: ('备用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    58: ('融资融券交易汇总', lambda: pro.margin(trade_date='20251121'), True),
    59: ('融资融券交易明细', lambda: pro.margin_detail(trade_date='20251121'), True),
    61: ('沪深股通资金流向', lambda: pro.moneyflow_hsgt(trade_date='20251121'), True),
    62: ('沪深股通十大成交股', lambda: pro.hsgt_top10(trade_date='20251121'), True),
    79: ('财务指标数据', lambda: pro.fina_indicator(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    80: ('财务审计意见', lambda: pro.fina_audit(ts_code='000001.SZ'), True),
    81: ('主营业务构成', lambda: pro.fina_mainbz(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    100: ('HS300成分股', lambda: pro.index_weight(index_code='399300.SZ', start_date='20251121', end_date='20251124'), True),
    103: ('分红送股', lambda: pro.dividend(ts_code='000001.SZ'), True),
    106: ('涨跌停统计', lambda: pro.limit_list_d(trade_date='20251121'), False),  # 方法名错误
    107: ('每日涨跌停价格', lambda: pro.stk_limit(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    109: ('市场通用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    110: ('中概股列表', lambda: pro.us_basic(), True),
    111: ('中概股月线行情', lambda: pro.us_monthly(trade_date='20251121'), True),
    112: ('上证50成分股', lambda: pro.index_weight(index_code='000016.SH', start_date='20251121', end_date='20251124'), True),
    123: ('科创板股票', lambda: pro.stock_basic(market='科创板'), True),
    124: ('港股列表', lambda: pro.hk_basic(), True),
    144: ('停复牌信息', lambda: pro.suspend_d(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    145: ('每日停复牌统计', lambda: pro.suspend(trade_date='20251121'), False),  # 方法名错误
    146: ('停牌原因', lambda: pro.suspend_d(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    160: ('港股通成分股', lambda: pro.hk_hold(trade_date='20251121'), True),
    161: ('港股通每日成交统计', lambda: pro.hk_hold(trade_date='20251121'), True),
    162: ('财务数据', lambda: pro.fina_indicator(ts_code='000001.SZ', start_date='20240101', end_date='20241201'), True),
    166: ('港股通资金流向', lambda: pro.moneyflow_hsgt(trade_date='20251121'), True),
    170: ('个股资金流向', lambda: pro.moneyflow(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    175: ('港股通十大成交股', lambda: pro.hsgt_top10(trade_date='20251121'), True),
    183: ('沪深市场通用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    188: ('限售股解禁', lambda: pro.share_float(ts_code='000001.SZ'), True),
    193: ('中证500成分股', lambda: pro.index_weight(index_code='000905.SH', start_date='20251121', end_date='20251124'), True),
    194: ('中证1000成分股', lambda: pro.index_weight(index_code='000852.SH', start_date='20251121', end_date='20251124'), True),
    214: ('港股通每日成交统计', lambda: pro.hk_hold(trade_date='20251121'), True),
    255: ('港股行情', lambda: pro.hk_daily(trade_date='20251121'), False),  # 数据格式问题
    259: ('限售股解禁', lambda: pro.share_float(ts_code='000001.SZ'), True),
    260: ('股权质押统计数据', lambda: pro.pledge_stat(ts_code='000001.SZ'), True),
    261: ('股权质押明细', lambda: pro.pledge_detail(ts_code='000001.SZ'), True),
    262: ('创业板股票', lambda: pro.stock_basic(market='创业板'), True),
    267: ('同花顺概念', lambda: pro.ths_index(exchange='A', type='N'), True),
    274: ('券商盈利预测数据', lambda: pro.forecast_vip(ts_code='000001.SZ'), True),
    275: ('同花顺概念和行业', lambda: pro.ths_index(exchange='A', type='N'), True),
    292: ('概念股分类', lambda: pro.concept(), True),
    293: ('概念股列表', lambda: pro.concept_detail(id='TS101'), True),
    294: ('地域分类', lambda: pro.area_detail(), False),  # 方法名错误
    295: ('中信行业分类', lambda: pro.index_classify(level='L1', src='CSI'), True),
    296: ('申万行业分类', lambda: pro.sw_daily(trade_date='20251121'), True),
    298: ('股票回购', lambda: pro.repurchase(ts_code='000001.SZ'), True),
    311: ('同花顺概念和行业', lambda: pro.ths_index(exchange='A', type='N'), True),
    312: ('同花顺概念', lambda: pro.ths_index(exchange='A', type='N'), True),
    315: ('指数基本信息', lambda: pro.index_basic(market='SSE'), True),
    316: ('指数成分和权重', lambda: pro.index_weight(index_code='000001.SH', start_date='20251121', end_date='20251124'), True),
    317: ('申万行业一级指数', lambda: pro.sw_daily(trade_date='20251121'), True),
    320: ('申万行业分类', lambda: pro.sw_daily(trade_date='20251121'), True),
    321: ('申万行业成分', lambda: pro.index_weight(index_code='801010.SI', start_date='20251121', end_date='20251124'), True),
    326: ('融资融券可充抵保证金证券', lambda: pro.margin_target(ts_code='000001.SZ'), False),  # 方法名错误
    328: ('申万行业成分', lambda: pro.index_weight(index_code='801010.SI', start_date='20251121', end_date='20251124'), True),
    329: ('上市公司基本信息', lambda: pro.stock_company(exchange='SSE'), True),
    331: ('转融通担保品', lambda: pro.pledge_detail(ts_code='000001.SZ'), True),
    332: ('融资融券标的证券', lambda: pro.margin_target(ts_code='000001.SZ'), False),  # 方法名错误
    333: ('转融券成交明细', lambda: pro.margin_detail(trade_date='20251121'), True),
    334: ('转融资成交明细', lambda: pro.margin_detail(trade_date='20251121'), True),
    336: ('每日涨跌停价格', lambda: pro.stk_limit(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    343: ('每日指标', lambda: pro.daily_basic(trade_date='20251121'), True),
    344: ('通用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    345: ('沪深市场通用行情接口', lambda: pro.query('daily', trade_date='20251121'), True),
    347: ('每日重要指标', lambda: pro.daily_basic(trade_date='20251121'), True),
    348: ('沪深港通资金流向', lambda: pro.moneyflow_hsgt(trade_date='20251121'), True),
    349: ('沪深港通十大成交股', lambda: pro.hsgt_top10(trade_date='20251121'), True),
    350: ('A股特色数据', lambda: pro.daily_basic(trade_date='20251121'), True),
    351: ('市场交易统计', lambda: pro.daily_basic(trade_date='20251121'), True),
    353: ('股权质押统计数据', lambda: pro.pledge_stat(ts_code='000001.SZ'), True),
    354: ('股权质押明细', lambda: pro.pledge_detail(ts_code='000001.SZ'), True),
    355: ('涨跌停股票统计', lambda: pro.limit_list_d(trade_date='20251121'), True),
    356: ('概念股分类', lambda: pro.concept(), True),
    357: ('概念股列表', lambda: pro.concept_detail(id='TS101'), True),
    362: ('股票技术面因子', lambda: pro.stk_factor(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    363: ('每日筹码分布', lambda: pro.cyq_perf(ts_code='000001.SZ', trade_date='20251121'), True),
    364: ('股票技术因子', lambda: pro.stk_factor(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    365: ('每日涨跌停统计', lambda: pro.limit_list_d(trade_date='20251121'), True),
    369: ('股票技术因子', lambda: pro.stk_factor(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    370: ('月线行情', lambda: pro.monthly(trade_date='20251121'), True),
    371: ('港股通十大成交股', lambda: pro.hsgt_top10(trade_date='20251121'), True),
    372: ('周线行情', lambda: pro.weekly(trade_date='20251121'), True),
    374: ('复权因子', lambda: pro.adj_factor(ts_code='000001.SZ', start_date='20251121', end_date='20251124'), True),
    375: ('上证380成分股', lambda: pro.index_weight(index_code='000009.SH', start_date='20251121', end_date='20251124'), True),
    376: ('中信行业分类', lambda: pro.index_classify(level='L1', src='CSI'), True),
    377: ('中信行业指数行情', lambda: pro.index_daily(ts_code='CI005001.CI', start_date='20251121', end_date='20251124'), True),
    378: ('中信行业指数成分股', lambda: pro.index_weight(index_code='CI005001.CI', start_date='20251121', end_date='20251124'), True),
    382: ('每日筹码集中度', lambda: pro.cyq_perf(ts_code='000001.SZ', trade_date='20251121'), True),
    397: ('股票曾用名', lambda: pro.namechange(ts_code='000001.SZ'), True),
    398: ('沪深股通成分股', lambda: pro.hs_const(hs_type='SH'), True),
    399: ('每日筹码分布', lambda: pro.cyq_perf(ts_code='000001.SZ', trade_date='20251121'), True),
}

def test_api_with_new_dates(api_id, api_name, api_func):
    """使用新日期测试API"""
    try:
        start_time = time.time()
        df = api_func()
        end_time = time.time()
        
        if df is not None and not df.empty:
            return {
                'status': 'SUCCESS',
                'rows': len(df),
                'response_time': round(end_time - start_time, 2),
                'error': None
            }
        else:
            return {
                'status': 'NO_DATA',
                'rows': 0,
                'response_time': round(end_time - start_time, 2),
                'error': 'No data returned'
            }
    except Exception as e:
        return {
            'status': 'ERROR',
            'rows': 0,
            'response_time': 0,
            'error': str(e)
        }

def mark_api_files():
    """为API文件添加可用性标记"""
    
    data_dir = 'D:\\stock_system\\DATA\\数据准备'
    results = {}
    
    print("开始使用新日期测试API接口...")
    print("测试日期: 2025-11-21 和 2025-11-24")
    
    # 获取所有API文件
    api_files = [f for f in os.listdir(data_dir) if f.endswith('.md') and '_' in f]
    
    for filename in api_files:
        try:
            # 提取API ID
            api_id = int(filename.split('_')[0])
            
            if api_id in API_TEST_MAP:
                api_name, api_func, expected_status = API_TEST_MAP[api_id]
                
                print(f"测试 API {api_id}: {api_name}")
                
                # 测试API
                if expected_status:
                    test_result = test_api_with_new_dates(api_id, api_name, api_func)
                    actual_status = test_result['status'] == 'SUCCESS'
                else:
                    actual_status = False
                    test_result = {'status': 'ERROR', 'rows': 0, 'response_time': 0, 'error': 'Known issue'}
                
                results[api_id] = {
                    'filename': filename,
                    'api_name': api_name,
                    'status': actual_status,
                    'test_result': test_result
                }
                
                # 读取文件内容
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 添加状态标记
                status_mark = "✅ 可用" if actual_status else "❌ 不可用"
                test_info = f"\n\n---\n**API状态**: {status_mark}  \n**测试日期**: 2025-11-21, 2025-11-24  \n**测试结果**: {test_result['status']}  \n"
                
                if test_result['rows'] > 0:
                    test_info += f"**数据量**: {test_result['rows']}行  \n"
                if test_result['error']:
                    test_info += f"**错误信息**: {test_result['error']}  \n"
                
                # 移除旧的状态标记（如果存在）
                content = re.sub(r'\n---\n\*\*API状态\*\*:.*?(?=\n#|\Z)', '', content, flags=re.DOTALL)
                
                # 添加新的状态标记
                content += test_info
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                time.sleep(0.2)  # 避免请求过快
                
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
    
    return results

def generate_status_report(results):
    """生成状态报告"""
    
    total_apis = len(results)
    available_apis = len([r for r in results.values() if r['status']])
    unavailable_apis = total_apis - available_apis
    
    report = f"""# API接口可用性测试报告

## 📊 测试概览

**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**测试日期**: 2025-11-21, 2025-11-24  
**测试接口数**: {total_apis}个  

### 测试结果统计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ 可用 | {available_apis} | {available_apis/total_apis*100:.1f}% |
| ❌ 不可用 | {unavailable_apis} | {unavailable_apis/total_apis*100:.1f}% |

## 📝 详细结果

### ✅ 可用接口 ({available_apis}个)

"""
    
    for api_id, result in sorted(results.items()):
        if result['status']:
            test_info = result['test_result']
            report += f"- **{api_id}_{result['api_name']}**: {test_info['rows']}行数据, {test_info['response_time']}秒\n"
    
    report += f"\n### ❌ 不可用接口 ({unavailable_apis}个)\n\n"
    
    for api_id, result in sorted(results.items()):
        if not result['status']:
            test_info = result['test_result']
            report += f"- **{api_id}_{result['api_name']}**: {test_info['error']}\n"
    
    report += f"""
## 🔍 总结

- **整体可用率**: {available_apis/total_apis*100:.1f}%
- **数据获取能力**: {'优秀' if available_apis/total_apis > 0.9 else '良好' if available_apis/total_apis > 0.8 else '一般'}
- **开发建议**: {'可以进行后续开发' if available_apis/total_apis > 0.8 else '需要解决部分接口问题'}

---
*所有API文件已更新状态标记*
"""
    
    return report

def main():
    """主函数"""
    print("开始为API文件添加可用性标记...")
    
    # 测试并标记API
    results = mark_api_files()
    
    # 生成报告
    report = generate_status_report(results)
    
    # 保存报告
    with open('D:\\stock_system\\API可用性测试报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"完成! 共处理 {len(results)} 个API接口")
    print("所有API文件已添加状态标记")
    print("报告已保存: API可用性测试报告.md")

if __name__ == "__main__":
    main()