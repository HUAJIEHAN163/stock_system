# 📋 版本更新说明 v0.6.0-beta

## 🎯 版本概述

**发布日期**: 2024年12月  
**版本类型**: Beta测试版  
**主要特性**: 数据库系统完善和初始化优化

本版本基于《多只股票多日查询API测试报告》的结果，对数据库结构和数据初始化系统进行了全面优化，显著提升了系统的稳定性和数据完整性。

---

## 🚀 重大更新

### 1. 数据库结构完善

#### 新增核心数据表
```sql
-- 上市公司基本信息 (基于测试报告新增)
CREATE TABLE stock_company (
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
);

-- IPO新股列表 (基于测试报告新增)
CREATE TABLE new_share (
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
);

-- 复权因子 (基于测试报告新增)
CREATE TABLE adj_factor (
    ts_code TEXT,
    trade_date TEXT,
    adj_factor REAL,
    update_time TEXT,
    PRIMARY KEY (ts_code, trade_date)
);

-- 指数每日基本指标 (基于测试报告新增)
CREATE TABLE index_dailybasic (
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
);
```

#### 现有表结构优化
- 为现有表添加 `src` 字段（数据源标识）
- 为现有表添加 `test_status` 字段（API测试状态）
- 创建数据库迁移脚本 `database_migration.py`

### 2. 数据初始化系统优化

#### API权限管理
- **成功率提升**: 从不确定提升到90.9% (10/11个API成功)
- **智能跳过**: 自动跳过权限不足的API (如stk_mins分钟数据)
- **错误处理**: 基于测试报告的智能重试机制

#### 时间范围配置优化
```python
# 统一为2年配置（根据用户需求调整）
TIME_RANGES = {
    'trade_cal': 'last_2_years',        # 交易日历: 2年
    'new_share': 'last_2_years',        # IPO新股: 2年
    'daily': 'last_2_years',            # 日线行情: 2年
    'weekly': 'last_2_years',           # 周线行情: 2年
    'monthly': 'last_2_years',          # 月线行情: 2年
    'adj_factor': 'last_2_years',       # 复权因子: 2年
    'index_dailybasic': 'last_2_years'  # 指数指标: 2年
}
```

#### 批次执行策略
- **第1批**: 基础数据（股票列表、交易日历、公司信息、新股列表）
- **第2批**: 历史行情（日线、周线、月线、复权因子、指数指标）
- **第3批**: 高级数据（暂时跳过权限不足的API）

### 3. 用户界面优化

#### 初始化按钮功能调整
- **"数据初始化"**: 执行完整初始化（batch_1 + batch_2）
- **"基础初始化"**: 只执行基础数据（batch_1）
- **进度显示**: 实时显示API调用进度和结果

---

## 📊 性能提升

### API调用效率
| 指标 | v0.5.0 | v0.6.0 | 提升 |
|------|--------|--------|------|
| API成功率 | 不确定 | 90.9% | 显著提升 |
| 平均响应时间 | 未测试 | 1.03秒 | 基准建立 |
| 数据记录数 | 有限 | 15,197条 | 大幅增加 |
| 权限错误处理 | 手动 | 自动跳过 | 智能化 |

### 数据完整性
- **基础数据**: 100%覆盖（股票、公司、交易日历、新股）
- **行情数据**: 2年历史数据（日线、周线、月线）
- **技术数据**: 复权因子、指数指标
- **数据源标识**: 支持多数据源区分

---

## 🔧 技术改进

### 1. 数据库迁移系统
```python
# 新增数据库迁移管理器
class DatabaseMigration:
    def migrate_to_latest(self):
        # 自动添加新表
        # 自动添加新字段
        # 创建索引优化
```

### 2. API配置管理
```python
# 基于测试报告的API配置
BATCH_1_APIS = {
    'stock_basic': {'test_status': 'SUCCESS', 'records': 5453},
    'stock_company': {'test_status': 'SUCCESS', 'records': 2431},
    'trade_cal': {'test_status': 'SUCCESS', 'records': 370},
    'new_share': {'test_status': 'SUCCESS', 'records': 112}
}

BATCH_2_APIS = {
    'daily': {'test_status': 'SUCCESS', 'strategy': 'multi_stock_multi_date'},
    'weekly': {'test_status': 'SUCCESS', 'records': 112},
    'monthly': {'test_status': 'SUCCESS', 'records': 44},
    'adj_factor': {'test_status': 'SUCCESS', 'records': 492},
    'index_dailybasic': {'test_status': 'SUCCESS', 'records': 1}
}

BATCH_3_APIS = {
    'stk_mins': {'test_status': 'FAILED', 'skip_reason': '需要单独申请分钟数据权限'}
}
```

### 3. 数据校验优化
```python
# 基于实际测试数据的校验规则
VALIDATION_RULES = {
    'stock_basic': {'min_records': 5000},      # 测试结果: 5,453行
    'stock_company': {'min_records': 2000},    # 测试结果: 2,431行
    'trade_calendar': {'min_records': 300},    # 测试结果: 370行
    'new_share': {'min_records': 50}           # 测试结果: 112行
}
```

---

## 🐛 问题修复

### 1. 初始化问题修复
- **问题**: 数据初始化只执行batch_1，缺少历史行情数据
- **原因**: 默认初始化按钮只配置了基础数据批次
- **解决**: 调整按钮功能，默认执行完整初始化

### 2. API权限问题
- **问题**: 权限不足的API导致初始化失败
- **原因**: 未区分不同权限级别的API
- **解决**: 基于测试报告智能跳过权限不足的API

### 3. 时间范围不统一
- **问题**: 不同API使用不同时间范围，数据不一致
- **原因**: 性能优化导致配置复杂化
- **解决**: 统一配置为2年，提供一致的数据范围

---

## 📋 升级指南

### 自动升级
1. 运行数据库迁移脚本：
```bash
python src/data/database_migration.py
```

2. 重新执行数据初始化：
- 点击"数据初始化"按钮
- 系统将自动获取完整的2年历史数据

### 手动升级
如果自动迁移失败，可以：
1. 备份现有数据库
2. 删除 `database/stock_data.db`
3. 重新运行完整初始化

---

## 🎯 下一步计划

### v0.7.0-beta 规划
- K线图表集成 (Matplotlib/Plotly)
- 高级筛选算法实现
- 实时预警推送机制
- 基础技术指标计算
- 增量数据更新优化

### 开发重点
1. **数据可视化**: 集成专业的股票图表库
2. **分析功能**: 实现技术指标和筛选算法
3. **实时功能**: 添加实时数据推送和预警
4. **用户体验**: 优化界面和交互逻辑

---

## 📞 技术支持

### 常见问题
1. **Q**: 升级后数据初始化很慢？
   **A**: 新版本获取2年完整数据，首次初始化需要更长时间，这是正常现象。

2. **Q**: 某些API仍然失败？
   **A**: 检查Token权限等级，部分高级API需要更高积分。

3. **Q**: 如何查看详细的初始化日志？
   **A**: 使用"带控制台日志启动"方式，或查看 `logs/` 目录下的日志文件。

### 反馈渠道
- 查看项目文档了解更多详情
- 关注版本更新获取最新功能

---

*版本更新完成时间: 2024年12月*  
*基于文档: 《数据库设计与初始化方案》、《数据初始化问题分析》*  
*测试依据: 《多只股票多日查询API测试报告》*