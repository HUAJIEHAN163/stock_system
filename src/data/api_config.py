#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API配置 - 定义数据初始化的API配置
"""

from datetime import datetime, timedelta

# 数据源映射
DATA_SOURCE_MAPPING = {
    'tushare': 'TS',
    'tudata': 'TD',
    'sw': 'SW',
    'zx': 'ZX', 
    'ths': 'THS'
}

# 时间范围配置
def get_time_range(range_type):
    """获取时间范围"""
    now = datetime.now()
    
    ranges = {
        'last_1_year': (
            (now - timedelta(days=365)).strftime('%Y%m%d'),
            now.strftime('%Y%m%d')
        ),
        'last_2_years': (
            (now - timedelta(days=730)).strftime('%Y%m%d'),
            now.strftime('%Y%m%d')
        ),
        'last_5_years': (
            (now - timedelta(days=1825)).strftime('%Y%m%d'),
            now.strftime('%Y%m%d')
        )
    }
    
    return ranges.get(range_type, ranges['last_2_years'])

# 第1批：基础数据（基于测试报告中成功的API）
BATCH_1_APIS = {
    'stock_basic': {
        'api_name': 'stock_basic',
        'table': 'stock_basic',
        'params': {
            'exchange': '',
            'list_status': 'L',
            'fields': 'ts_code,symbol,name,area,industry,market,list_date,delist_date,is_hs'
        },
        'description': '股票基本信息 (测试成功: 5,453行)',
        'required': True,
        'test_status': 'SUCCESS'
    },
    'stock_company': {
        'api_name': 'stock_company',
        'table': 'stock_company',
        'params': {
            'exchange': 'SSE',
            'fields': 'ts_code,com_name,chairman,manager,secretary,reg_capital,setup_date,province,city,website,email,employees,main_business'
        },
        'description': '上市公司基本信息 (测试成功: 2,431行)',
        'required': False,
        'test_status': 'SUCCESS'
    },
    'trade_cal': {
        'api_name': 'trade_cal',
        'table': 'trade_calendar', 
        'params': {
            'exchange': 'SSE',
            'fields': 'cal_date,is_open,pretrade_date'
        },
        'time_range': 'last_2_years',
        'description': '交易日历 (测试成功: 370行)',
        'required': True,
        'test_status': 'SUCCESS'
    },
    'new_share': {
        'api_name': 'new_share',
        'table': 'new_share',
        'params': {
            'fields': 'ts_code,sub_code,name,ipo_date,issue_date,amount,market_amount,price,pe,limit_amount,funds,ballot'
        },
        'time_range': 'last_2_years',
        'description': 'IPO新股列表 (测试成功: 112行)',
        'required': False,
        'test_status': 'SUCCESS'
    }
}

# 第2批：历史行情（基于测试报告中成功的API）
BATCH_2_APIS = {
    'daily': {
        'api_name': 'daily',
        'table': 'daily_basic',
        'params': {
            'fields': 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
        },
        'time_range': 'last_2_years',  # 统一为2年历史数据
        'strategy': 'multi_stock_multi_date',  # 使用测试成功的策略
        'batch_size': 50,  # 根据测试结果调整
        'description': 'A股日线行情 (测试成功: 5,444行单日全市场 + 738行多股票多日)',
        'required': False,
        'test_status': 'SUCCESS'
    },
    'weekly': {
        'api_name': 'weekly',
        'table': 'weekly_basic',
        'params': {
            'fields': 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
        },
        'time_range': 'last_2_years',
        'test_codes': '000001.SZ,600000.SH',  # 使用测试成功的股票代码
        'description': '周线行情 (测试成功: 112行)',
        'required': False,
        'test_status': 'SUCCESS'
    },
    'monthly': {
        'api_name': 'monthly',
        'table': 'monthly_basic',
        'params': {
            'fields': 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
        },
        'time_range': 'last_2_years',
        'test_codes': '000001.SZ,600000.SH',  # 使用测试成功的股票代码
        'description': '月线行情 (测试成功: 44行)',
        'required': False,
        'test_status': 'SUCCESS'
    },
    'adj_factor': {
        'api_name': 'adj_factor',
        'table': 'adj_factor',
        'params': {
            'ts_code': '000001.SZ,600000.SH',
            'fields': 'ts_code,trade_date,adj_factor'
        },
        'time_range': 'last_2_years',
        'description': '复权因子 (测试成功: 492行)',
        'required': False,
        'test_status': 'SUCCESS'
    },
    'index_dailybasic': {
        'api_name': 'index_dailybasic',
        'table': 'index_dailybasic',
        'params': {
            'ts_code': '000001.SH,399001.SZ',
            'fields': 'ts_code,trade_date,total_mv,float_mv,total_share,float_share,free_share,turnover_rate,turnover_rate_f,pe,pe_ttm,pb'
        },
        'time_range': 'last_2_years',
        'description': '大盘指数每日指标 (测试成功: 1行)',
        'required': False,
        'test_status': 'SUCCESS'
    }
}

# 第3批：高级数据（暂时禁用，等待权限升级）
BATCH_3_APIS = {
    # 注意：以下API未在测试报告中验证，可能需要更高权限
    'stk_mins': {
        'api_name': 'stk_mins',
        'table': 'stock_mins',
        'params': {
            'ts_code': '000001.SZ',
            'freq': '60min',
            'fields': 'ts_code,trade_time,open,close,high,low,vol,amount'
        },
        'time_range': 'last_1_year',
        'description': '股票历史分钟行情 (测试失败: 需要单独权限)',
        'required': False,
        'test_status': 'FAILED',
        'skip_reason': '需要单独申请分钟数据权限',
        'enabled': False
    }
}

# 数据完整性检测配置
DATA_INTEGRITY_CONFIG = {
    'daily_basic': {
        'expected_stock_count': 5000,
        'missing_threshold': 0.05,
        'check_days': 30,
        'full_update_threshold': 0.20
    },
    'index_daily': {
        'expected_index_count': 300,
        'missing_threshold': 0.03,
        'check_days': 30,
        'full_update_threshold': 0.15
    }
}

# 数据校验规则 - 基于测试报告结果调整
VALIDATION_RULES = {
    'stock_basic': {
        'min_records': 5000,  # 测试结果: 5,453行
        'required_fields': ['ts_code', 'name', 'market']
    },
    'stock_company': {
        'min_records': 2000,  # 测试结果: 2,431行
        'required_fields': ['ts_code', 'com_name']
    },
    'trade_calendar': {
        'min_records': 300,   # 测试结果: 370行
        'required_fields': ['cal_date', 'is_open']
    },
    'new_share': {
        'min_records': 50,    # 测试结果: 112行
        'required_fields': ['ts_code', 'name', 'ipo_date']
    },
    'daily_basic': {
        'price_validation': True,
        'volume_validation': True,
        'min_records_per_stock': 200  # 每只股票最少记录数
    },
    'weekly_basic': {
        'min_records': 50,    # 测试结果: 112行
        'required_fields': ['ts_code', 'trade_date', 'close']
    },
    'monthly_basic': {
        'min_records': 20,    # 测试结果: 44行
        'required_fields': ['ts_code', 'trade_date', 'close']
    }
}

# 重试配置 - 基于测试经验优化
RETRY_CONFIG = {
    'max_retries': 3,
    'retry_delay': [1, 3, 5],  # 缩短重试间隔
    'retry_conditions': ['network_error', 'api_limit', 'timeout', 'permission_denied'],
    'skip_on_permission_error': True,  # 权限错误时直接跳过
    'api_rate_limit': 0.2  # API调用间隔(秒)
}

# 测试报告统计信息
TEST_REPORT_SUMMARY = {
    'test_date': '2025-11-24',
    'total_apis_tested': 11,
    'successful_apis': 10,
    'failed_apis': 1,
    'success_rate': 90.9,
    'total_records': 15197,
    'avg_response_time': 1.03,
    'notes': '基于 tudata 库测试结果，分钟数据需要单独权限'
}