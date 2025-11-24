import requests
from bs4 import BeautifulSoup
import re
import json
import time

def get_api_info(url):
    """获取单个页面的API信息"""
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找API接口名称
        api_name = soup.find('h1')
        if api_name:
            api_name = api_name.text.strip()
        
        # 查找参数表格
        tables = soup.find_all('table')
        params = []
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) >= 3:
                    param_name = cols[0].text.strip()
                    param_type = cols[1].text.strip()
                    param_desc = cols[2].text.strip()
                    params.append({
                        'name': param_name,
                        'type': param_type,
                        'description': param_desc
                    })
        
        return {
            'url': url,
            'api_name': api_name,
            'parameters': params
        }
    except Exception as e:
        print(f"获取 {url} 失败: {e}")
        return None

def classify_apis(apis):
    """分类API接口"""
    batch_apis = []  # 可批量获取的数据
    single_apis = []  # 单只股票逐条获取的数据
    
    for api in apis:
        if not api:
            continue
            
        api_name = api.get('api_name', '').lower()
        params = api.get('parameters', [])
        
        # 判断是否为批量接口
        is_batch = False
        has_ts_code = False
        
        for param in params:
            param_name = param['name'].lower()
            if param_name in ['ts_code', 'code', 'symbol']:
                has_ts_code = True
            if param_name in ['trade_date', 'start_date', 'end_date', 'list_status']:
                is_batch = True
        
        # 分类逻辑
        if ('list' in api_name or 'basic' in api_name or 
            '列表' in api_name or '基础' in api_name or
            not has_ts_code or is_batch):
            batch_apis.append(api)
        else:
            single_apis.append(api)
    
    return batch_apis, single_apis

def main():
    # 读取URL列表
    with open('D:\\stock_system\\tushare网页.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有URL
    urls = re.findall(r'https://tushare\.pro/document/2\?doc_id=\d+', content)
    
    print(f"找到 {len(urls)} 个API文档链接")
    
    # 获取所有API信息
    apis = []
    for i, url in enumerate(urls):
        print(f"正在处理 {i+1}/{len(urls)}: {url}")
        api_info = get_api_info(url)
        if api_info:
            apis.append(api_info)
        time.sleep(1)  # 避免请求过快
    
    # 分类API
    batch_apis, single_apis = classify_apis(apis)
    
    # 保存结果
    result = {
        '可以批量获取的数据': [
            {
                'api_name': api['api_name'],
                'url': api['url'],
                'parameters': [p['name'] for p in api['parameters']]
            } for api in batch_apis
        ],
        '单只股票逐条获取的数据': [
            {
                'api_name': api['api_name'],
                'url': api['url'],
                'parameters': [p['name'] for p in api['parameters']]
            } for api in single_apis
        ]
    }
    
    with open('D:\\stock_system\\tushare_api_classification.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n分类完成:")
    print(f"可以批量获取的数据: {len(batch_apis)} 个接口")
    print(f"单只股票逐条获取的数据: {len(single_apis)} 个接口")
    print("结果已保存到 tushare_api_classification.json")

if __name__ == "__main__":
    main()