#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API文档正确性
"""

import os
import re
import requests
from bs4 import BeautifulSoup

def extract_doc_id_from_filename(filename):
    """从文件名提取doc_id"""
    match = re.match(r'(\d+)_', filename)
    return match.group(1) if match else None

def extract_doc_id_from_content(content):
    """从内容提取doc_id"""
    match = re.search(r'doc_id=(\d+)', content)
    return match.group(1) if match else None

def extract_api_name_from_content(content):
    """从内容提取API名称"""
    # 查找接口：xxx 模式
    match = re.search(r'接口：(\w+)', content)
    return match.group(1) if match else None

def check_document_consistency():
    """检查文档一致性"""
    doc_dir = "doc/数据调查/数据准备"
    if not os.path.exists(doc_dir):
        print("文档目录不存在")
        return
    
    errors = []
    
    for filename in os.listdir(doc_dir):
        if not filename.endswith('.md') or filename.startswith('00_'):
            continue
            
        filepath = os.path.join(doc_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件名中的doc_id
            filename_doc_id = extract_doc_id_from_filename(filename)
            
            # 提取内容中的doc_id
            content_doc_id = extract_doc_id_from_content(content)
            
            # 提取API名称
            api_name = extract_api_name_from_content(content)
            
            # 检查doc_id一致性
            if filename_doc_id != content_doc_id:
                errors.append({
                    'file': filename,
                    'type': 'doc_id_mismatch',
                    'filename_id': filename_doc_id,
                    'content_id': content_doc_id,
                    'api_name': api_name
                })
            
            # 检查标题是否合理
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "无标题"
            
            print(f"文件: {filename}")
            print(f"  文件名ID: {filename_doc_id}")
            print(f"  内容ID: {content_doc_id}")
            print(f"  API名称: {api_name}")
            print(f"  标题: {title}")
            print(f"  状态: {'❌ 不匹配' if filename_doc_id != content_doc_id else '✅ 匹配'}")
            print()
            
        except Exception as e:
            errors.append({
                'file': filename,
                'type': 'read_error',
                'error': str(e)
            })
    
    # 输出错误汇总
    if errors:
        print("=" * 60)
        print("发现的问题:")
        for error in errors:
            if error['type'] == 'doc_id_mismatch':
                print(f"❌ {error['file']}: 文件名ID({error['filename_id']}) != 内容ID({error['content_id']})")
                print(f"   API: {error['api_name']}")
            elif error['type'] == 'read_error':
                print(f"❌ {error['file']}: 读取错误 - {error['error']}")
    else:
        print("✅ 所有文档检查通过")

if __name__ == '__main__':
    check_document_consistency()