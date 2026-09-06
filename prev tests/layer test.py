import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QColorDialog
from PyQt5.QtGui import QPainter, QPen, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas_image = QImage(600, 600, QImage.Format_RGB32)
        self.canvas_image.fill(Qt.white)

    def paintEvent(self, event):
        # Paint the current canvas image onto the canvas widget
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(0, 0, self.canvas_image)

class Layer:
    def __init__(self, width, height):
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)  # Transparent background
        self.visible = True
        self.opacity = 1.0  # Fully opaque by default

class LayeredCanvas(QWidget):
    def __init__(self, parent=None, width=800, height=600):
        super().__init__(parent)
        self.layers = []  # List to store layers
        self.current_layer_index = -1  # No layer selected initially
        self.setFixedSize(width, height)

        # Add an initial layer
        self.add_layer()

    def add_layer(self):
        new_layer = Layer(self.width(), self.height())
        self.layers.append(new_layer)
        self.current_layer_index = len(self.layers) - 1
        self.update()

    def delete_layer(self):
        if self.current_layer_index != -1:
            self.layers.pop(self.current_layer_index)
            self.current_layer_index = max(0, len(self.layers) - 1)
            self.update()

    def toggle_layer_visibility(self, index):
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible
            self.update()

    def set_current_layer(self, index):
        if 0 <= index < len(self.layers):
            self.current_layer_index = index

    def paintEvent(self, event):
        """Draw all visible layers in order."""
        canvas_painter = QPainter(self)
        for layer in self.layers:
            if layer.visible:
                painter = QPainter(layer.image)
                painter.setOpacity(layer.opacity)  # Apply opacity
                canvas_painter.drawImage(0, 0, layer.image)

    def mousePressEvent(self, event):
        if self.current_layer_index != -1:
            self.parent().start_drawing(event.pos())

    def mouseMoveEvent(self, event):
        if self.current_layer_index != -1 and self.parent().drawing:
            self.parent().continue_drawing(event.pos())

    def mouseReleaseEvent(self, event):
        if self.current_layer_index != -1:
            self.parent().stop_drawing()

class ArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art App with Layers")
        self.setGeometry(100, 100, 1000, 600)

        # Drawing properties
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.pen_width = 2

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QHBoxLayout(self.central_widget)
        self.button_layout = QVBoxLayout()

        # Add canvas with layers
        self.canvas = LayeredCanvas(self)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.canvas)

        # Add buttons for layer management
        self.add_buttons()

    def add_buttons(self):
        # Add Layer Button
        self.add_layer_button = QPushButton("Add Layer", self)
        self.add_layer_button.clicked.connect(self.canvas.add_layer)
        self.button_layout.addWidget(self.add_layer_button)

        # Delete Layer Button
        self.delete_layer_button = QPushButton("Delete Layer", self)
        self.delete_layer_button.clicked.connect(self.canvas.delete_layer)
        self.button_layout.addWidget(self.delete_layer_button)

        # Layer Visibility Toggle Button
        self.toggle_visibility_button = QPushButton("Toggle Visibility", self)
        self.toggle_visibility_button.clicked.connect(
            lambda: self.canvas.toggle_layer_visibility(self.canvas.current_layer_index)
        )
        self.button_layout.addWidget(self.toggle_visibility_button)

        # Additional controls can be added for reordering and opacity adjustment

    def start_drawing(self, pos):
        self.drawing = True
        self.last_point = pos

    def continue_drawing(self, pos):
        if self.drawing and self.canvas.current_layer_index != -1:
            current_layer = self.canvas.layers[self.canvas.current_layer_index]
            painter = QPainter(current_layer.image)
            pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, pos)
            self.last_point = pos
            self.canvas.update()

    def stop_drawing(self):
        self.drawing = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())