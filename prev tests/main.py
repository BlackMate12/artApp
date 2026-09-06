from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from PIL import Image

class ArtProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArtApp")
        self.setGeometry(100, 100, 800, 600)

        # Initialize variables
        self.canvas_width = 800
        self.canvas_height = 600
        self.last_point = QPoint()
        self.drawing = False

        # Create a blank canvas
        self.canvas = QImage(self.canvas_width, self.canvas_height, QImage.Format_RGB32)
        self.canvas.fill(Qt.white)

        # Set up the UI
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Canvas display
        self.canvas_label = QLabel(self)
        self.canvas_label.setPixmap(QPixmap.fromImage(self.canvas))
        main_layout.addWidget(self.canvas_label)

        # Buttons
        button_layout = QHBoxLayout()

        new_canvas_btn = QPushButton("New Canvas")
        new_canvas_btn.clicked.connect(self.new_canvas)
        button_layout.addWidget(new_canvas_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_canvas)
        button_layout.addWidget(save_btn)

        main_layout.addLayout(button_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def new_canvas(self):
        self.canvas.fill(Qt.white)
        self.update_canvas()

    def save_canvas(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Canvas", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
        if file_path:
            self.canvas.save(file_path)

    def update_canvas(self):
        self.canvas_label.setPixmap(QPixmap.fromImage(self.canvas))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing and event.buttons() == Qt.LeftButton:
            painter = QPainter(self.canvas)
            pen = QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update_canvas()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False


if __name__ == "__main__":
    app = QApplication([])
    window = ArtProgram()
    window.show()
    app.exec_()
