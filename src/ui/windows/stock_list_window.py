#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票列表窗口 - 显示股票基本信息和数据管理
"""

import os
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QProgressBar, QLabel, QLineEdit, QComboBox,
                             QMessageBox, QGroupBox, QFormLayout, QTextEdit,
                             QSplitter, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

class DataInitThread(QThread):
    """数据初始化线程"""
    progress_updated = pyqtSignal(int, str)  # 进度, 消息
    finished_signal = pyqtSignal(bool, str)  # 成功/失败, 消息
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        """执行数据初始化"""
        try:
            self.progress_updated.emit(10, "正在连接数据源...")
            
            # 加载token配置
            token_config = self.load_token_config()
            if not token_config:
                self.finished_signal.emit(False, "未找到Token配置，请先设置Token")
                return
                
            # 导入对应的库
            if token_config['token_type'] == 'tudata':
                import tudata as ts
            else:
                import tushare as ts
                
            ts.set_token(token_config['token'])
            pro = ts.pro_api()
            
            self.progress_updated.emit(20, "正在创建数据库...")
            
            # 创建数据库
            self.create_database()
            
            self.progress_updated.emit(30, "正在获取股票列表...")
            
            # 获取股票基本信息
            stock_basic = pro.stock_basic(exchange='', list_status='L',
                                        fields='ts_code,symbol,name,area,industry,market,list_date')
            
            self.progress_updated.emit(50, f"正在保存股票数据 ({len(stock_basic)}条)...")
            
            # 保存到数据库
            self.save_stock_basic(stock_basic)
            
            self.progress_updated.emit(70, "正在获取交易日历...")
            
            # 获取交易日历
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            trade_cal = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
            
            self.progress_updated.emit(90, "正在保存交易日历...")
            
            # 保存交易日历
            self.save_trade_calendar(trade_cal)
            
            self.progress_updated.emit(100, "数据初始化完成")
            self.finished_signal.emit(True, f"成功初始化 {len(stock_basic)} 只股票数据")
            
        except Exception as e:
            self.finished_signal.emit(False, f"数据初始化失败: {str(e)}")
            
    def load_token_config(self):
        """加载token配置"""
        try:
            config_file = "config/token_config.txt"
            if not os.path.exists(config_file):
                return None
                
            config = {}
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
            return config
        except:
            return None
            
    def create_database(self):
        """创建数据库表"""
        db_dir = "database"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        conn = sqlite3.connect("database/stock_data.db")
        cursor = conn.cursor()
        
        # 创建股票基本信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_basic (
                ts_code TEXT PRIMARY KEY,
                symbol TEXT,
                name TEXT,
                area TEXT,
                industry TEXT,
                market TEXT,
                list_date TEXT,
                update_time TEXT
            )
        ''')
        
        # 创建交易日历表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_calendar (
                cal_date TEXT PRIMARY KEY,
                is_open INTEGER,
                pretrade_date TEXT
            )
        ''')
        
        # 创建日线行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_basic (
                ts_code TEXT,
                trade_date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                pre_close REAL,
                change REAL,
                pct_chg REAL,
                vol REAL,
                amount REAL,
                PRIMARY KEY (ts_code, trade_date)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def save_stock_basic(self, df):
        """保存股票基本信息"""
        conn = sqlite3.connect("database/stock_data.db")
        
        # 添加更新时间
        df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 保存数据
        df.to_sql('stock_basic', conn, if_exists='replace', index=False)
        
        conn.close()
        
    def save_trade_calendar(self, df):
        """保存交易日历"""
        conn = sqlite3.connect("database/stock_data.db")
        df.to_sql('trade_calendar', conn, if_exists='replace', index=False)
        conn.close()

class DataUpdateThread(QThread):
    """数据更新线程"""
    progress_updated = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        """执行数据更新"""
        try:
            self.progress_updated.emit(10, "检查数据库状态...")
            
            # 检查数据库是否存在
            if not os.path.exists("database/stock_data.db"):
                self.finished_signal.emit(False, "数据库不存在，请先进行数据初始化")
                return
                
            # 加载token配置
            token_config = self.load_token_config()
            if not token_config:
                self.finished_signal.emit(False, "未找到Token配置")
                return
                
            if token_config['token_type'] == 'tudata':
                import tudata as ts
            else:
                import tushare as ts
                
            ts.set_token(token_config['token'])
            pro = ts.pro_api()
            
            self.progress_updated.emit(30, "检查缺失的交易日...")
            
            # 获取最新的交易日历
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
            trade_cal = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
            
            self.progress_updated.emit(60, "更新交易日历...")
            
            # 更新交易日历
            conn = sqlite3.connect("database/stock_data.db")
            trade_cal.to_sql('trade_calendar', conn, if_exists='append', index=False)
            
            self.progress_updated.emit(80, "检查股票列表更新...")
            
            # 检查是否有新股上市
            stock_basic = pro.stock_basic(exchange='', list_status='L',
                                        fields='ts_code,symbol,name,area,industry,market,list_date')
            
            # 获取数据库中的股票数量
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM stock_basic")
            db_count = cursor.fetchone()[0]
            
            new_stocks = len(stock_basic) - db_count
            
            if new_stocks > 0:
                self.progress_updated.emit(90, f"发现 {new_stocks} 只新股，正在更新...")
                stock_basic['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                stock_basic.to_sql('stock_basic', conn, if_exists='replace', index=False)
            
            conn.close()
            
            self.progress_updated.emit(100, "数据更新完成")
            
            if new_stocks > 0:
                self.finished_signal.emit(True, f"更新完成，新增 {new_stocks} 只股票")
            else:
                self.finished_signal.emit(True, "数据已是最新，无需更新")
                
        except Exception as e:
            self.finished_signal.emit(False, f"数据更新失败: {str(e)}")
            
    def load_token_config(self):
        """加载token配置"""
        try:
            config_file = "config/token_config.txt"
            if not os.path.exists(config_file):
                return None
                
            config = {}
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
            return config
        except:
            return None

class StockListWindow(QWidget):
    """股票列表窗口"""
    
    stock_selected = pyqtSignal(str)  # 股票选择信号
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_stock_data()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧控制面板
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # 右侧股票列表
        list_panel = self.create_list_panel()
        splitter.addWidget(list_panel)
        
        # 设置分割比例
        splitter.setSizes([300, 800])
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 数据管理组
        data_group = QGroupBox("数据管理")
        data_layout = QVBoxLayout(data_group)
        
        # 数据初始化按钮
        self.init_button = QPushButton("数据初始化")
        self.init_button.clicked.connect(self.init_data)
        data_layout.addWidget(self.init_button)
        
        # 增量更新按钮
        self.update_button = QPushButton("增量更新")
        self.update_button.clicked.connect(self.update_data)
        data_layout.addWidget(self.update_button)
        
        # 刷新列表按钮
        self.refresh_button = QPushButton("刷新列表")
        self.refresh_button.clicked.connect(self.load_stock_data)
        data_layout.addWidget(self.refresh_button)
        
        layout.addWidget(data_group)
        
        # 筛选组
        filter_group = QGroupBox("筛选条件")
        filter_layout = QFormLayout(filter_group)
        
        # 市场筛选
        self.market_combo = QComboBox()
        self.market_combo.addItems(["全部", "主板", "创业板", "科创板"])
        self.market_combo.currentTextChanged.connect(self.filter_stocks)
        filter_layout.addRow("市场:", self.market_combo)
        
        # 行业筛选
        self.industry_combo = QComboBox()
        self.industry_combo.addItem("全部")
        self.industry_combo.currentTextChanged.connect(self.filter_stocks)
        filter_layout.addRow("行业:", self.industry_combo)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入股票代码或名称")
        self.search_input.textChanged.connect(self.filter_stocks)
        filter_layout.addRow("搜索:", self.search_input)
        
        layout.addWidget(filter_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态信息
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        layout.addStretch()
        return panel
        
    def create_list_panel(self):
        """创建列表面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 标题
        title_label = QLabel("股票列表")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # 股票表格
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(7)
        self.stock_table.setHorizontalHeaderLabels([
            "股票代码", "股票简称", "所属市场", "所属行业", "地区", "上市日期", "更新时间"
        ])
        
        # 设置表格属性
        self.stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.setSortingEnabled(True)
        
        # 设置列宽
        header = self.stock_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        
        self.stock_table.setColumnWidth(0, 100)
        self.stock_table.setColumnWidth(1, 120)
        self.stock_table.setColumnWidth(2, 80)
        self.stock_table.setColumnWidth(4, 80)
        self.stock_table.setColumnWidth(5, 100)
        self.stock_table.setColumnWidth(6, 150)
        
        # 双击事件
        self.stock_table.itemDoubleClicked.connect(self.on_stock_double_clicked)
        
        layout.addWidget(self.stock_table)
        
        # 统计信息
        self.stats_label = QLabel("总计: 0 只股票")
        layout.addWidget(self.stats_label)
        
        return panel
        
    def init_data(self):
        """数据初始化"""
        reply = QMessageBox.question(self, '确认', 
                                   '数据初始化将重新下载所有基础数据，可能需要较长时间。\n确定要继续吗？',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
            
        # 禁用按钮
        self.init_button.setEnabled(False)
        self.update_button.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 清空状态
        self.status_text.clear()
        self.status_text.append("开始数据初始化...")
        
        # 启动初始化线程
        self.init_thread = DataInitThread()
        self.init_thread.progress_updated.connect(self.on_progress_updated)
        self.init_thread.finished_signal.connect(self.on_init_finished)
        self.init_thread.start()
        
    def update_data(self):
        """增量数据更新"""
        # 禁用按钮
        self.init_button.setEnabled(False)
        self.update_button.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 清空状态
        self.status_text.clear()
        self.status_text.append("开始增量更新...")
        
        # 启动更新线程
        self.update_thread = DataUpdateThread()
        self.update_thread.progress_updated.connect(self.on_progress_updated)
        self.update_thread.finished_signal.connect(self.on_update_finished)
        self.update_thread.start()
        
    def on_progress_updated(self, progress, message):
        """进度更新"""
        self.progress_bar.setValue(progress)
        self.status_text.append(f"[{progress}%] {message}")
        
    def on_init_finished(self, success, message):
        """初始化完成"""
        self.progress_bar.setVisible(False)
        self.init_button.setEnabled(True)
        self.update_button.setEnabled(True)
        
        self.status_text.append(f"\n初始化结果: {message}")
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.load_stock_data()
        else:
            QMessageBox.critical(self, "失败", message)
            
    def on_update_finished(self, success, message):
        """更新完成"""
        self.progress_bar.setVisible(False)
        self.init_button.setEnabled(True)
        self.update_button.setEnabled(True)
        
        self.status_text.append(f"\n更新结果: {message}")
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.load_stock_data()
        else:
            QMessageBox.critical(self, "失败", message)
            
    def load_stock_data(self):
        """加载股票数据"""
        try:
            if not os.path.exists("database/stock_data.db"):
                self.status_text.append("数据库不存在，请先进行数据初始化")
                return
                
            conn = sqlite3.connect("database/stock_data.db")
            cursor = conn.cursor()
            
            # 查询股票数据
            cursor.execute("""
                SELECT ts_code, name, market, industry, area, list_date, update_time
                FROM stock_basic
                ORDER BY ts_code
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            # 更新表格
            self.stock_table.setRowCount(len(rows))
            
            # 收集行业信息
            industries = set()
            
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value) if value else "")
                    self.stock_table.setItem(i, j, item)
                    
                # 收集行业
                if row[3]:  # industry
                    industries.add(row[3])
                    
            # 更新行业下拉框
            current_industry = self.industry_combo.currentText()
            self.industry_combo.clear()
            self.industry_combo.addItem("全部")
            self.industry_combo.addItems(sorted(industries))
            
            # 恢复选择
            index = self.industry_combo.findText(current_industry)
            if index >= 0:
                self.industry_combo.setCurrentIndex(index)
                
            # 更新统计信息
            self.stats_label.setText(f"总计: {len(rows)} 只股票")
            
            self.status_text.append(f"成功加载 {len(rows)} 只股票数据")
            
        except Exception as e:
            self.status_text.append(f"加载数据失败: {str(e)}")
            
    def filter_stocks(self):
        """筛选股票"""
        market_filter = self.market_combo.currentText()
        industry_filter = self.industry_combo.currentText()
        search_text = self.search_input.text().strip().upper()
        
        visible_count = 0
        
        for row in range(self.stock_table.rowCount()):
            show_row = True
            
            # 市场筛选
            if market_filter != "全部":
                market_item = self.stock_table.item(row, 2)
                if market_item and market_filter not in market_item.text():
                    show_row = False
                    
            # 行业筛选
            if show_row and industry_filter != "全部":
                industry_item = self.stock_table.item(row, 3)
                if industry_item and industry_filter != industry_item.text():
                    show_row = False
                    
            # 搜索筛选
            if show_row and search_text:
                code_item = self.stock_table.item(row, 0)
                name_item = self.stock_table.item(row, 1)
                
                code_match = code_item and search_text in code_item.text().upper()
                name_match = name_item and search_text in name_item.text().upper()
                
                if not (code_match or name_match):
                    show_row = False
                    
            self.stock_table.setRowHidden(row, not show_row)
            if show_row:
                visible_count += 1
                
        # 更新统计信息
        total_count = self.stock_table.rowCount()
        self.stats_label.setText(f"显示: {visible_count} / {total_count} 只股票")
        
    def on_stock_double_clicked(self, item):
        """股票双击事件"""
        row = item.row()
        code_item = self.stock_table.item(row, 0)
        if code_item:
            stock_code = code_item.text()
            self.stock_selected.emit(stock_code)