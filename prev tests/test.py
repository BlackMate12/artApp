import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QMouseEvent
from PyQt5.QtCore import Qt, QPoint


class ArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art App")
        self.setGeometry(100, 100, 800, 600)

        # Canvas properties
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.pen_width = 2
        self.eraser_mode = False

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout for the main window
        self.main_layout = QHBoxLayout(self.central_widget)

        # Buttons layout (left side)
        self.button_layout = QVBoxLayout()

        # Add buttons to the left side
        self.add_buttons()

        # Canvas area
        self.canvas = QWidget(self)
        self.canvas.setStyleSheet("background-color: white;")
        self.canvas.setMinimumSize(600, 600)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.canvas)

        self.canvas.installEventFilter(self)

        # Pixmap for drawing
        self.canvas_pixmap = self.canvas.grab().toImage()

    def add_buttons(self):
        # Brush Button
        self.brush_button = QPushButton("Brush", self)
        self.brush_button.clicked.connect(self.activate_brush)
        self.button_layout.addWidget(self.brush_button)

        # Pen Button
        self.pen_button = QPushButton("Pen", self)
        self.pen_button.clicked.connect(self.activate_pen)
        self.button_layout.addWidget(self.pen_button)

        # Eraser Button
        self.eraser_button = QPushButton("Eraser", self)
        self.eraser_button.clicked.connect(self.activate_eraser)
        self.button_layout.addWidget(self.eraser_button)

        # Clear Button
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_canvas)
        self.button_layout.addWidget(self.clear_button)

    def activate_brush(self):
        self.pen_color = Qt.black
        self.pen_width = 5
        self.eraser_mode = False

    def activate_pen(self):
        self.pen_color = Qt.black
        self.pen_width = 2
        self.eraser_mode = False

    def activate_eraser(self):
        self.pen_color = Qt.white
        self.pen_width = 10
        self.eraser_mode = True

    def clear_canvas(self):
        self.canvas_pixmap.fill(Qt.white)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())
