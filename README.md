# 🚀 Tushare股票数据系统

> 基于Tushare和Tudata的股票数据分析系统，包含完整的API文档和数据获取工具

## 📋 项目概述

本项目提供了完整的Tushare API接口分类和本地文档系统，帮助用户快速了解和使用各种股票数据接口。

### 🎯 主要功能

- **API接口分类**: 将102个Tushare API按使用特点精确分类
- **本地文档系统**: 爬取并保存所有API详细文档到本地
- **环境管理**: 自动化环境安装和测试脚本
- **文档生成**: 支持多种格式的完整文档生成

## 🛠️ 环境要求

- **Python**: 3.8+ 
- **操作系统**: Windows/Linux/macOS
- **内存**: 建议4GB+
- **网络**: 需要访问tushare.pro

## 📦 快速安装

### 方法1: 自动安装（推荐）

```bash
# 1. 克隆项目
git clone <项目地址>
cd stock_system

# 2. 运行自动安装脚本
python install_env.py

# 3. 测试环境
python test_env.py
```

### 方法2: 手动安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或者逐个安装核心包
pip install tushare tudata pandas numpy requests beautifulsoup4
```

## 🔧 配置说明

### 1. 获取Tushare Token

1. 注册账号: [https://tushare.pro/register](https://tushare.pro/register)
2. 获取token: [https://tushare.pro/user/token](https://tushare.pro/user/token)
3. 设置token:

```python
import tushare as ts
ts.set_token('your_token_here')
pro = ts.pro_api()
```

### 2. 验证安装

```python
# 运行测试脚本
python test_env.py
```

## 📚 项目结构

```
stock_system/
├── README.md                          # 项目说明
├── requirements.txt                   # 依赖包列表
├── run.py                            # 标准启动脚本
├── start_with_console.py             # 带控制台日志启动脚本
├── 启动系统(带日志).bat               # Windows批处理启动文件
├── src/                              # 源代码目录
│   ├── main.py                       # 主程序入口
│   ├── ui/                           # 用户界面
│   │   ├── main_window.py            # 主窗口
│   │   └── windows/                  # 功能窗口
│   └── data/                         # 数据处理模块
├── logs/                             # 日志文件目录
│   └── stock_system_YYYYMMDD.log     # 按日期命名的日志文件
├── database/                         # 数据库文件
├── config/                           # 配置文件
├── docs/                             # 本地API文档目录
│   ├── 25_股票列表.md
│   ├── 27_A股日线行情.md
│   └── ... (102个API文档)
└── 数据调查/                          # API分类和文档
    └── 数据准备/
        └── 00_tushare_api_classification.md  # API分类文档
```

## 🎯 API分类说明

### 📊 多只股票多日查询（37个接口）
**特点**: 真正的批量数据，效率最高
- 基础数据: 股票列表、指数成分股等
- 行情数据: 日/周/月线行情等
- 参考数据: 港股通、中概股等
- 特色数据: 概念股、行业分类等

### 🎯 单只股票多日查询（22个接口）  
**特点**: 需指定股票代码，可获取历史数据
- 行情数据: 复权因子、停复牌信息等
- 财务数据: 三大报表、业绩预告等
- 特色数据: 质押、解禁、技术因子等

### ⚠️ 单只股票逐条获取（43个接口）
**特点**: 需指定股票和日期，API使用量大
- 基础数据: 股票曾用名等
- 资金流向: 各类流向统计
- 打板数据: 涨跌停、筹码等
- 两融转融通: 融资融券相关

## 🚀 系统启动

### 启动方式

#### 方法1: 带控制台日志启动（推荐）
```bash
# 命令行启动
python start_with_console.py

# 或双击批处理文件（Windows）
启动系统(带日志).bat
```

#### 方法2: 标准启动
```bash
# 标准启动（无控制台日志）
python run.py
```

### 🔍 日志系统

- **控制台日志**: 实时显示系统运行状态和操作日志
- **文件日志**: 自动保存到 `logs/` 目录，按日期命名
- **日志级别**: INFO级别，包含详细的操作记录
- **日志格式**: 时间戳 + 模块名 + 级别 + 消息内容

**日志文件位置**: `logs/stock_system_YYYYMMDD.log`

## 🔍 使用示例

### 1. 查看API分类

```python
# 打开主分类文档
# 文件: tushare_api_classification.md
# 包含所有API的分类和本地文档链接
```

### 2. 获取股票基础数据

```python
import tushare as ts

# 设置token
ts.set_token('your_token_here')
pro = ts.pro_api()

# 获取股票列表
df = pro.stock_basic(exchange='', list_status='L', 
                    fields='ts_code,symbol,name,area,industry,list_date')
print(df.head())
```

### 3. 获取行情数据

```python
# 获取日线行情
df = pro.daily(ts_code='000001.SZ', start_date='20240101', end_date='20240131')
print(df.head())
```

## 📖 文档系统

### 本地文档特点
- **格式**: Markdown格式，支持表格和代码高亮
- **内容**: 包含API参数说明、返回字段、代码示例  
- **离线**: 无需网络即可查看详细文档
- **链接**: 支持本地跳转和在线文档双链接

### 文档生成
```python
# 重新爬取API文档
python crawl_api_docs.py

# 生成合并文档
python merge_docs.py
```

## 🛠️ 开发工具

### 环境管理
```bash
# 安装环境
python install_env.py

# 测试环境  
python test_env.py

# 更新依赖
pip install -r requirements.txt --upgrade
```

### 启动选项
```bash
# 带控制台日志启动（开发调试推荐）
python start_with_console.py

# 标准启动
python run.py

# 直接启动主程序
python src/main.py
```

### 文档管理
```bash
# 爬取最新API文档
python crawl_api_docs.py

# 更新分类文档
python update_local_links.py

# 生成完整文档
python merge_docs.py
```

## ❓ 常见问题

### Q: 提示"token验证失败"？
A: 请确保已正确设置tushare token，并且账户积分足够

### Q: 某些API无法访问？
A: 部分API需要更高积分等级，请查看tushare官网积分要求

### Q: 如何更新API文档？
A: 运行 `python crawl_api_docs.py` 重新爬取最新文档

### Q: 文档链接无法跳转？
A: 确保使用支持Markdown的编辑器，如VS Code、Typora等

### Q: 如何查看系统运行日志？
A: 使用 `python start_with_console.py` 启动，或双击 `启动系统(带日志).bat` 文件

### Q: 控制台窗口可以关闭吗？
A: 建议保持控制台窗口打开以查看实时日志，关闭控制台不会影响GUI运行

### Q: 日志文件在哪里？
A: 日志文件自动保存在 `logs/` 目录下，按日期命名

## 📞 技术支持

- **Tushare官网**: [https://tushare.pro](https://tushare.pro)
- **API文档**: [https://tushare.pro/document/2](https://tushare.pro/document/2)
- **积分获取**: [https://tushare.pro/document/1?doc_id=13](https://tushare.pro/document/1?doc_id=13)

## 📄 许可证

本项目仅供学习和研究使用，请遵守tushare的使用条款。

---

*最后更新: 2024年*  
*项目版本: v1.0*