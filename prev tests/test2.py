import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPainter, QPen, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QPoint
#from PyQt5.QtWidgets.QMainWindow import paintEvent


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

        # Create a QImage to act as the drawing surface
        self.canvas_image = QImage(600, 600, QImage.Format_RGB32)
        self.canvas_image.fill(Qt.white)

        self.canvas.installEventFilter(self)

    def add_buttons(self):
        # Pen Button
        self.pen_button = QPushButton("Pen", self)
        self.pen_button.clicked.connect(self.activate_pen)
        self.button_layout.addWidget(self.pen_button)

        # Eraser Button
        self.eraser_button = QPushButton("Eraser", self)
        self.eraser_button.clicked.connect(self.activate_eraser)
        self.button_layout.addWidget(self.eraser_button)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_canvas)
        self.button_layout.addWidget(self.save_button)

        # Clear Canvas Button
        self.clear_button = QPushButton("Clear Canvas", self)
        self.clear_button.clicked.connect(self.clear_canvas)
        self.button_layout.addWidget(self.clear_button)

    def activate_pen(self):
        self.pen_color = Qt.black
        self.pen_width = 2
        self.eraser_mode = False

    def activate_eraser(self):
        self.pen_color = Qt.white
        self.pen_width = 10
        self.eraser_mode = True

    def save_canvas(self):
        # Open a file dialog to save the image
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            self.canvas_image.save(file_path)

    def clear_canvas(self):
        self.canvas_image.fill(Qt.white)
        self.update()

    def eventFilter(self, obj, event):
        if obj == self.canvas:
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.drawing = True
                    self.last_point = event.pos()  # Start point for drawing
            elif event.type() == event.MouseMove:
                if self.drawing:  # Draw only if left button is pressed
                    painter = QPainter(self.canvas_image)
                    pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                    painter.setPen(pen)

                    # Map event position to local canvas coordinates
                    local_pos = event.pos()
                    paintEvent(self, event)  # Draw line
                    self.last_point = local_pos  # Update for next segment
                    self.canvas.update()  # Trigger a canvas repaint
            elif event.type() == event.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.drawing = False
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        # Paint the current canvas image onto the canvas widget
        canvas_painter = QPainter(self.canvas)
        canvas_painter.drawImage(0, 0, self.canvas_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())
