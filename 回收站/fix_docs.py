#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复API文档内容错误
"""

import os
import re
import requests
from bs4 import BeautifulSoup
import time

def get_correct_api_content(doc_id):
    """获取正确的API文档内容"""
    url = f"https://tushare.pro/document/2?doc_id={doc_id}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text().strip() if title_elem else f"API_{doc_id}"
            
            # 提取主要内容
            content_div = soup.find('div', class_='content') or soup.find('div', class_='main')
            if content_div:
                content = content_div.get_text().strip()
            else:
                content = f"无法获取doc_id={doc_id}的详细内容"
            
            return title, content
        else:
            return None, None
            
    except Exception as e:
        print(f"获取doc_id={doc_id}失败: {e}")
        return None, None

def fix_document(filepath, doc_id):
    """修复单个文档"""
    print(f"修复文档: {os.path.basename(filepath)} (doc_id={doc_id})")
    
    # 获取正确内容
    title, content = get_correct_api_content(doc_id)
    
    if title and content:
        # 生成新的文档内容
        new_content = f"""# {title}

**接口地址**: https://tushare.pro/document/2?doc_id={doc_id}

{content}

---
**API状态**: 待测试  
**测试日期**: 待更新  
**测试结果**: 待测试  
**数据量**: 待测试  
"""
        
        # 写入文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ 修复成功")
            return True
        except Exception as e:
            print(f"  ✗ 写入失败: {e}")
            return False
    else:
        print(f"  ✗ 无法获取内容")
        return False

def fix_all_documents():
    """修复所有文档"""
    doc_dir = "doc/数据调查/数据准备"
    if not os.path.exists(doc_dir):
        print("文档目录不存在")
        return
    
    # 只修复几个关键的申万行业相关文档
    target_files = [
        "296_申万行业分类.md",
        "317_申万行业一级指数.md", 
        "320_申万行业分类.md",
        "321_申万行业成分.md"
    ]
    
    for filename in target_files:
        filepath = os.path.join(doc_dir, filename)
        if os.path.exists(filepath):
            # 提取doc_id
            match = re.match(r'(\d+)_', filename)
            if match:
                doc_id = match.group(1)
                fix_document(filepath, doc_id)
                time.sleep(2)  # 避免请求过快
        else:
            print(f"文件不存在: {filename}")

if __name__ == '__main__':
    print("开始修复API文档...")
    fix_all_documents()
    print("修复完成")