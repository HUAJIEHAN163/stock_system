#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口 - 股票分析系统主界面
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QMenuBar, QStatusBar,
                             QAction, QMessageBox, QToolBar)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from .windows.stock_list_window import StockListWindow
from .windows.stock_filter_window import StockFilterWindow
from .windows.stock_detail_window import StockDetailWindow
from .windows.monitor_window import MonitorWindow
from .dialogs.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    """主窗口类"""
    
    # 信号定义
    stock_selected = pyqtSignal(str)  # 股票选择信号
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_connections()
        
    def init_ui(self):
        """初始化用户界面"""
        # 获取版本信息
        from src.__version__ import get_version_info
        version_info = get_version_info()
        self.setWindowTitle(f"{version_info['app_name']} {version_info['version']}")
        self.setGeometry(100, 100, 1400, 900)
        
        # 设置应用图标
        # self.setWindowIcon(QIcon('assets/icons/app_icon.ico'))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建各个功能窗口
        self.stock_list_window = StockListWindow()
        self.stock_filter_window = StockFilterWindow()
        self.stock_detail_window = StockDetailWindow()
        self.monitor_window = MonitorWindow()
        
        # 添加选项卡
        self.tab_widget.addTab(self.stock_list_window, "📊 股票列表")
        self.tab_widget.addTab(self.stock_filter_window, "🔍 股票筛选")
        self.tab_widget.addTab(self.stock_detail_window, "📈 股票详情")
        self.tab_widget.addTab(self.monitor_window, "🔔 实时监控")
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 系统菜单
        system_menu = menubar.addMenu('系统')
        
        # 系统设置
        settings_action = QAction('系统设置', self)
        settings_action.setShortcut('Ctrl+S')
        settings_action.triggered.connect(self.open_settings)
        system_menu.addAction(settings_action)
        
        system_menu.addSeparator()
        
        # 退出
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        system_menu.addAction(exit_action)
        
        # 数据菜单
        data_menu = menubar.addMenu('数据')
        
        # 数据初始化
        init_data_action = QAction('数据初始化', self)
        init_data_action.triggered.connect(self.init_data)
        data_menu.addAction(init_data_action)
        
        # 增量更新
        update_data_action = QAction('增量更新', self)
        update_data_action.triggered.connect(self.update_data)
        data_menu.addAction(update_data_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 数据初始化按钮
        init_action = QAction('数据初始化', self)
        init_action.triggered.connect(self.init_data)
        toolbar.addAction(init_action)
        
        # 增量更新按钮
        update_action = QAction('增量更新', self)
        update_action.triggered.connect(self.update_data)
        toolbar.addAction(update_action)
        
        toolbar.addSeparator()
        
        # 系统设置按钮
        settings_action = QAction('系统设置', self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
    def init_connections(self):
        """初始化信号连接"""
        # 股票列表选择信号
        self.stock_list_window.stock_selected.connect(self.on_stock_selected)
        
        # 选项卡切换信号
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
    def on_stock_selected(self, stock_code):
        """处理股票选择事件"""
        self.stock_selected.emit(stock_code)
        # 切换到股票详情页面
        self.tab_widget.setCurrentIndex(2)  # 股票详情页面索引
        # 更新股票详情
        self.stock_detail_window.update_stock_info(stock_code)
        
    def on_tab_changed(self, index):
        """处理选项卡切换事件"""
        tab_names = ["股票列表", "股票筛选", "股票详情", "实时监控"]
        if index < len(tab_names):
            self.status_bar.showMessage(f"当前页面: {tab_names[index]}")
            
    def open_settings(self):
        """打开系统设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec_() == dialog.Accepted:
            # 处理设置更新
            self.status_bar.showMessage("设置已更新", 3000)
            
    def init_data(self):
        """数据初始化"""
        reply = QMessageBox.question(self, '确认', '确定要进行数据初始化吗？这可能需要较长时间。',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.status_bar.showMessage("正在初始化数据...")
            # TODO: 实现数据初始化逻辑
            self.stock_list_window.init_data()
            
    def update_data(self):
        """增量数据更新"""
        self.status_bar.showMessage("正在更新数据...")
        # TODO: 实现增量更新逻辑
        self.stock_list_window.update_data()
        
    def show_about(self):
        """显示关于对话框"""
        from src.__version__ import get_version_info
        version_info = get_version_info()
        QMessageBox.about(self, "关于", 
                         f"{version_info['app_name']} {version_info['version']}\n\n"
                         f"{version_info['description']}\n"
                         f"包含选股、回测、监控等功能\n\n"
                         f"构建日期: {version_info['build_date']}\n"
                         f"{version_info['copyright']}")
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        reply = QMessageBox.question(self, '确认退出', '确定要退出股票分析系统吗？',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 设置应用信息
    from src.__version__ import get_version_info
    version_info = get_version_info()
    app.setApplicationName(version_info['app_name'])
    app.setApplicationVersion(version_info['version'])
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()