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

class ArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art App")
        self.setGeometry(100, 100, 800, 600)

        # Canvas properties
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.eraser_color = Qt.white
        self.current_color = self.pen_color
        self.pen_width = 2

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout for the main window
        self.main_layout = QHBoxLayout(self.central_widget)

        # Buttons layout (left side)
        self.button_layout = QVBoxLayout()

        # Add buttons to the left side
        self.add_buttons()

        # Add a spacer to push buttons to the top
        self.button_layout.addStretch()

        # Canvas area
        self.canvas = CanvasWidget(self)
        self.canvas.setFixedSize(600, 600)  # Set a fixed size for the canvas
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.canvas, stretch=1)  # Give canvas higher stretch priority

        # Ensure the canvas reacts to events
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

        # Color Picker Button
        self.color_button = QPushButton("Color Picker", self)
        self.color_button.clicked.connect(self.open_color_picker)
        #self.color_button.setFixedSize(100, 40) -----------see for fixing button sizes
        self.button_layout.addWidget(self.color_button)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_canvas)
        self.button_layout.addWidget(self.save_button)

        # Clear Canvas Button
        self.clear_button = QPushButton("Clear Canvas", self)
        self.clear_button.clicked.connect(self.clear_canvas)
        self.button_layout.addWidget(self.clear_button)

    def activate_pen(self):
        self.current_color = self.pen_color
        self.pen_width = 2

    def activate_eraser(self):
        self.current_color = self.eraser_color
        self.pen_width = 10

    def save_canvas(self):
        # Open a file dialog to save the image
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            self.canvas.canvas_image.save(file_path)

    def clear_canvas(self):
        self.canvas.canvas_image.fill(Qt.white)
        self.canvas.update()

    def open_color_picker(self):
        """Open a color picker dialog and set the pen color."""
        try:
            color = QColorDialog.getColor(initial=self.current_color, parent=self, title="Select Pen Color")
            if color.isValid():
                self.pen_color = color
                self.activate_pen()
                #self.eraser_mode = False  # Ensure eraser mode is off when selecting a color
        except Exception as e:
            print(f"An error occurred in the color picker: {e}")

    def eventFilter(self, obj, event):
        if obj == self.canvas:
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.drawing = True
                    self.last_point = event.pos()  # Start point for drawing
            elif event.type() == event.MouseMove:
                if self.drawing:  # Draw only if left button is pressed
                    painter = QPainter(self.canvas.canvas_image)
                    pen = QPen(self.current_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                    painter.setPen(pen)

                    # Map event position to local canvas coordinates
                    local_pos = event.pos()
                    painter.drawLine(self.last_point, local_pos)  # Draw line
                    self.last_point = local_pos  # Update for next segment
                    self.canvas.update()  # Trigger a canvas repaint
            elif event.type() == event.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.drawing = False
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())