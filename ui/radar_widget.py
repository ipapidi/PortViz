from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import QTimer, Qt
import math

class RadarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.ports = []   # (port, angle)
        self.pulses = []  # (x, y, opacity, size)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # 20 FPS

    def update_animation(self):
        self.angle = (self.angle + 3) % 360

        # Fade out existing pulses
        new_pulses = []
        for px, py, opacity, size in self.pulses:
            if opacity > 0:
                new_pulses.append((px, py, opacity - 10, size + 1))
        self.pulses = new_pulses

        # Detect pulse trigger
        for port, port_angle in self.ports:
            if abs(self.angle - port_angle) < 5:  # near needle
                center = self.rect().center()
                radius = min(self.width(), self.height()) // 2 - 40
                rad = math.radians(port_angle)
                px = center.x() + (radius - 10) * math.cos(rad)
                py = center.y() - (radius - 10) * math.sin(rad)
                self.pulses.append((px, py, 255, 10))

        self.update()

    def add_port(self, port):
        if any(p == port for p, _ in self.ports):
            return
        angle = port % 360
        self.ports.append((port, angle))

    def clear_ports(self):
        self.ports = []
        self.pulses = []

    def paintEvent(self, event):
        painter = QPainter(self)
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 40

        # Radar rings
        painter.setPen(QPen(QColor("#2e2e2e"), 1))
        for r in range(50, radius, 50):
            painter.drawEllipse(center, r, r)

        # Radar sweep line
        painter.setPen(QPen(QColor("#00ff88"), 2))
        angle_rad = math.radians(self.angle)
        x = center.x() + radius * math.cos(angle_rad)
        y = center.y() - radius * math.sin(angle_rad)
        painter.drawLine(center.x(), center.y(), int(x), int(y))

        # Port dots
        for port, port_angle in self.ports:
            rad = math.radians(port_angle)
            px = center.x() + (radius - 10) * math.cos(rad)
            py = center.y() - (radius - 10) * math.sin(rad)

            # Color by port
            if port == 22:
                color = QColor("#ffff00")
            elif port in [80, 443, 8080]:
                color = QColor("#00ffff")
            elif port == 21:
                color = QColor("#ff66cc")
            elif port == 53:
                color = QColor("#ff9933")
            else:
                color = QColor("#00ff88")

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(px), int(py), 8, 8)

        # Pulses
        for px, py, opacity, size in self.pulses:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(0, 255, 136, opacity), 1))
            painter.drawEllipse(int(px - size / 2), int(py - size / 2), size, size)
        
        # Color Legend
        legend = [
            ("SSH (22)", "#ffff00"),
            ("HTTP/HTTPS (80, 443, 8080)", "#00ffff"),
            ("FTP (21)", "#ff66cc"),
            ("DNS (53)", "#ff9933"),
            ("Other", "#00ff88"),
        ]

        start_y = self.height() - 130
        line_height = 28

        for i, (label, hex_color) in enumerate(legend):
            y = start_y + i * line_height
            painter.setPen(QColor(hex_color))
            painter.setBrush(QColor(hex_color))
            painter.drawRect(30, y, 10, 10)
            painter.setPen(QColor("#ffffff"))
            painter.drawText(50, y + 10, label)


