#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新分类文档中的链接路径
"""

import re

def update_classification_links():
    """更新分类文档中的链接"""
    file_path = "doc/数据调查/数据准备/00_tushare_api_classification.md"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 将所有 docs/ 路径替换为相对路径
        updated_content = re.sub(r'docs/(\d+_[^)]+\.md)', r'\1', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("分类文档链接更新完成")
        
    except Exception as e:
        print(f"更新失败: {e}")

if __name__ == '__main__':
    update_classification_links()