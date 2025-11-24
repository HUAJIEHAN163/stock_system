import os
import re
from datetime import datetime

def merge_to_html():
    """合并所有文档为HTML格式"""
    
    # API分类数据
    api_data = {
        '多只股票多日查询（真正批量数据）': {
            '基础数据': {
                25: '股票列表', 329: '上市公司基本信息', 26: '交易日历',
                100: 'HS300成分股', 112: '上证50成分股', 193: '中证500成分股',
                194: '中证1000成分股', 375: '上证380成分股', 123: '科创板股票', 262: '创业板股票'
            },
            '行情数据': {
                27: 'A股日线行情', 372: '周线行情', 370: '月线行情', 28: '指数日线行情',
                315: '指数基本信息', 316: '指数成分和权重', 317: '申万行业一级指数',
                32: '大盘指数每日指标', 109: '市场通用行情接口', 183: '沪深市场通用行情接口',
                48: '备用行情接口', 255: '港股行情'
            },
            '参考数据': {
                61: '沪深股通资金流向', 62: '沪深股通十大成交股', 110: '中概股列表',
                111: '中概股月线行情', 124: '港股列表', 160: '港股通成分股',
                161: '港股通每日成交统计', 166: '港股通资金流向', 175: '港股通十大成交股'
            },
            '特色数据': {
                292: '概念股分类', 293: '概念股列表', 294: '地域分类',
                296: '申万行业分类', 328: '申万行业成分', 295: '中信行业分类'
            }
        },
        '单只股票多日查询': {
            '行情数据': {374: '复权因子', 144: '停复牌信息', 336: '每日涨跌停价格'},
            '财务数据': {
                33: '利润表', 36: '资产负债表', 44: '现金流量表', 45: '业绩预告',
                46: '业绩快报', 103: '分红送股', 79: '财务指标数据',
                80: '财务审计意见', 81: '主营业务构成', 162: '财务数据'
            },
            '特色数据': {
                274: '券商盈利预测数据', 188: '限售股解禁', 353: '股权质押统计数据',
                354: '股权质押明细', 364: '股票技术因子', 399: '每日筹码分布',
                275: '同花顺概念和行业', 267: '同花顺概念'
            },
            '资金流向': {170: '个股资金流向'}
        },
        '单只股票逐条获取（单日单股）': {
            '基础数据': {397: '股票曾用名', 398: '沪深股通成分股'},
            '行情数据': {
                145: '每日停复牌统计', 146: '停牌原因', 365: '每日涨跌停统计', 214: '港股通每日成交统计'
            },
            '资金流向': {
                348: '沪深港通资金流向', 349: '沪深港通十大成交股', 371: '港股通十大成交股',
                343: '每日指标', 344: '通用行情接口', 345: '沪深市场通用行情接口', 47: '备用行情接口'
            },
            '打板数据': {
                106: '涨跌停统计', 107: '每日涨跌停价格', 355: '涨跌停股票统计', 298: '股票回购',
                356: '概念股分类', 357: '概念股列表', 259: '限售股解禁', 260: '股权质押统计数据',
                261: '股权质押明细', 362: '股票技术面因子', 363: '每日筹码分布', 382: '每日筹码集中度',
                369: '股票技术因子', 311: '同花顺概念和行业', 312: '同花顺概念', 320: '申万行业分类',
                321: '申万行业成分', 376: '中信行业分类', 377: '中信行业指数行情', 378: '中信行业指数成分股',
                347: '每日重要指标', 350: 'A股特色数据', 351: '市场交易统计'
            },
            '两融转融通': {
                58: '融资融券交易汇总', 59: '融资融券交易明细', 326: '融资融券可充抵保证金证券',
                332: '融资融券标的证券', 331: '转融通担保品', 333: '转融券成交明细', 334: '转融资成交明细'
            }
        }
    }
    
    # HTML模板
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tushare API 完整文档</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .toc {{ position: fixed; left: 20px; top: 20px; width: 300px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-height: 80vh; overflow-y: auto; }}
        .content {{ margin-left: 340px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; margin-top: 40px; }}
        h3 {{ color: #7f8c8d; }}
        .api-section {{ border: 1px solid #ecf0f1; margin: 20px 0; padding: 20px; border-radius: 5px; background: #fafafa; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .toc a {{ text-decoration: none; color: #3498db; display: block; padding: 5px 0; }}
        .toc a:hover {{ color: #2980b9; }}
        .back-to-top {{ position: fixed; bottom: 20px; right: 20px; background: #3498db; color: white; padding: 10px; border-radius: 50%; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="toc">
        <h3>📚 目录导航</h3>
"""
    
    # 生成目录
    for main_category, categories in api_data.items():
        html_content += f'        <a href="#{main_category.replace("（", "").replace("）", "")}">{main_category}</a>\n'
        for category, apis in categories.items():
            html_content += f'        <div style="margin-left: 15px;"><a href="#{category}">{category}</a></div>\n'
    
    html_content += """    </div>
    
    <div class="content">
        <h1>🚀 Tushare API 完整文档</h1>
        <p><strong>生成时间:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        <p><strong>文档说明:</strong> 本文档包含所有102个Tushare API接口的详细说明</p>
        
"""
    
    # 生成内容
    for main_category, categories in api_data.items():
        category_id = main_category.replace("（", "").replace("）", "")
        html_content += f'        <h2 id="{category_id}">{main_category}</h2>\n'
        
        for category, apis in categories.items():
            html_content += f'        <h3 id="{category}">{category}</h3>\n'
            
            for doc_id, api_name in apis.items():
                # 读取对应的文档文件
                safe_filename = re.sub(r'[<>:"/\\|?*]', '_', api_name)
                file_path = f'D:\\stock_system\\docs\\{doc_id}_{safe_filename}.md'
                
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 转换Markdown到HTML
                    content = content.replace('# ', '<h4>').replace('\n', '</h4>\n', 1)
                    content = content.replace('## ', '<h5>').replace('\n', '</h5>\n')
                    content = content.replace('**', '<strong>').replace('**', '</strong>')
                    content = content.replace('```python', '<pre><code>').replace('```', '</code></pre>')
                    content = re.sub(r'\| (.*?) \|', r'<td>\1</td>', content)
                    
                    html_content += f'        <div class="api-section" id="api_{doc_id}">\n'
                    html_content += f'            <h4>{api_name} (ID: {doc_id})</h4>\n'
                    html_content += f'            {content}\n'
                    html_content += '        </div>\n\n'
    
    html_content += """    </div>
    
    <a href="#" class="back-to-top">↑</a>
    
    <script>
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>"""
    
    # 保存HTML文件
    with open('D:\\stock_system\\tushare_complete_docs.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML文档已生成: tushare_complete_docs.html")

def merge_to_markdown():
    """合并所有文档为单个Markdown文件"""
    
    # 读取所有文档
    docs_dir = 'D:\\stock_system\\docs'
    all_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
    
    md_content = f"""# 🚀 Tushare API 完整文档

> **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **文档数量**: {len(all_files)}个API接口  
> **使用说明**: 使用Ctrl+F搜索特定API

## 📚 目录

"""
    
    # 生成目录
    for i, filename in enumerate(sorted(all_files), 1):
        api_name = filename.replace('.md', '').split('_', 1)[1]
        doc_id = filename.split('_')[0]
        md_content += f"{i}. [{api_name}](#api-{doc_id})\n"
    
    md_content += "\n---\n\n"
    
    # 合并所有文档内容
    for filename in sorted(all_files):
        file_path = os.path.join(docs_dir, filename)
        doc_id = filename.split('_')[0]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加锚点
        content = content.replace('# ', f'# <a id="api-{doc_id}"></a>')
        md_content += content + "\n\n---\n\n"
    
    # 保存Markdown文件
    with open('D:\\stock_system\\tushare_complete_docs.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("Markdown文档已生成: tushare_complete_docs.md")

def main():
    """主函数"""
    print("选择合并格式:")
    print("1. HTML格式 (推荐)")
    print("2. Markdown格式")
    print("3. 两种格式都生成")
    
    choice = input("请输入选择 (1/2/3): ").strip()
    
    if choice == '1':
        merge_to_html()
    elif choice == '2':
        merge_to_markdown()
    elif choice == '3':
        merge_to_html()
        merge_to_markdown()
        print("两种格式都已生成完成!")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()