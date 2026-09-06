import sys
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

class Layer:
    def __init__(self, name, width, height, visible=True, opacity=100):
        self.content = QImage(width, height, QImage.Format_ARGB32)
        self.content.fill(Qt.transparent)
        self.name = name
        self.visible = visible
        self.opacity = opacity

    def toggle_visibility(self):
        self.visible = not self.visible

    def change_opacity(self, new_opacity):
        if 0 <= new_opacity <= 100:
            self.opacity = new_opacity
        elif 100 < new_opacity:
            self.opacity = 100
        elif 0 > new_opacity:
            self.opacity = 0

    def clear_layer(self):
        self.content.fill(Qt.transparent)

    def get_content(self):
        return self.content