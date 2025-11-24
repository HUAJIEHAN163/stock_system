#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票筛选窗口 - 多维度股票筛选功能
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLabel, QLineEdit, QComboBox, QGroupBox,
                             QFormLayout, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QSplitter, QFrame, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class StockFilterWindow(QWidget):
    """股票筛选窗口"""
    
    stock_selected = pyqtSignal(str)  # 股票选择信号
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("股票筛选")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # 左侧筛选条件面板
        filter_panel = self.create_filter_panel()
        splitter.addWidget(filter_panel)
        
        # 右侧结果显示面板
        result_panel = self.create_result_panel()
        splitter.addWidget(result_panel)
        
        # 设置分割比例
        splitter.setSizes([400, 800])
        
    def create_filter_panel(self):
        """创建筛选条件面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 基础筛选选项卡
        basic_tab = self.create_basic_filter_tab()
        tab_widget.addTab(basic_tab, "基础筛选")
        
        # 技术指标选项卡
        technical_tab = self.create_technical_filter_tab()
        tab_widget.addTab(technical_tab, "技术指标")
        
        # 财务指标选项卡
        financial_tab = self.create_financial_filter_tab()
        tab_widget.addTab(financial_tab, "财务指标")
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.filter_button = QPushButton("开始筛选")
        self.filter_button.clicked.connect(self.start_filter)
        
        self.reset_button = QPushButton("重置条件")
        self.reset_button.clicked.connect(self.reset_filters)
        
        self.save_button = QPushButton("保存条件")
        self.save_button.clicked.connect(self.save_filters)
        
        button_layout.addWidget(self.filter_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        return panel
        
    def create_basic_filter_tab(self):
        """创建基础筛选选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 市场分类组
        market_group = QGroupBox("市场分类")
        market_layout = QFormLayout(market_group)
        
        self.market_combo = QComboBox()
        self.market_combo.addItems(["全部", "主板", "创业板", "科创板", "北交所"])
        market_layout.addRow("交易市场:", self.market_combo)
        
        self.industry_combo = QComboBox()
        self.industry_combo.addItems(["全部", "银行", "房地产", "医药生物", "电子", "计算机"])
        market_layout.addRow("所属行业:", self.industry_combo)
        
        self.area_combo = QComboBox()
        self.area_combo.addItems(["全部", "北京", "上海", "深圳", "广东", "浙江"])
        market_layout.addRow("所属地区:", self.area_combo)
        
        layout.addWidget(market_group)
        
        # 基本指标组
        basic_group = QGroupBox("基本指标")
        basic_layout = QFormLayout(basic_group)
        
        # 市值范围
        market_cap_layout = QHBoxLayout()
        self.min_market_cap = QDoubleSpinBox()
        self.min_market_cap.setRange(0, 999999)
        self.min_market_cap.setSuffix(" 亿")
        self.max_market_cap = QDoubleSpinBox()
        self.max_market_cap.setRange(0, 999999)
        self.max_market_cap.setSuffix(" 亿")
        self.max_market_cap.setValue(999999)
        
        market_cap_layout.addWidget(self.min_market_cap)
        market_cap_layout.addWidget(QLabel("至"))
        market_cap_layout.addWidget(self.max_market_cap)
        basic_layout.addRow("市值范围:", market_cap_layout)
        
        # 股价范围
        price_layout = QHBoxLayout()
        self.min_price = QDoubleSpinBox()
        self.min_price.setRange(0, 9999)
        self.min_price.setSuffix(" 元")
        self.max_price = QDoubleSpinBox()
        self.max_price.setRange(0, 9999)
        self.max_price.setSuffix(" 元")
        self.max_price.setValue(9999)
        
        price_layout.addWidget(self.min_price)
        price_layout.addWidget(QLabel("至"))
        price_layout.addWidget(self.max_price)
        basic_layout.addRow("股价范围:", price_layout)
        
        # 成交量范围
        volume_layout = QHBoxLayout()
        self.min_volume = QDoubleSpinBox()
        self.min_volume.setRange(0, 999999)
        self.min_volume.setSuffix(" 万手")
        self.max_volume = QDoubleSpinBox()
        self.max_volume.setRange(0, 999999)
        self.max_volume.setSuffix(" 万手")
        self.max_volume.setValue(999999)
        
        volume_layout.addWidget(self.min_volume)
        volume_layout.addWidget(QLabel("至"))
        volume_layout.addWidget(self.max_volume)
        basic_layout.addRow("成交量:", volume_layout)
        
        layout.addWidget(basic_group)
        
        layout.addStretch()
        return widget
        
    def create_technical_filter_tab(self):
        """创建技术指标筛选选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 趋势指标组
        trend_group = QGroupBox("趋势指标")
        trend_layout = QFormLayout(trend_group)
        
        # MA均线
        self.ma5_check = QCheckBox("5日均线上方")
        trend_layout.addRow("", self.ma5_check)
        
        self.ma10_check = QCheckBox("10日均线上方")
        trend_layout.addRow("", self.ma10_check)
        
        self.ma20_check = QCheckBox("20日均线上方")
        trend_layout.addRow("", self.ma20_check)
        
        # 涨跌幅
        change_layout = QHBoxLayout()
        self.min_change = QDoubleSpinBox()
        self.min_change.setRange(-20, 20)
        self.min_change.setSuffix(" %")
        self.min_change.setValue(-20)
        self.max_change = QDoubleSpinBox()
        self.max_change.setRange(-20, 20)
        self.max_change.setSuffix(" %")
        self.max_change.setValue(20)
        
        change_layout.addWidget(self.min_change)
        change_layout.addWidget(QLabel("至"))
        change_layout.addWidget(self.max_change)
        trend_layout.addRow("涨跌幅:", change_layout)
        
        layout.addWidget(trend_group)
        
        # 动量指标组
        momentum_group = QGroupBox("动量指标")
        momentum_layout = QFormLayout(momentum_group)
        
        # RSI
        rsi_layout = QHBoxLayout()
        self.min_rsi = QSpinBox()
        self.min_rsi.setRange(0, 100)
        self.max_rsi = QSpinBox()
        self.max_rsi.setRange(0, 100)
        self.max_rsi.setValue(100)
        
        rsi_layout.addWidget(self.min_rsi)
        rsi_layout.addWidget(QLabel("至"))
        rsi_layout.addWidget(self.max_rsi)
        momentum_layout.addRow("RSI:", rsi_layout)
        
        # MACD
        self.macd_golden_check = QCheckBox("MACD金叉")
        momentum_layout.addRow("", self.macd_golden_check)
        
        self.macd_above_zero = QCheckBox("MACD在零轴上方")
        momentum_layout.addRow("", self.macd_above_zero)
        
        layout.addWidget(momentum_group)
        
        layout.addStretch()
        return widget
        
    def create_financial_filter_tab(self):
        """创建财务指标筛选选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 盈利能力组
        profit_group = QGroupBox("盈利能力")
        profit_layout = QFormLayout(profit_group)
        
        # ROE
        roe_layout = QHBoxLayout()
        self.min_roe = QDoubleSpinBox()
        self.min_roe.setRange(-100, 100)
        self.min_roe.setSuffix(" %")
        self.max_roe = QDoubleSpinBox()
        self.max_roe.setRange(-100, 100)
        self.max_roe.setSuffix(" %")
        self.max_roe.setValue(100)
        
        roe_layout.addWidget(self.min_roe)
        roe_layout.addWidget(QLabel("至"))
        roe_layout.addWidget(self.max_roe)
        profit_layout.addRow("ROE:", roe_layout)
        
        # 净利润增长率
        growth_layout = QHBoxLayout()
        self.min_growth = QDoubleSpinBox()
        self.min_growth.setRange(-100, 1000)
        self.min_growth.setSuffix(" %")
        self.max_growth = QDoubleSpinBox()
        self.max_growth.setRange(-100, 1000)
        self.max_growth.setSuffix(" %")
        self.max_growth.setValue(1000)
        
        growth_layout.addWidget(self.min_growth)
        growth_layout.addWidget(QLabel("至"))
        growth_layout.addWidget(self.max_growth)
        profit_layout.addRow("净利润增长率:", growth_layout)
        
        layout.addWidget(profit_group)
        
        # 估值指标组
        valuation_group = QGroupBox("估值指标")
        valuation_layout = QFormLayout(valuation_group)
        
        # PE
        pe_layout = QHBoxLayout()
        self.min_pe = QDoubleSpinBox()
        self.min_pe.setRange(0, 1000)
        self.max_pe = QDoubleSpinBox()
        self.max_pe.setRange(0, 1000)
        self.max_pe.setValue(1000)
        
        pe_layout.addWidget(self.min_pe)
        pe_layout.addWidget(QLabel("至"))
        pe_layout.addWidget(self.max_pe)
        valuation_layout.addRow("PE:", pe_layout)
        
        # PB
        pb_layout = QHBoxLayout()
        self.min_pb = QDoubleSpinBox()
        self.min_pb.setRange(0, 100)
        self.max_pb = QDoubleSpinBox()
        self.max_pb.setRange(0, 100)
        self.max_pb.setValue(100)
        
        pb_layout.addWidget(self.min_pb)
        pb_layout.addWidget(QLabel("至"))
        pb_layout.addWidget(self.max_pb)
        valuation_layout.addRow("PB:", pb_layout)
        
        layout.addWidget(valuation_group)
        
        # 财务健康组
        health_group = QGroupBox("财务健康")
        health_layout = QFormLayout(health_group)
        
        # 资产负债率
        debt_layout = QHBoxLayout()
        self.min_debt_ratio = QDoubleSpinBox()
        self.min_debt_ratio.setRange(0, 100)
        self.min_debt_ratio.setSuffix(" %")
        self.max_debt_ratio = QDoubleSpinBox()
        self.max_debt_ratio.setRange(0, 100)
        self.max_debt_ratio.setSuffix(" %")
        self.max_debt_ratio.setValue(100)
        
        debt_layout.addWidget(self.min_debt_ratio)
        debt_layout.addWidget(QLabel("至"))
        debt_layout.addWidget(self.max_debt_ratio)
        health_layout.addRow("资产负债率:", debt_layout)
        
        layout.addWidget(health_group)
        
        layout.addStretch()
        return widget
        
    def create_result_panel(self):
        """创建结果显示面板"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 结果标题
        result_label = QLabel("筛选结果")
        result_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(result_label)
        
        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "股票代码", "股票名称", "最新价", "涨跌幅", "成交量", "市值", "PE", "PB"
        ])
        
        # 设置表格属性
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setSortingEnabled(True)
        
        # 设置列宽
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # 双击事件
        self.result_table.itemDoubleClicked.connect(self.on_result_double_clicked)
        
        layout.addWidget(self.result_table)
        
        # 统计信息
        self.result_stats_label = QLabel("筛选结果: 0 只股票")
        layout.addWidget(self.result_stats_label)
        
        return panel
        
    def start_filter(self):
        """开始筛选"""
        # TODO: 实现筛选逻辑
        # 这里应该根据设置的条件查询数据库
        
        # 模拟数据
        sample_data = [
            ["000001.SZ", "平安银行", "12.50", "2.45", "15000", "2420", "6.8", "0.85"],
            ["000002.SZ", "万科A", "18.30", "-1.20", "8500", "2010", "8.2", "1.12"],
            ["600036.SH", "招商银行", "42.80", "1.85", "12000", "11500", "5.9", "1.05"],
        ]
        
        # 更新表格
        self.result_table.setRowCount(len(sample_data))
        
        for i, row_data in enumerate(sample_data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.result_table.setItem(i, j, item)
                
        # 更新统计信息
        self.result_stats_label.setText(f"筛选结果: {len(sample_data)} 只股票")
        
    def reset_filters(self):
        """重置筛选条件"""
        # 重置基础筛选
        self.market_combo.setCurrentIndex(0)
        self.industry_combo.setCurrentIndex(0)
        self.area_combo.setCurrentIndex(0)
        
        # 重置数值范围
        self.min_market_cap.setValue(0)
        self.max_market_cap.setValue(999999)
        self.min_price.setValue(0)
        self.max_price.setValue(9999)
        self.min_volume.setValue(0)
        self.max_volume.setValue(999999)
        
        # 重置技术指标
        self.ma5_check.setChecked(False)
        self.ma10_check.setChecked(False)
        self.ma20_check.setChecked(False)
        self.min_change.setValue(-20)
        self.max_change.setValue(20)
        
        # 重置财务指标
        self.min_roe.setValue(0)
        self.max_roe.setValue(100)
        self.min_pe.setValue(0)
        self.max_pe.setValue(1000)
        
        # 清空结果
        self.result_table.setRowCount(0)
        self.result_stats_label.setText("筛选结果: 0 只股票")
        
    def save_filters(self):
        """保存筛选条件"""
        # TODO: 实现保存筛选条件到文件
        pass
        
    def on_result_double_clicked(self, item):
        """结果双击事件"""
        row = item.row()
        code_item = self.result_table.item(row, 0)
        if code_item:
            stock_code = code_item.text()
            self.stock_selected.emit(stock_code)