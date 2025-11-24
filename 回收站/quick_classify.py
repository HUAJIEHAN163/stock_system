import re

def classify_tushare_apis():
    """基于URL ID和常见模式快速分类tushare API"""
    
    # 读取URL列表
    with open('D:\\stock_system\\tushare网页.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有URL和对应的doc_id
    urls = re.findall(r'https://tushare\.pro/document/2\?doc_id=(\d+)', content)
    
    # 基于经验的分类规则
    batch_apis = {
        '基础数据': [14],  # 股票列表等
        '行情数据': [15],  # 日线行情等
        '财务数据': [16],  # 利润表、资产负债表等
        '参考数据': [17],  # 交易日历等
        '特色数据': [291], # 概念股分类等
        '资金流向': [170, 348, 349, 371, 343, 344, 345, 47],
        '打板数据': [106, 107, 355, 298, 356, 357, 259, 260, 261, 362, 363, 382, 369, 311, 312, 320, 321, 376, 377, 378, 347, 350, 351]
    }
    
    single_apis = {
        '两融转融通': [58, 59, 326, 332, 331, 333, 334]
    }
    
    # 生成分类结果
    result = {
        '可以批量获取的数据': {},
        '单只股票逐条获取的数据': {}
    }
    
    # 分类批量API
    for category, doc_ids in batch_apis.items():
        result['可以批量获取的数据'][category] = [
            f"https://tushare.pro/document/2?doc_id={doc_id}" 
            for doc_id in doc_ids if str(doc_id) in urls
        ]
    
    # 分类单股票API
    for category, doc_ids in single_apis.items():
        result['单只股票逐条获取的数据'][category] = [
            f"https://tushare.pro/document/2?doc_id={doc_id}" 
            for doc_id in doc_ids if str(doc_id) in urls
        ]
    
    # 输出结果
    print("=== Tushare API 分类结果 ===\n")
    
    print("可以批量获取的数据:")
    for category, api_urls in result['可以批量获取的数据'].items():
        if api_urls:
            print(f"\n  {category}:")
            for url in api_urls:
                print(f"    - {url}")
    
    print("\n单只股票逐条获取的数据:")
    for category, api_urls in result['单只股票逐条获取的数据'].items():
        if api_urls:
            print(f"\n  {category}:")
            for url in api_urls:
                print(f"    - {url}")
    
    # 保存到文件
    with open('D:\\stock_system\\api_classification.txt', 'w', encoding='utf-8') as f:
        f.write("Tushare API 分类结果\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("可以批量获取的数据:\n")
        for category, api_urls in result['可以批量获取的数据'].items():
            if api_urls:
                f.write(f"\n{category}:\n")
                for url in api_urls:
                    f.write(f"  - {url}\n")
        
        f.write("\n单只股票逐条获取的数据:\n")
        for category, api_urls in result['单只股票逐条获取的数据'].items():
            if api_urls:
                f.write(f"\n{category}:\n")
                for url in api_urls:
                    f.write(f"  - {url}\n")
    
    print(f"\n分类结果已保存到: D:\\stock_system\\api_classification.txt")

if __name__ == "__main__":
    classify_tushare_apis()