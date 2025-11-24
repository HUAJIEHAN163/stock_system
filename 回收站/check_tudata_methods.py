#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查tudata中可用的方法
"""

import tudata as ts

# 设置token
with open('doc/数据调查/token.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.strip().split('\n')
    token = lines[1].strip() if len(lines) > 1 else lines[0].strip()

ts.set_token(token)
pro = ts.pro_api()

print("tudata pro_api 可用方法:")
methods = [method for method in dir(pro) if not method.startswith('_')]
print(f"总方法数: {len(methods)}")

# 查找包含mins的方法
mins_methods = [method for method in methods if 'min' in method.lower()]
print(f"\n包含'min'的方法:")
for method in mins_methods:
    print(f"  {method}")

# 查找包含stk的方法
stk_methods = [method for method in methods if 'stk' in method.lower()]
print(f"\n包含'stk'的方法:")
for method in stk_methods:
    print(f"  {method}")

# 查找可能的分钟数据方法
possible_methods = [method for method in methods if any(keyword in method.lower() for keyword in ['min', 'tick', 'intra'])]
print(f"\n可能的分钟/tick数据方法:")
for method in possible_methods:
    print(f"  {method}")