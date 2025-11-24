#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能增量更新器 - 基于数据完整性检测的精准更新
"""

import sqlite3
import pandas as pd
import tushare as ts
from datetime import datetime, timedelta
from .database_manager import DatabaseManager

class IncrementalUpdater:
    """智能增量更新器"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.pro = ts.pro_api()  # 初始化tushare pro接口
        
    def update_date_data_with_override(self, table_name, trade_date, update_type='full'):
        """
        更新指定日期数据并覆盖已有数据
        
        Args:
            table_name: 表名
            trade_date: 交易日期
            update_type: 更新类型 ('full', 'partial', 'missing_only')
        """
        
        if update_type == 'full':
            # 全量覆盖：删除该日期所有数据后重新插入
            return self._full_date_override(table_name, trade_date)
        elif update_type == 'partial':
            # 部分覆盖：只覆盖指定股票的数据
            return self._partial_date_override(table_name, trade_date)
        elif update_type == 'missing_only':
            # 补充模式：只添加缺失的股票数据
            return self._missing_only_update(table_name, trade_date)
    
    def _full_date_override(self, table_name, trade_date):
        """
        全量覆盖指定日期的数据
        策略：DELETE + INSERT，确保数据完全覆盖
        """
        conn = None
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # 1. 开始事务
            conn.execute("BEGIN TRANSACTION")
            
            # 2. 删除该日期的所有数据
            delete_sql = f"DELETE FROM {table_name} WHERE trade_date = ?"
            cursor.execute(delete_sql, (trade_date,))
            deleted_count = cursor.rowcount
            print(f"🗑️ 删除 {table_name} {trade_date} 的 {deleted_count} 条旧数据")
            
            # 3. 获取新数据
            if table_name == 'daily_basic':
                df = self.pro.daily(trade_date=trade_date)
            elif table_name == 'index_daily':
                df = self.pro.index_daily(trade_date=trade_date)
            else:
                raise ValueError(f"不支持的表名: {table_name}")
            
            # 4. 插入新数据
            if not df.empty:
                df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                df['src'] = 'incremental_override'  # 标记数据源
                
                # 使用to_sql直接插入，确保完全覆盖
                df.to_sql(table_name, conn, if_exists='append', index=False)
                records = len(df)
                
                # 5. 提交事务
                conn.commit()
                print(f"✅ 全量覆盖成功：删除{deleted_count}条，新增{records}条")
                return True, records, f"全量覆盖成功：删除{deleted_count}条，新增{records}条"
            else:
                conn.rollback()
                return False, 0, "API返回空数据，回滚事务"
                
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"❌ 全量覆盖失败，已回滚: {str(e)}")
            return False, 0, f"全量覆盖失败: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def _partial_date_override(self, table_name, trade_date, target_stocks=None):
        """
        部分覆盖指定股票的数据
        策略：DELETE WHERE + INSERT，只覆盖指定股票
        """
        conn = None
        try:
            if target_stocks is None:
                # 如果未指定股票，则找出需要更新的股票
                target_stocks = self._find_problematic_stocks(table_name, trade_date)
            
            if not target_stocks:
                return True, 0, "无需更新的股票"
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # 1. 开始事务
            conn.execute("BEGIN TRANSACTION")
            
            # 2. 删除指定股票在该日期的数据
            placeholders = ','.join(['?' for _ in target_stocks])
            delete_sql = f"DELETE FROM {table_name} WHERE trade_date = ? AND ts_code IN ({placeholders})"
            cursor.execute(delete_sql, [trade_date] + target_stocks)
            deleted_count = cursor.rowcount
            print(f"🗑️ 删除 {len(target_stocks)} 只股票在 {trade_date} 的 {deleted_count} 条数据")
            
            # 3. 批量获取新数据
            all_new_data = []
            for ts_code in target_stocks:
                if table_name == 'daily_basic':
                    df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
                elif table_name == 'index_daily':
                    df = self.pro.index_daily(ts_code=ts_code, trade_date=trade_date)
                
                if not df.empty:
                    df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    df['src'] = 'incremental_partial'
                    all_new_data.append(df)
            
            # 4. 批量插入新数据
            if all_new_data:
                combined_df = pd.concat(all_new_data, ignore_index=True)
                combined_df.to_sql(table_name, conn, if_exists='append', index=False)
                updated_records = len(combined_df)
                
                conn.commit()
                print(f"✅ 部分覆盖成功：删除{deleted_count}条，新增{updated_records}条")
                return True, updated_records, f"部分覆盖成功：删除{deleted_count}条，新增{updated_records}条"
            else:
                conn.rollback()
                return False, 0, "未获取到新数据，回滚事务"
            
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"❌ 部分覆盖失败，已回滚: {str(e)}")
            return False, 0, f"部分覆盖失败: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def _missing_only_update(self, table_name, trade_date):
        """
        只补充缺失的股票数据
        策略：INSERT OR IGNORE，保留已有数据，只添加缺失数据
        """
        conn = None
        try:
            # 1. 找出缺失的股票
            missing_stocks = self._find_missing_stocks(table_name, trade_date)
            
            if not missing_stocks:
                return True, 0, "无缺失数据"
            
            print(f"📝 需要补充 {len(missing_stocks)} 只股票的数据")
            
            conn = self.db_manager.get_connection()
            conn.execute("BEGIN TRANSACTION")
            
            # 2. 批量获取缺失股票的数据
            all_new_data = []
            for ts_code in missing_stocks:
                if table_name == 'daily_basic':
                    df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
                elif table_name == 'index_daily':
                    df = self.pro.index_daily(ts_code=ts_code, trade_date=trade_date)
                
                if not df.empty:
                    df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    df['src'] = 'incremental_missing'
                    all_new_data.append(df)
            
            # 3. 批量插入新数据（使用INSERT OR IGNORE避免冲突）
            if all_new_data:
                combined_df = pd.concat(all_new_data, ignore_index=True)
                # 使用INSERT OR IGNORE策略
                combined_df.to_sql(f"{table_name}_temp", conn, if_exists='replace', index=False)
                
                # 执行INSERT OR IGNORE
                columns = ', '.join(combined_df.columns)
                placeholders = ', '.join(['?' for _ in combined_df.columns])
                insert_sql = f"""
                    INSERT OR IGNORE INTO {table_name} ({columns})
                    SELECT {columns} FROM {table_name}_temp
                """
                cursor = conn.cursor()
                cursor.execute(insert_sql)
                updated_records = cursor.rowcount
                
                # 清理临时表
                cursor.execute(f"DROP TABLE {table_name}_temp")
                
                conn.commit()
                print(f"✅ 补充缺失数据成功：新增{updated_records}条")
                return True, updated_records, f"补充缺失数据成功：新增{updated_records}条"
            else:
                conn.rollback()
                return True, 0, "未获取到新数据"
            
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"❌ 补充数据失败，已回滚: {str(e)}")
            return False, 0, f"补充数据失败: {str(e)}"
        finally:
            if conn:
                conn.close()
    
    def _find_missing_stocks(self, table_name, trade_date):
        """找出指定日期缺失数据的股票"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # 获取所有活跃股票
            cursor.execute("""
                SELECT ts_code FROM stock_basic 
                WHERE list_date <= ? 
                AND (delist_date IS NULL OR delist_date > ?)
            """, (trade_date, trade_date))
            all_stocks = [row[0] for row in cursor.fetchall()]
            
            # 获取已有数据的股票
            cursor.execute(f"""
                SELECT DISTINCT ts_code FROM {table_name} 
                WHERE trade_date = ?
            """, (trade_date,))
            existing_stocks = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            
            # 计算缺失的股票
            missing_stocks = list(set(all_stocks) - set(existing_stocks))
            return missing_stocks
            
        except Exception as e:
            print(f"查找缺失股票失败: {e}")
            if conn:
                conn.close()
            return []
    
    def _find_problematic_stocks(self, table_name, trade_date):
        """找出数据有问题需要重新获取的股票"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            # 查找数据异常的股票（如价格为0、成交量异常等）
            if table_name == 'daily_basic':
                cursor.execute(f"""
                    SELECT ts_code FROM {table_name} 
                    WHERE trade_date = ? 
                    AND (close <= 0 OR vol < 0 OR amount < 0 OR close IS NULL)
                """, (trade_date,))
            else:
                cursor.execute(f"""
                    SELECT ts_code FROM {table_name} 
                    WHERE trade_date = ? 
                    AND (close <= 0 OR close IS NULL)
                """, (trade_date,))
            
            problematic_stocks = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return problematic_stocks
            
        except Exception as e:
            print(f"查找问题股票失败: {e}")
            if conn:
                conn.close()
            return []

    def smart_update_decision(self, table_name, trade_date):
        """
        智能决策更新策略
        """
        # 1. 检查数据完整性
        missing_stocks = self._find_missing_stocks(table_name, trade_date)
        problematic_stocks = self._find_problematic_stocks(table_name, trade_date)
        
        # 2. 计算缺失率
        total_expected = len(self._get_active_stocks(trade_date))
        missing_rate = len(missing_stocks) / total_expected if total_expected > 0 else 0
        problem_rate = len(problematic_stocks) / total_expected if total_expected > 0 else 0
        
        # 3. 决策更新策略
        if missing_rate > 0.2 or problem_rate > 0.1:
            # 缺失率或问题率过高，全量更新
            return 'full', f"缺失率{missing_rate:.1%}，问题率{problem_rate:.1%}，建议全量更新"
        elif missing_stocks or problematic_stocks:
            # 有缺失或问题数据，部分更新
            target_stocks = list(set(missing_stocks + problematic_stocks))
            return 'partial', f"需要更新{len(target_stocks)}只股票"
        else:
            # 数据完整，无需更新
            return 'none', "数据完整，无需更新"
    
    def _get_active_stocks(self, trade_date):
        """获取指定日期的活跃股票列表"""
        try:
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ts_code FROM stock_basic 
                WHERE list_date <= ? 
                AND (delist_date IS NULL OR delist_date > ?)
            """, (trade_date, trade_date))
            
            stocks = [row[0] for row in cursor.fetchall()]
            conn.close()
            return stocks
            
        except Exception as e:
            print(f"获取活跃股票失败: {e}")
            return []
    
    def ensure_data_override(self, table_name, trade_date, force_override=False):
        """
        确保当日数据可以被覆盖的主入口方法
        
        Args:
            table_name: 表名
            trade_date: 交易日期
            force_override: 是否强制覆盖（忽略数据质量检查）
        
        Returns:
            tuple: (success, records, message)
        """
        print(f"🔍 检查 {table_name} {trade_date} 的数据覆盖需求...")
        
        if force_override:
            print("⚠️ 强制覆盖模式，将全量更新数据")
            return self._full_date_override(table_name, trade_date)
        
        # 智能决策更新策略
        update_type, reason = self.smart_update_decision(table_name, trade_date)
        print(f"📋 更新策略: {update_type} - {reason}")
        
        if update_type == 'full':
            return self._full_date_override(table_name, trade_date)
        elif update_type == 'partial':
            return self._partial_date_override(table_name, trade_date)
        elif update_type == 'none':
            return True, 0, reason
        else:
            return self._missing_only_update(table_name, trade_date)