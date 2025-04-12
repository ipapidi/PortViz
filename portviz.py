#!/usr/bin/env python3

import sys
import re
import datetime
import socket
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLineEdit, QLabel, QTextEdit, QCheckBox
)
from ui.radar_widget import RadarWidget

# ------------------------------
# Port Scanner Thread (No Banner)
# ------------------------------
class ScanThread(QThread):
    result_signal = pyqtSignal(int, bool)

    def __init__(self, ip, ports, timeout=1):
        super().__init__()
        self.ip = ip
        self.ports = ports
        self.timeout = timeout

    def run(self):
        family = socket.AF_INET6 if ':' in self.ip else socket.AF_INET
        for port in self.ports:
            try:
                s = socket.socket(family, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                s.connect((self.ip, port))
                s.close()
                self.result_signal.emit(port, True)
            except:
                self.result_signal.emit(port, False)


# ------------------------------
# PortViz Main App
# ------------------------------
class PortViz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PortViz - Visual Port Scanner")
        self.setFixedSize(800, 1100)

        self.radar = RadarWidget()
        self.ip_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("any")
        self.show_closed_checkbox = QCheckBox("Show closed ports")
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(250)
        self.log_box.setStyleSheet("font-family: monospace;")

        # Layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("IP:"))
        input_layout.addWidget(self.ip_input)
        input_layout.addWidget(QLabel("Ports:"))
        input_layout.addWidget(self.port_input)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.show_closed_checkbox)
        options_layout.addWidget(self.scan_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.radar)
        main_layout.addWidget(self.log_box)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(options_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet(open("themes/dark.qss").read())

    def start_scan(self):
        ip = self.ip_input.text().strip()
        ports_input = self.port_input.text().strip()
        ports = self.parse_ports(ports_input)

        ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        ipv6_pattern = r"^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$"

        if not ip:
            self.append_log("[!] IP field is empty.", "#ff4444")
            return
        elif not re.match(ipv4_pattern, ip) and not re.match(ipv6_pattern, ip):
            self.append_log("[!] Invalid IP address format.", "#ff4444")
            return

        if not ports:
            self.append_log("[!] Port field is empty or invalid.", "#ff4444")
            return

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.append_log(f"[📡] Scan started at {now}", "#8888ff")
        self.append_log(f"[+] Scanning {ip} on ports: {', '.join(map(str, ports[:10]))}{'...' if len(ports) > 10 else ''}", "#00ff88")

        self.radar.clear_ports()
        self.thread = ScanThread(ip, ports)
        self.thread.result_signal.connect(self.handle_result)
        self.thread.start()

    def handle_result(self, port, is_open):
        ip = self.ip_input.text().strip()
        if is_open:
            self.radar.add_port(port)
            self.append_log(f"[+] {ip}:{port} OPEN", "#00ff88")
        elif self.show_closed_checkbox.isChecked():
            self.append_log(f"[•] {ip}:{port} closed", "#ff4444")

    def append_log(self, text, color="#ffffff"):
        self.log_box.append(f'<span style="color:{color}">{text}</span>')
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def parse_ports(self, port_text):
        port_text = port_text.lower().strip()
        if port_text in ["any", "all"]:
            return list(range(1, 1025))

        ports = set()
        for part in port_text.split(","):
            if "-" in part:
                try:
                    start, end = map(int, part.split("-"))
                    ports.update(range(start, end + 1))
                except:
                    pass
            else:
                try:
                    ports.add(int(part))
                except:
                    pass
        return sorted(p for p in ports if 1 <= p <= 65535)

# ------------------------------
# Launch App
# ------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortViz()
    window.show()
    sys.exit(app.exec_())

