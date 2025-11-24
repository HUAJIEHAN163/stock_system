#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有测试
"""

import sys
import os
import subprocess

def run_test(test_file):
    """运行单个测试文件"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, encoding='utf-8')
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"PASS {test_file}")
            return True
        else:
            print(f"FAIL {test_file} (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"ERROR {test_file}: {e}")
        return False

def main():
    """主函数"""
    print("Stock System - Test Suite")
    print("=" * 60)
    
    # 测试文件列表
    test_files = [
        'tests/test_database.py',
        'tests/test_api_config.py', 
        'tests/test_data_init.py'
    ]
    
    results = []
    
    # 运行所有测试
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test(test_file)
            results.append((test_file, success))
        else:
            print(f"NOT FOUND {test_file}")
            results.append((test_file, False))
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    failed = 0
    
    for test_file, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{status:8} {test_file}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\nAll tests passed!")
        return 0
    else:
        print(f"\n{failed} test(s) failed")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)