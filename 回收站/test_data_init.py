#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据初始化功能
"""

import sys
import os
import logging

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.data.data_initializer import DataInitializer

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger('TestDataInit')

def load_token_config():
    """加载token配置"""
    try:
        config_file = "config/token_config.txt"
        if not os.path.exists(config_file):
            return None
            
        config = {}
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except Exception as e:
        print(f"加载token配置失败: {e}")
        return None

def test_api_connection():
    """测试API连接"""
    logger = setup_logging()
    
    logger.info("开始测试API连接...")
    
    # 加载token配置
    token_config = load_token_config()
    if not token_config:
        logger.error("未找到token配置")
        return False
    
    logger.info(f"Token配置: {list(token_config.keys())}")
    
    try:
        if token_config.get('token_type') == 'tudata':
            try:
                import tudata as ts
                logger.info("使用tudata库")
            except ImportError:
                logger.warning("tudata库未安装，使用tushare库")
                import tushare as ts
        else:
            import tushare as ts
            logger.info("使用tushare库")
        
        ts.set_token(token_config['token'])
        pro = ts.pro_api()
        
        # 测试连接
        logger.info("测试API连接...")
        test_df = pro.stock_basic(exchange='', list_status='L', limit=5)
        
        if len(test_df) > 0:
            logger.info(f"API连接成功，获取到 {len(test_df)} 条测试数据")
            logger.info(f"测试数据列: {list(test_df.columns)}")
            return True
        else:
            logger.error("API返回空数据")
            return False
            
    except Exception as e:
        logger.error(f"API连接失败: {e}")
        return False

def test_data_initializer():
    """测试数据初始化器"""
    logger = setup_logging()
    
    logger.info("开始测试数据初始化器...")
    
    # 加载token配置
    token_config = load_token_config()
    if not token_config:
        logger.error("未找到token配置")
        return False
    
    # 创建数据初始化器
    initializer = DataInitializer(['batch_1'], token_config)
    
    # 测试API连接初始化
    if initializer._init_api_connection():
        logger.info("数据初始化器API连接成功")
        return True
    else:
        logger.error("数据初始化器API连接失败")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("数据初始化功能测试")
    print("=" * 60)
    
    # 测试1: API连接
    print("\n1. 测试API连接...")
    if test_api_connection():
        print("[成功] API连接测试通过")
    else:
        print("[失败] API连接测试失败")
        return
    
    # 测试2: 数据初始化器
    print("\n2. 测试数据初始化器...")
    if test_data_initializer():
        print("[成功] 数据初始化器测试通过")
    else:
        print("[失败] 数据初始化器测试失败")
        return
    
    print("\n" + "=" * 60)
    print("所有测试通过！数据初始化功能正常")
    print("=" * 60)

if __name__ == '__main__':
    main()