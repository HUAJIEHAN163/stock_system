#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时监控窗口 - 股价监控和预警功能
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLabel, QLineEdit, QComboBox, QGroupBox,
                             QFormLayout, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QSplitter, QFrame, QTabWidget,
                             QTextEdit, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class MonitorWindow(QWidget):
    """实时监控窗口"""
    
    stock_selected = pyqtSignal(str)  # 股票选择信号
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_timer()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("实时监控")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 自选股监控选项卡
        watchlist_tab = self.create_watchlist_tab()
        tab_widget.addTab(watchlist_tab, "📊 自选股监控")
        
        # 预警设置选项卡
        alert_tab = self.create_alert_tab()
        tab_widget.addTab(alert_tab, "🔔 预警设置")
        
        # 市场概况选项卡
        market_tab = self.create_market_tab()
        tab_widget.addTab(market_tab, "📈 市场概况")
        
        # 资金流向选项卡
        flow_tab = self.create_flow_tab()
        tab_widget.addTab(flow_tab, "💰 资金流向")
        
    def create_watchlist_tab(self):
        """创建自选股监控选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 控制面板
        control_panel = QFrame()
        control_panel.setMaximumHeight(60)
        control_layout = QHBoxLayout(control_panel)
        
        # 添加股票
        self.add_stock_input = QLineEdit()
        self.add_stock_input.setPlaceholderText("输入股票代码")
        control_layout.addWidget(QLabel("添加股票:"))
        control_layout.addWidget(self.add_stock_input)
        
        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_to_watchlist)
        control_layout.addWidget(self.add_button)
        
        control_layout.addStretch()
        
        # 刷新按钮
        self.refresh_button = QPushButton("刷新数据")
        self.refresh_button.clicked.connect(self.refresh_watchlist)
        control_layout.addWidget(self.refresh_button)
        
        # 自动刷新
        self.auto_refresh_check = QCheckBox("自动刷新(30秒)")
        self.auto_refresh_check.stateChanged.connect(self.toggle_auto_refresh)
        control_layout.addWidget(self.auto_refresh_check)
        
        layout.addWidget(control_panel)
        
        # 自选股表格
        self.watchlist_table = QTableWidget()
        self.watchlist_table.setColumnCount(10)
        self.watchlist_table.setHorizontalHeaderLabels([
            "股票代码", "股票名称", "最新价", "涨跌额", "涨跌幅", 
            "开盘价", "最高价", "最低价", "成交量", "操作"
        ])
        
        # 设置表格属性
        self.watchlist_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.watchlist_table.setAlternatingRowColors(True)
        
        # 设置列宽
        header = self.watchlist_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # 双击事件
        self.watchlist_table.itemDoubleClicked.connect(self.on_watchlist_double_clicked)
        
        layout.addWidget(self.watchlist_table)
        
        # 加载示例数据
        self.load_sample_watchlist()
        
        return widget
        
    def create_alert_tab(self):
        """创建预警设置选项卡"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # 左侧预警设置
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        # 预警设置组
        alert_group = QGroupBox("新增预警")
        alert_layout = QFormLayout(alert_group)
        
        # 股票选择
        self.alert_stock_input = QLineEdit()
        self.alert_stock_input.setPlaceholderText("输入股票代码")
        alert_layout.addRow("股票代码:", self.alert_stock_input)
        
        # 预警类型
        self.alert_type_combo = QComboBox()
        self.alert_type_combo.addItems(["价格预警", "涨跌幅预警", "成交量预警", "技术指标预警"])
        alert_layout.addRow("预警类型:", self.alert_type_combo)
        
        # 预警条件
        condition_layout = QHBoxLayout()
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["大于", "小于", "等于", "大于等于", "小于等于"])
        self.condition_value = QDoubleSpinBox()
        self.condition_value.setRange(0, 99999)
        self.condition_value.setDecimals(2)
        
        condition_layout.addWidget(self.condition_combo)
        condition_layout.addWidget(self.condition_value)
        alert_layout.addRow("预警条件:", condition_layout)
        
        # 预警方式
        self.alert_method_combo = QComboBox()
        self.alert_method_combo.addItems(["弹窗提醒", "声音提醒", "邮件提醒", "短信提醒"])
        alert_layout.addRow("预警方式:", self.alert_method_combo)
        
        # 添加按钮
        self.add_alert_button = QPushButton("添加预警")
        self.add_alert_button.clicked.connect(self.add_alert)
        alert_layout.addRow("", self.add_alert_button)
        
        left_layout.addWidget(alert_group)
        left_layout.addStretch()
        
        layout.addWidget(left_panel)
        
        # 右侧预警列表
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        # 预警列表标题
        list_label = QLabel("预警列表")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(list_label)
        
        # 预警列表表格
        self.alert_table = QTableWidget()
        self.alert_table.setColumnCount(6)
        self.alert_table.setHorizontalHeaderLabels([
            "股票代码", "预警类型", "预警条件", "当前值", "状态", "操作"
        ])
        
        # 设置表格属性
        self.alert_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.alert_table.setAlternatingRowColors(True)
        
        right_layout.addWidget(self.alert_table)
        
        # 预警历史
        history_label = QLabel("预警历史")
        history_label.setFont(QFont("Arial", 10, QFont.Bold))
        right_layout.addWidget(history_label)
        
        self.alert_history = QTextEdit()
        self.alert_history.setMaximumHeight(150)
        self.alert_history.setReadOnly(True)
        right_layout.addWidget(self.alert_history)
        
        layout.addWidget(right_panel)
        
        # 设置分割比例
        layout.setStretch(0, 1)
        layout.setStretch(1, 2)
        
        return widget
        
    def create_market_tab(self):
        """创建市场概况选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 市场指数面板
        index_panel = QFrame()
        index_panel.setFrameStyle(QFrame.StyledPanel)
        index_panel.setMaximumHeight(120)
        index_layout = QHBoxLayout(index_panel)
        
        # 主要指数
        indices = [
            ("上证指数", "3000.00", "+15.20", "+0.51%"),
            ("深证成指", "9500.00", "-25.30", "-0.27%"),
            ("创业板指", "2100.00", "+8.50", "+0.41%"),
            ("科创50", "850.00", "+3.20", "+0.38%")
        ]
        
        for name, price, change, pct_change in indices:
            index_group = QGroupBox(name)
            index_group_layout = QVBoxLayout(index_group)
            
            price_label = QLabel(price)
            price_label.setFont(QFont("Arial", 16, QFont.Bold))
            price_label.setAlignment(Qt.AlignCenter)
            
            change_label = QLabel(f"{change} ({pct_change})")
            change_label.setAlignment(Qt.AlignCenter)
            
            # 设置颜色
            if change.startswith('+'):
                price_label.setStyleSheet("color: red;")
                change_label.setStyleSheet("color: red;")
            else:
                price_label.setStyleSheet("color: green;")
                change_label.setStyleSheet("color: green;")
                
            index_group_layout.addWidget(price_label)
            index_group_layout.addWidget(change_label)
            
            index_layout.addWidget(index_group)
            
        layout.addWidget(index_panel)
        
        # 市场统计
        stats_panel = QFrame()
        stats_panel.setFrameStyle(QFrame.StyledPanel)
        stats_layout = QHBoxLayout(stats_panel)
        
        # 涨跌统计
        updown_group = QGroupBox("涨跌统计")
        updown_layout = QFormLayout(updown_group)
        
        updown_layout.addRow("上涨家数:", QLabel("1250"))
        updown_layout.addRow("下跌家数:", QLabel("1180"))
        updown_layout.addRow("平盘家数:", QLabel("85"))
        updown_layout.addRow("涨停家数:", QLabel("25"))
        updown_layout.addRow("跌停家数:", QLabel("8"))
        
        stats_layout.addWidget(updown_group)
        
        # 资金统计
        money_group = QGroupBox("资金统计")
        money_layout = QFormLayout(money_group)
        
        money_layout.addRow("总成交额:", QLabel("8500亿"))
        money_layout.addRow("沪市成交:", QLabel("4200亿"))
        money_layout.addRow("深市成交:", QLabel("4300亿"))
        money_layout.addRow("北向资金:", QLabel("净流入25亿"))
        money_layout.addRow("南向资金:", QLabel("净流出8亿"))
        
        stats_layout.addWidget(money_group)
        
        # 板块统计
        sector_group = QGroupBox("板块涨幅榜")
        sector_layout = QVBoxLayout(sector_group)
        
        self.sector_table = QTableWidget()
        self.sector_table.setColumnCount(3)
        self.sector_table.setHorizontalHeaderLabels(["板块名称", "涨跌幅", "领涨股"])
        
        sector_data = [
            ["人工智能", "+3.25%", "科大讯飞"],
            ["新能源车", "+2.80%", "比亚迪"],
            ["医药生物", "+1.95%", "恒瑞医药"],
            ["银行", "-1.20%", "招商银行"],
            ["房地产", "-2.15%", "万科A"]
        ]
        
        self.sector_table.setRowCount(len(sector_data))
        for i, row_data in enumerate(sector_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                # 设置涨跌幅颜色
                if j == 1:
                    if value.startswith('+'):
                        item.setForeground(QColor('red'))
                    elif value.startswith('-'):
                        item.setForeground(QColor('green'))
                self.sector_table.setItem(i, j, item)
                
        sector_layout.addWidget(self.sector_table)
        stats_layout.addWidget(sector_group)
        
        layout.addWidget(stats_panel)
        
        return widget
        
    def create_flow_tab(self):
        """创建资金流向选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 资金流向概览
        overview_panel = QFrame()
        overview_panel.setFrameStyle(QFrame.StyledPanel)
        overview_panel.setMaximumHeight(100)
        overview_layout = QHBoxLayout(overview_panel)
        
        flow_items = [
            ("主力净流入", "+125.8亿", "red"),
            ("超大单净流入", "+85.2亿", "red"),
            ("大单净流入", "+40.6亿", "red"),
            ("中单净流出", "-65.3亿", "green"),
            ("小单净流出", "-60.5亿", "green")
        ]
        
        for name, value, color in flow_items:
            item_layout = QVBoxLayout()
            
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignCenter)
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Arial", 14, QFont.Bold))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet(f"color: {color};")
            
            item_layout.addWidget(name_label)
            item_layout.addWidget(value_label)
            
            overview_layout.addLayout(item_layout)
            
        layout.addWidget(overview_panel)
        
        # 个股资金流向排行
        ranking_label = QLabel("个股资金流向排行")
        ranking_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(ranking_label)
        
        # 创建选项卡
        ranking_tab = QTabWidget()
        layout.addWidget(ranking_tab)
        
        # 净流入排行
        inflow_tab = self.create_flow_ranking_table("净流入")
        ranking_tab.addTab(inflow_tab, "净流入排行")
        
        # 净流出排行
        outflow_tab = self.create_flow_ranking_table("净流出")
        ranking_tab.addTab(outflow_tab, "净流出排行")
        
        return widget
        
    def create_flow_ranking_table(self, flow_type):
        """创建资金流向排行表格"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "排名", "股票代码", "股票名称", "最新价", "涨跌幅", "主力净流入", "净流入占比"
        ])
        
        # 示例数据
        if flow_type == "净流入":
            sample_data = [
                ["1", "000001.SZ", "平安银行", "12.50", "+2.29%", "+5.2亿", "8.5%"],
                ["2", "600036.SH", "招商银行", "42.80", "+1.85%", "+4.8亿", "7.2%"],
                ["3", "000002.SZ", "万科A", "18.30", "+0.85%", "+3.5亿", "6.8%"],
            ]
        else:
            sample_data = [
                ["1", "600519.SH", "贵州茅台", "1680.00", "-2.15%", "-8.5亿", "-12.3%"],
                ["2", "000858.SZ", "五粮液", "158.50", "-1.80%", "-6.2亿", "-9.8%"],
                ["3", "002415.SZ", "海康威视", "35.20", "-1.25%", "-4.8亿", "-7.5%"],
            ]
            
        table.setRowCount(len(sample_data))
        for i, row_data in enumerate(sample_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                # 设置涨跌幅和资金流向颜色
                if j == 4:  # 涨跌幅
                    if value.startswith('+'):
                        item.setForeground(QColor('red'))
                    elif value.startswith('-'):
                        item.setForeground(QColor('green'))
                elif j in [5, 6]:  # 资金流向
                    if value.startswith('+'):
                        item.setForeground(QColor('red'))
                    elif value.startswith('-'):
                        item.setForeground(QColor('green'))
                table.setItem(i, j, item)
                
        # 设置表格属性
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        
        return table
        
    def init_timer(self):
        """初始化定时器"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_watchlist)
        
    def add_to_watchlist(self):
        """添加股票到自选股"""
        stock_code = self.add_stock_input.text().strip().upper()
        if not stock_code:
            return
            
        # TODO: 验证股票代码有效性
        
        # 添加到表格
        row_count = self.watchlist_table.rowCount()
        self.watchlist_table.insertRow(row_count)
        
        # 示例数据
        sample_data = [stock_code, "股票名称", "0.00", "0.00", "0.00%", "0.00", "0.00", "0.00", "0", "删除"]
        
        for j, value in enumerate(sample_data):
            item = QTableWidgetItem(str(value))
            self.watchlist_table.setItem(row_count, j, item)
            
        # 清空输入框
        self.add_stock_input.clear()
        
    def refresh_watchlist(self):
        """刷新自选股数据"""
        # TODO: 实现实时数据刷新
        pass
        
    def toggle_auto_refresh(self, state):
        """切换自动刷新"""
        if state == Qt.Checked:
            self.refresh_timer.start(30000)  # 30秒
        else:
            self.refresh_timer.stop()
            
    def add_alert(self):
        """添加预警"""
        stock_code = self.alert_stock_input.text().strip()
        alert_type = self.alert_type_combo.currentText()
        condition = self.condition_combo.currentText()
        value = self.condition_value.value()
        
        if not stock_code:
            return
            
        # 添加到预警表格
        row_count = self.alert_table.rowCount()
        self.alert_table.insertRow(row_count)
        
        alert_data = [
            stock_code,
            alert_type,
            f"{condition} {value}",
            "0.00",
            "监控中",
            "删除"
        ]
        
        for j, value in enumerate(alert_data):
            item = QTableWidgetItem(str(value))
            self.alert_table.setItem(row_count, j, item)
            
        # 清空输入
        self.alert_stock_input.clear()
        self.condition_value.setValue(0)
        
    def load_sample_watchlist(self):
        """加载示例自选股数据"""
        sample_data = [
            ["000001.SZ", "平安银行", "12.50", "+0.28", "+2.29%", "12.25", "12.58", "12.20", "15000", "删除"],
            ["600036.SH", "招商银行", "42.80", "+0.78", "+1.85%", "42.50", "43.20", "42.30", "8500", "删除"],
            ["000002.SZ", "万科A", "18.30", "-0.22", "-1.19%", "18.50", "18.60", "18.20", "12000", "删除"],
        ]
        
        self.watchlist_table.setRowCount(len(sample_data))
        for i, row_data in enumerate(sample_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                # 设置涨跌幅颜色
                if j == 4:  # 涨跌幅列
                    if value.startswith('+'):
                        item.setForeground(QColor('red'))
                    elif value.startswith('-'):
                        item.setForeground(QColor('green'))
                self.watchlist_table.setItem(i, j, item)
                
    def on_watchlist_double_clicked(self, item):
        """自选股双击事件"""
        row = item.row()
        code_item = self.watchlist_table.item(row, 0)
        if code_item:
            stock_code = code_item.text()
            self.stock_selected.emit(stock_code)