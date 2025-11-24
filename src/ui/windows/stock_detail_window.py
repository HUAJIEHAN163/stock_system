#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票详情窗口 - 显示单只股票的详细信息
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTabWidget, QTableWidget, QTableWidgetItem,
                             QSplitter, QFrame, QGroupBox, QFormLayout,
                             QTextEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StockDetailWindow(QWidget):
    """股票详情窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_stock_code = None
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 股票基本信息头部
        self.create_header_panel(layout)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # K线图表选项卡
        chart_tab = self.create_chart_tab()
        tab_widget.addTab(chart_tab, "📈 K线图表")
        
        # 基本信息选项卡
        info_tab = self.create_info_tab()
        tab_widget.addTab(info_tab, "📊 基本信息")
        
        # 财务数据选项卡
        financial_tab = self.create_financial_tab()
        tab_widget.addTab(financial_tab, "💰 财务数据")
        
        # 技术指标选项卡
        technical_tab = self.create_technical_tab()
        tab_widget.addTab(technical_tab, "📉 技术指标")
        
        # 资讯公告选项卡
        news_tab = self.create_news_tab()
        tab_widget.addTab(news_tab, "📰 资讯公告")
        
    def create_header_panel(self, parent_layout):
        """创建头部信息面板"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.StyledPanel)
        header_frame.setMaximumHeight(120)
        
        layout = QHBoxLayout(header_frame)
        
        # 左侧基本信息
        left_layout = QVBoxLayout()
        
        # 股票名称和代码
        self.stock_name_label = QLabel("请选择股票")
        self.stock_name_label.setFont(QFont("Arial", 16, QFont.Bold))
        left_layout.addWidget(self.stock_name_label)
        
        self.stock_code_label = QLabel("")
        self.stock_code_label.setFont(QFont("Arial", 12))
        left_layout.addWidget(self.stock_code_label)
        
        # 行业和地区
        info_layout = QHBoxLayout()
        self.industry_label = QLabel("")
        self.area_label = QLabel("")
        info_layout.addWidget(self.industry_label)
        info_layout.addWidget(self.area_label)
        info_layout.addStretch()
        left_layout.addLayout(info_layout)
        
        layout.addLayout(left_layout)
        
        # 中间价格信息
        middle_layout = QVBoxLayout()
        
        self.current_price_label = QLabel("--")
        self.current_price_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.current_price_label.setStyleSheet("color: red;")
        middle_layout.addWidget(self.current_price_label)
        
        price_change_layout = QHBoxLayout()
        self.price_change_label = QLabel("--")
        self.pct_change_label = QLabel("--")
        price_change_layout.addWidget(self.price_change_label)
        price_change_layout.addWidget(self.pct_change_label)
        middle_layout.addLayout(price_change_layout)
        
        layout.addLayout(middle_layout)
        
        # 右侧关键指标
        right_layout = QFormLayout()
        
        self.pe_label = QLabel("--")
        self.pb_label = QLabel("--")
        self.market_cap_label = QLabel("--")
        self.volume_label = QLabel("--")
        
        right_layout.addRow("市盈率:", self.pe_label)
        right_layout.addRow("市净率:", self.pb_label)
        right_layout.addRow("总市值:", self.market_cap_label)
        right_layout.addRow("成交量:", self.volume_label)
        
        layout.addLayout(right_layout)
        
        parent_layout.addWidget(header_frame)
        
    def create_chart_tab(self):
        """创建K线图表选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 图表控制面板
        control_panel = QFrame()
        control_panel.setMaximumHeight(60)
        control_layout = QHBoxLayout(control_panel)
        
        # 时间周期按钮
        period_buttons = ["日K", "周K", "月K", "5分钟", "15分钟", "30分钟", "60分钟"]
        for period in period_buttons:
            btn = QPushButton(period)
            btn.setCheckable(True)
            if period == "日K":
                btn.setChecked(True)
            control_layout.addWidget(btn)
            
        control_layout.addStretch()
        
        # 指标选择
        indicator_buttons = ["MA", "MACD", "RSI", "KDJ", "BOLL"]
        for indicator in indicator_buttons:
            btn = QPushButton(indicator)
            btn.setCheckable(True)
            control_layout.addWidget(btn)
            
        layout.addWidget(control_panel)
        
        # 图表区域（占位）
        chart_placeholder = QLabel("K线图表区域\n（待集成图表库）")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setStyleSheet("border: 1px dashed gray; background-color: #f0f0f0;")
        chart_placeholder.setMinimumHeight(400)
        
        layout.addWidget(chart_placeholder)
        
        return widget
        
    def create_info_tab(self):
        """创建基本信息选项卡"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # 左侧基本资料
        left_group = QGroupBox("基本资料")
        left_layout = QFormLayout(left_group)
        
        self.info_labels = {}
        info_fields = [
            ("股票代码", "ts_code"),
            ("股票简称", "name"),
            ("英文名称", "enname"),
            ("交易市场", "market"),
            ("所属行业", "industry"),
            ("所属地区", "area"),
            ("上市日期", "list_date"),
            ("退市日期", "delist_date"),
            ("是否沪深港通", "is_hs")
        ]
        
        for label, field in info_fields:
            self.info_labels[field] = QLabel("--")
            left_layout.addRow(f"{label}:", self.info_labels[field])
            
        layout.addWidget(left_group)
        
        # 右侧实时数据
        right_group = QGroupBox("实时数据")
        right_layout = QFormLayout(right_group)
        
        self.realtime_labels = {}
        realtime_fields = [
            ("最新价", "close"),
            ("涨跌额", "change"),
            ("涨跌幅", "pct_chg"),
            ("开盘价", "open"),
            ("最高价", "high"),
            ("最低价", "low"),
            ("昨收价", "pre_close"),
            ("成交量", "vol"),
            ("成交额", "amount"),
            ("换手率", "turnover_rate")
        ]
        
        for label, field in realtime_fields:
            self.realtime_labels[field] = QLabel("--")
            right_layout.addRow(f"{label}:", self.realtime_labels[field])
            
        layout.addWidget(right_group)
        
        return widget
        
    def create_financial_tab(self):
        """创建财务数据选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 财务报表选择
        report_layout = QHBoxLayout()
        
        report_buttons = ["利润表", "资产负债表", "现金流量表", "财务指标"]
        for report in report_buttons:
            btn = QPushButton(report)
            btn.setCheckable(True)
            if report == "利润表":
                btn.setChecked(True)
            report_layout.addWidget(btn)
            
        report_layout.addStretch()
        layout.addLayout(report_layout)
        
        # 财务数据表格
        self.financial_table = QTableWidget()
        self.financial_table.setColumnCount(5)
        self.financial_table.setHorizontalHeaderLabels([
            "项目", "2023年", "2022年", "2021年", "2020年"
        ])
        
        # 示例数据
        sample_data = [
            ["营业收入", "1000.00", "950.00", "900.00", "850.00"],
            ["净利润", "100.00", "95.00", "90.00", "85.00"],
            ["每股收益", "1.50", "1.43", "1.35", "1.28"],
            ["净资产收益率", "15.2%", "14.8%", "14.5%", "14.1%"],
        ]
        
        self.financial_table.setRowCount(len(sample_data))
        for i, row_data in enumerate(sample_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.financial_table.setItem(i, j, item)
                
        layout.addWidget(self.financial_table)
        
        return widget
        
    def create_technical_tab(self):
        """创建技术指标选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧指标列表
        left_group = QGroupBox("技术指标")
        left_layout = QVBoxLayout(left_group)
        
        self.technical_table = QTableWidget()
        self.technical_table.setColumnCount(3)
        self.technical_table.setHorizontalHeaderLabels(["指标", "数值", "信号"])
        
        # 示例技术指标数据
        technical_data = [
            ["MA5", "12.50", "上涨"],
            ["MA10", "12.30", "上涨"],
            ["MA20", "12.00", "上涨"],
            ["RSI", "65.5", "强势"],
            ["MACD", "0.15", "金叉"],
            ["KDJ_K", "75.2", "超买"],
            ["BOLL上轨", "13.20", ""],
            ["BOLL中轨", "12.50", ""],
            ["BOLL下轨", "11.80", ""],
        ]
        
        self.technical_table.setRowCount(len(technical_data))
        for i, row_data in enumerate(technical_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.technical_table.setItem(i, j, item)
                
        left_layout.addWidget(self.technical_table)
        splitter.addWidget(left_group)
        
        # 右侧指标说明
        right_group = QGroupBox("指标说明")
        right_layout = QVBoxLayout(right_group)
        
        self.indicator_desc = QTextEdit()
        self.indicator_desc.setReadOnly(True)
        self.indicator_desc.setText("""
技术指标说明：

MA（移动平均线）：
- MA5: 5日移动平均线
- MA10: 10日移动平均线  
- MA20: 20日移动平均线

RSI（相对强弱指标）：
- 70以上为超买区域
- 30以下为超卖区域

MACD（指数平滑移动平均线）：
- 金叉：DIF上穿DEA，买入信号
- 死叉：DIF下穿DEA，卖出信号

KDJ（随机指标）：
- K值80以上超买，20以下超卖

BOLL（布林带）：
- 价格触及上轨可能回调
- 价格触及下轨可能反弹
        """)
        
        right_layout.addWidget(self.indicator_desc)
        splitter.addWidget(right_group)
        
        # 设置分割比例
        splitter.setSizes([400, 300])
        
        return widget
        
    def create_news_tab(self):
        """创建资讯公告选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 资讯类型选择
        news_type_layout = QHBoxLayout()
        
        news_buttons = ["公司公告", "研报分析", "新闻资讯", "龙虎榜", "大宗交易"]
        for news_type in news_buttons:
            btn = QPushButton(news_type)
            btn.setCheckable(True)
            if news_type == "公司公告":
                btn.setChecked(True)
            news_type_layout.addWidget(btn)
            
        news_type_layout.addStretch()
        layout.addLayout(news_type_layout)
        
        # 资讯列表
        self.news_table = QTableWidget()
        self.news_table.setColumnCount(3)
        self.news_table.setHorizontalHeaderLabels(["日期", "标题", "类型"])
        
        # 示例资讯数据
        news_data = [
            ["2024-01-15", "2023年年度业绩预告", "业绩预告"],
            ["2024-01-10", "关于股东减持计划的公告", "股东变动"],
            ["2024-01-08", "董事会决议公告", "治理结构"],
            ["2024-01-05", "2023年第四季度经营数据", "经营数据"],
        ]
        
        self.news_table.setRowCount(len(news_data))
        for i, row_data in enumerate(news_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.news_table.setItem(i, j, item)
                
        layout.addWidget(self.news_table)
        
        return widget
        
    def update_stock_info(self, stock_code):
        """更新股票信息"""
        self.current_stock_code = stock_code
        
        # TODO: 从数据库加载股票信息
        # 这里使用模拟数据
        
        # 更新头部信息
        self.stock_name_label.setText("平安银行")
        self.stock_code_label.setText(f"股票代码: {stock_code}")
        self.industry_label.setText("行业: 银行")
        self.area_label.setText("地区: 深圳")
        
        # 更新价格信息
        self.current_price_label.setText("12.50")
        self.price_change_label.setText("+0.28")
        self.pct_change_label.setText("+2.29%")
        
        # 更新关键指标
        self.pe_label.setText("6.8")
        self.pb_label.setText("0.85")
        self.market_cap_label.setText("2420亿")
        self.volume_label.setText("15000万手")
        
        # 更新基本信息
        if hasattr(self, 'info_labels'):
            self.info_labels['ts_code'].setText(stock_code)
            self.info_labels['name'].setText("平安银行")
            self.info_labels['market'].setText("主板")
            self.info_labels['industry'].setText("银行")
            self.info_labels['area'].setText("深圳")
            self.info_labels['list_date'].setText("1991-04-03")
            
        # 更新实时数据
        if hasattr(self, 'realtime_labels'):
            self.realtime_labels['close'].setText("12.50")
            self.realtime_labels['change'].setText("+0.28")
            self.realtime_labels['pct_chg'].setText("+2.29%")
            self.realtime_labels['open'].setText("12.25")
            self.realtime_labels['high'].setText("12.58")
            self.realtime_labels['low'].setText("12.20")
            self.realtime_labels['vol'].setText("15000万手")
            self.realtime_labels['amount'].setText("18.5亿")