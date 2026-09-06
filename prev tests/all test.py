import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QColorDialog, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QPen, QImage, QColor
from PyQt5.QtCore import Qt, QPoint, QRect


class Layer:
    def __init__(self, width, height, color):
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.image.fill(color)  # Transparent background
        self.visible = True


class LayeredCanvas(QWidget):
    def __init__(self, update_callback, parent=None, skip_initial_update=False):
        super().__init__(parent)
        self.layers = []
        self.current_layer_index = -1
        self.width = 600
        self.height = 600
        self.setFixedSize(self.width, self.height)

        self.update_callback = update_callback
        self.selection_rect = None
        self.is_dragging = False
        self.drag_offset = QPoint()
        self.original_image = None

        # Add an initial transparent layer, but skip callback if specified
        self.add_layer(skip_callback=skip_initial_update)

    def add_layer(self, skip_callback=False):
        """Add a new transparent layer."""
        new_layer = Layer(self.width, self.height, Qt.transparent)
        self.layers.append(new_layer)
        self.current_layer_index = len(self.layers) - 1
        self.update()
        if not skip_callback and self.update_callback:
            self.update_callback()

    # Other LayeredCanvas methods remain unchanged


    def delete_layer(self):
        if self.current_layer_index != -1:
            self.layers.pop(self.current_layer_index)
            self.current_layer_index = max(0, len(self.layers) - 1)
            self.update()
            self.update_callback()

    def toggle_layer_visibility(self, index):
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible
            self.update()
            self.update_callback()

    def paintEvent(self, event):
        painter = QPainter(self)
        base_image = QImage(self.width, self.height, QImage.Format_ARGB32)
        base_image.fill(Qt.white)
        painter.drawImage(0, 0, base_image)

        for layer in self.layers:
            if layer.visible:
                painter.drawImage(0, 0, layer.image)

        if self.selection_rect:
            pen = QPen(Qt.red, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_layer_index != -1:
            if self.current_tool == "brush":
                self.drawing = True
                self.last_point = event.pos()
            elif self.current_tool == "eraser":
                self.drawing = True
                self.last_point = event.pos()
            elif self.current_tool == "fill":
                self.fill(event.pos(), self.pen_color)
            elif self.current_tool == "select":
                self.selection_rect = QRect(event.pos(), event.pos())

    def mouseMoveEvent(self, event):
        if self.drawing and self.current_layer_index != -1:
            if self.current_tool in ["brush", "eraser"]:
                painter = QPainter(self.layers[self.current_layer_index].image)
                color = self.pen_color if self.current_tool == "brush" else QColor(0, 0, 0, 0)  # Transparent for eraser
                pen = QPen(color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setPen(pen)
                painter.drawLine(self.last_point, event.pos())
                self.last_point = event.pos()
                self.update()
        elif self.current_tool == "select" and self.selection_rect:
            self.selection_rect.setBottomRight(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def fill(self, point, color):
        if self.current_layer_index == -1:
            return
        image = self.layers[self.current_layer_index].image
        target_color = image.pixelColor(point)
        if target_color == color:
            return

        def is_within_bounds(pt):
            return 0 <= pt.x() < image.width() and 0 <= pt.y() < image.height()

        stack = [point]
        while stack:
            current = stack.pop()
            if not is_within_bounds(current) or image.pixelColor(current) != target_color:
                continue
            image.setPixelColor(current, color)
            stack.extend([QPoint(current.x() + 1, current.y()), QPoint(current.x() - 1, current.y()),
                          QPoint(current.x(), current.y() + 1), QPoint(current.x(), current.y() - 1)])
        self.update()


class ArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art App with Layers")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Initialize layer list first
        self.layer_list = None
        self.add_layer_manager()

        # Initialize canvas with skip_initial_update=True
        self.canvas = LayeredCanvas(self.update_layer_list, self, skip_initial_update=True)

        # Left panel for tools
        self.left_panel = QVBoxLayout()
        self.add_tool_buttons()

        # Add everything to the layout
        self.main_layout.addLayout(self.left_panel)
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addLayout(self.right_panel)

        # Now that canvas is initialized, manually trigger the update
        self.update_layer_list()


    def add_tool_buttons(self):
        self.brush_button = QPushButton("Brush")
        self.brush_button.clicked.connect(self.activate_brush)
        self.left_panel.addWidget(self.brush_button)

        self.eraser_button = QPushButton("Eraser")
        self.eraser_button.clicked.connect(self.activate_eraser)
        self.left_panel.addWidget(self.eraser_button)

        self.fill_button = QPushButton("Fill")
        self.fill_button.clicked.connect(self.activate_fill)
        self.left_panel.addWidget(self.fill_button)

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.activate_select)
        self.left_panel.addWidget(self.select_button)

    def add_layer_manager(self):
        self.add_layer_button = QPushButton("Add Layer")
        self.add_layer_button.clicked.connect(self.add_new_layer)
        self.right_panel.addWidget(self.add_layer_button)

        self.delete_layer_button = QPushButton("Delete Layer")
        self.delete_layer_button.clicked.connect(self.delete_layer)
        self.right_panel.addWidget(self.delete_layer_button)

        self.layer_list = QListWidget()
        self.layer_list.currentRowChanged.connect(self.select_layer)
        self.right_panel.addWidget(self.layer_list)

    def update_layer_list(self):
        self.layer_list.clear()
        for i, layer in enumerate(self.canvas.layers):
            item = QListWidgetItem(f"Layer {i + 1}")
            if not layer.visible:
                item.setForeground(Qt.gray)
            self.layer_list.addItem(item)
        if self.canvas.current_layer_index != -1:
            self.layer_list.setCurrentRow(self.canvas.current_layer_index)

    def activate_brush(self):
        self.canvas.current_tool = "brush"

    def activate_eraser(self):
        self.canvas.current_tool = "eraser"

    def activate_fill(self):
        self.canvas.current_tool = "fill"

    def activate_select(self):
        self.canvas.current_tool = "select"

    def select_layer(self, index):
        self.canvas.current_layer_index = index

    def add_new_layer(self):
        self.canvas.add_layer()

    def delete_layer(self):
        self.canvas.delete_layer()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())
