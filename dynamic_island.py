#!/usr/bin/env python3
import sys
import os
import psutil
import time
import threading
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                            QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor

class AlwaysVisibleIsland(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_beautiful_ui()
        self.start_monitoring()
        
    def setup_window(self):
        """Setup always-on-top window"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Fixed size and position
        self.setFixedSize(460, 140)
        
        # Center at top of screen
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - 460) // 2
        y = 10
        
        self.setGeometry(x, y, 460, 140)
        
        # Initialize stats
        self.cpu = self.ram = self.disk = 0
        self.upload = self.download = 0
        
    def create_beautiful_ui(self):
        """Create the beautiful UI that worked before"""
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # Top row - Stats
        top_row = QHBoxLayout()
        top_row.setSpacing(12)
        
        # CPU (Blue)
        self.cpu_label = QLabel(f"CPU {self.cpu}%")
        self.cpu_label.setStyleSheet("""
            color: #007AFF; 
            font: bold 14px 'Helvetica Neue';
            background: transparent;
        """)
        
        # Separator
        sep = QLabel("•")
        sep.setStyleSheet("color: #666666; font: 14px 'Helvetica Neue'; background: transparent;")
        
        # RAM (Green)
        self.ram_label = QLabel(f"RAM {self.ram}%")
        self.ram_label.setStyleSheet("""
            color: #34C759; 
            font: bold 14px 'Helvetica Neue';
            background: transparent;
        """)
        
        top_row.addWidget(self.cpu_label)
        top_row.addWidget(sep)
        top_row.addWidget(self.ram_label)
        top_row.addStretch()
        
        # Full GUI button
        gui_btn = QPushButton("⚙ Full GUI")
        gui_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                font: 10px 'Helvetica Neue';
            }
            QPushButton:hover { background-color: #2a2a2a; }
        """)
        gui_btn.clicked.connect(self.open_full_gui)
        top_row.addWidget(gui_btn)
        
        layout.addLayout(top_row)
        
        # Network/Disk row
        mid_row = QHBoxLayout()
        
        self.net_label = QLabel("↑ 0 B/s  ↓ 0 B/s")
        self.net_label.setStyleSheet("color: #FF9500; font: 11px 'Helvetica Neue'; background: transparent;")
        
        self.disk_label = QLabel("Disk 0%")
        self.disk_label.setStyleSheet("color: #AF52DE; font: 11px 'Helvetica Neue'; background: transparent;")
        
        mid_row.addWidget(self.net_label)
        mid_row.addStretch()
        mid_row.addWidget(self.disk_label)
        
        layout.addLayout(mid_row)
        
        # Action buttons - PERFECT alignment
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        # Free Up Memory
        btn1 = QPushButton("🧹 Free Up Memory")
        btn1.setFixedSize(140, 36)
        btn1.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border: none;
                border-radius: 16px;
                font: bold 10px 'Helvetica Neue';
            }
            QPushButton:hover { background-color: #FF3B30; }
        """)
        btn1.clicked.connect(self.purge_memory)
        
        # Flush DNS Cache
        btn2 = QPushButton("🌐 Flush DNS Cache")
        btn2.setFixedSize(140, 36)
        btn2.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border: none;
                border-radius: 16px;
                font: bold 10px 'Helvetica Neue';
            }
            QPushButton:hover { background-color: #007AFF; }
        """)
        btn2.clicked.connect(self.flush_dns)
        
        # About
        btn3 = QPushButton("ℹ️ About")
        btn3.setFixedSize(100, 36)
        btn3.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border: none;
                border-radius: 16px;
                font: bold 10px 'Helvetica Neue';
            }
            QPushButton:hover { background-color: #34C759; }
        """)
        btn3.clicked.connect(self.show_about)
        
        btn_row.addWidget(btn1)
        btn_row.addWidget(btn2)
        btn_row.addWidget(btn3)
        
        layout.addLayout(btn_row)
        
        self.setLayout(layout)
        
    def paintEvent(self, event):
        """Draw perfect rounded background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # Perfect rounded rectangle
        rect = self.rect().adjusted(3, 3, -3, -3)
        painter.setBrush(QBrush(QColor(10, 10, 10, 245)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 24, 24)
        
    def show_about(self):
        QMessageBox.information(self, "About OptiMac", "OptiMac Enhanced v2.0\nDynamic Island Interface")
        
    def open_full_gui(self):
        subprocess.Popen([sys.executable, 'optimac_gui.py'])
        
    def purge_memory(self):
        subprocess.run(["sudo", "purge"], capture_output=True)
        
    def flush_dns(self):
        subprocess.run(["sudo", "dscacheutil", "-flushcache"], capture_output=True)
        
    def start_monitoring(self):
        timer = QTimer()
        timer.timeout.connect(self.update_stats)
        timer.start(3000)
        
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()
        
    def update_stats(self):
        try:
            self.cpu = int(psutil.cpu_percent())
            mem = psutil.virtual_memory()
            self.ram = int(mem.percent)
            disk = psutil.disk_usage('/')
            self.disk = int(disk.percent)
            
            # Update labels
            self.cpu_label.setText(f"CPU {self.cpu}%")
            self.ram_label.setText(f"RAM {self.ram}%")
            self.disk_label.setText(f"Disk {self.disk}%")
        except:
            pass

def main():
    os.environ['QT_LOGGING_RULES'] = 'qt.qpa.fonts.debug=false'
    app = QApplication(sys.argv)
    island = AlwaysVisibleIsland()
    island.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

