#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统设置对话框 - Token设置和验证
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
                             QTextEdit, QGroupBox, QFormLayout, QMessageBox,
                             QProgressBar, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class TokenValidator(QThread):
    """Token验证线程"""
    validation_finished = pyqtSignal(bool, str, dict)  # 成功/失败, 消息, 详细结果
    
    def __init__(self, token, token_type):
        super().__init__()
        self.token = token
        self.token_type = token_type
        
    def run(self):
        """执行token验证"""
        try:
            if self.token_type == "tudata":
                import tudata as ts
            else:
                import tushare as ts
                
            # 设置token
            ts.set_token(self.token)
            pro = ts.pro_api()
            
            # 测试基础API
            test_results = {}
            
            # 测试股票列表（基础权限）
            try:
                df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
                test_results['stock_basic'] = {'success': True, 'count': len(df)}
            except Exception as e:
                test_results['stock_basic'] = {'success': False, 'error': str(e)}
            
            # 测试日线行情（基础权限）
            try:
                df = pro.daily(ts_code='000001.SZ', start_date='20240101', end_date='20240105')
                test_results['daily'] = {'success': True, 'count': len(df)}
            except Exception as e:
                test_results['daily'] = {'success': False, 'error': str(e)}
                
            # 测试财务数据（需要更高权限）
            try:
                df = pro.income(ts_code='000001.SZ', period='20231231')
                test_results['income'] = {'success': True, 'count': len(df)}
            except Exception as e:
                test_results['income'] = {'success': False, 'error': str(e)}
            
            # 判断验证结果
            basic_success = test_results['stock_basic']['success'] and test_results['daily']['success']
            
            if basic_success:
                message = "Token验证成功！"
                if test_results['income']['success']:
                    message += " (包含高级权限)"
                else:
                    message += " (基础权限)"
                self.validation_finished.emit(True, message, test_results)
            else:
                self.validation_finished.emit(False, "Token验证失败，请检查token是否正确", test_results)
                
        except Exception as e:
            self.validation_finished.emit(False, f"验证过程出错: {str(e)}", {})

class SettingsDialog(QDialog):
    """系统设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("系统设置")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        # 主布局
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Token设置选项卡
        token_tab = self.create_token_tab()
        tab_widget.addTab(token_tab, "Token设置")
        
        # 数据库设置选项卡
        db_tab = self.create_database_tab()
        tab_widget.addTab(db_tab, "数据库设置")
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.apply_button = QPushButton("应用")
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)
        
        layout.addLayout(button_layout)
        
        # 连接信号
        self.ok_button.clicked.connect(self.accept_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.apply_button.clicked.connect(self.apply_settings)
        
    def create_token_tab(self):
        """创建Token设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Token配置组
        token_group = QGroupBox("Token配置")
        token_layout = QFormLayout(token_group)
        
        # Token类型选择
        self.token_type_combo = QComboBox()
        self.token_type_combo.addItems(["tushare", "tudata"])
        token_layout.addRow("Token类型:", self.token_type_combo)
        
        # Token输入
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("请输入您的Token")
        token_layout.addRow("Token:", self.token_input)
        
        # Token验证按钮
        self.validate_button = QPushButton("验证Token")
        self.validate_button.clicked.connect(self.validate_token)
        token_layout.addRow("", self.validate_button)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        token_layout.addRow("", self.progress_bar)
        
        layout.addWidget(token_group)
        
        # 验证结果组
        result_group = QGroupBox("验证结果")
        result_layout = QVBoxLayout(result_group)
        
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(200)
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        
        layout.addWidget(result_group)
        
        layout.addStretch()
        return widget
        
    def create_database_tab(self):
        """创建数据库设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 数据库配置组
        db_group = QGroupBox("数据库配置")
        db_layout = QFormLayout(db_group)
        
        # 数据库路径
        self.db_path_input = QLineEdit()
        self.db_path_input.setText("database/stock_data.db")
        db_layout.addRow("数据库路径:", self.db_path_input)
        
        # 自动备份
        self.auto_backup_check = QCheckBox("启用自动备份")
        db_layout.addRow("", self.auto_backup_check)
        
        layout.addWidget(db_group)
        
        # 数据更新配置组
        update_group = QGroupBox("数据更新配置")
        update_layout = QFormLayout(update_group)
        
        # 自动更新
        self.auto_update_check = QCheckBox("启用自动更新")
        update_layout.addRow("", self.auto_update_check)
        
        # 更新时间
        self.update_time_input = QLineEdit()
        self.update_time_input.setText("18:00")
        self.update_time_input.setPlaceholderText("HH:MM")
        update_layout.addRow("更新时间:", self.update_time_input)
        
        layout.addWidget(update_group)
        
        layout.addStretch()
        return widget
        
    def validate_token(self):
        """验证Token"""
        token = self.token_input.text().strip()
        token_type = self.token_type_combo.currentText()
        
        if not token:
            QMessageBox.warning(self, "警告", "请输入Token")
            return
            
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 无限进度条
        self.validate_button.setEnabled(False)
        self.result_text.clear()
        self.result_text.append("正在验证Token...")
        
        # 启动验证线程
        self.validator = TokenValidator(token, token_type)
        self.validator.validation_finished.connect(self.on_validation_finished)
        self.validator.start()
        
    def on_validation_finished(self, success, message, results):
        """验证完成回调"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        self.validate_button.setEnabled(True)
        
        # 显示结果
        self.result_text.clear()
        self.result_text.append(f"验证结果: {message}\n")
        
        if results:
            self.result_text.append("详细测试结果:")
            for api, result in results.items():
                if result['success']:
                    self.result_text.append(f"✓ {api}: 成功 (数据条数: {result.get('count', 0)})")
                else:
                    self.result_text.append(f"✗ {api}: 失败 - {result.get('error', '未知错误')}")
        
        if success:
            # 保存Token配置
            self.save_token_config(self.token_input.text().strip(), self.token_type_combo.currentText())
            
    def save_token_config(self, token, token_type):
        """保存Token配置"""
        try:
            config_dir = "config"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            config_file = os.path.join(config_dir, "token_config.txt")
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"token={token}\n")
                f.write(f"token_type={token_type}\n")
                
            self.result_text.append("\nToken配置已保存到 config/token_config.txt")
            
        except Exception as e:
            self.result_text.append(f"\n保存配置失败: {str(e)}")
            
    def load_settings(self):
        """加载设置"""
        try:
            config_file = "config/token_config.txt"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line in lines:
                    line = line.strip()
                    if line.startswith("token="):
                        self.token_input.setText(line.split("=", 1)[1])
                    elif line.startswith("token_type="):
                        token_type = line.split("=", 1)[1]
                        index = self.token_type_combo.findText(token_type)
                        if index >= 0:
                            self.token_type_combo.setCurrentIndex(index)
                            
        except Exception as e:
            print(f"加载设置失败: {e}")
            
    def apply_settings(self):
        """应用设置"""
        # TODO: 实现设置应用逻辑
        QMessageBox.information(self, "信息", "设置已应用")
        
    def accept_settings(self):
        """确定并关闭"""
        self.apply_settings()
        self.accept()