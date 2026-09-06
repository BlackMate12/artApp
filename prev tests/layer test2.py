import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QColorDialog, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QPen, QImage, QColor
from PyQt5.QtCore import Qt, QPoint


class Layer:
    def __init__(self, width, height, color):
        self.image = QImage(width, height, QImage.Format_ARGB32)
        self.image.fill(color)  # Start with a transparent layer
        self.visible = True


class LayeredCanvas(QWidget):
    def __init__(self, update_callback, parent=None):
        super().__init__(parent)
        self.layers = []  # List of layers
        self.current_layer_index = -1  # No active layer initially
        self.width = 1600
        self.height = 950
        self.setFixedSize(self.width, self.height)

        self.update_callback = update_callback

        self.add_layer(skip_callback=True)  # Start with one layer

        #new_layer = Layer(self.width, self.height, Qt.white)
        #self.layers.append(new_layer)
        #self.current_layer_index = len(self.layers) - 1
        #self.update()

    def add_layer(self, skip_callback=False):
        """Add a new transparent layer."""
        new_layer = Layer(self.width, self.height, Qt.transparent)
        self.layers.append(new_layer)
        self.current_layer_index = len(self.layers) - 1
        self.update()
        if not skip_callback and self.update_callback:
            self.update_callback()

    def delete_layer(self):
        """Delete the currently active layer."""
        if self.current_layer_index != -1:
            self.layers.pop(self.current_layer_index)
            self.current_layer_index = max(0, len(self.layers) - 1)  # Update index
            self.update()
            self.update_callback()

    def paintEvent(self, event):
        """Paint all visible layers in order."""
        canvas_painter = QPainter(self)

        base_image = QImage(self.width, self.height, QImage.Format_ARGB32)
        base_image.fill(Qt.white)
        canvas_painter.drawImage(0, 0, base_image)

        for layer in self.layers:
            if layer.visible:
                canvas_painter.drawImage(0, 0, layer.image)

    def toggle_layer_visibility(self, index):
        """Toggle the visibility of a layer."""
        if 0 <= index < len(self.layers):
            self.layers[index].visible = not self.layers[index].visible
            self.update()
            self.update_callback()


class ArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Art App with Layers")
        self.setGeometry(100, 100, 1000, 600)

        # Drawing properties
        self.drawing = False
        self.last_point = QPoint()
        self.pen_color = Qt.black
        self.eraser_color = Qt.white
        self.current_color = self.pen_color
        self.pen_width = 5

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Canvas
        self.canvas = LayeredCanvas(self.update_layer_list, self)

        # Left panel for buttons and layers
        self.left_panel = QVBoxLayout()
        self.right_panel = QVBoxLayout()

        # Add buttons to left panel
        self.add_buttons()

        # Add layer manager to the left panel
        self.add_layer_manager()

        # Add a spacer to push buttons and layers to the top
        self.left_panel.addStretch() #???

        self.main_layout.addLayout(self.left_panel)
        self.main_layout.addWidget(self.canvas, stretch=1)
        self.main_layout.addLayout(self.right_panel)

        # Ensure the canvas reacts to events
        self.canvas.installEventFilter(self)

    def add_buttons(self):
        # Pen Button
        self.pen_button = QPushButton("Pen", self)
        self.pen_button.clicked.connect(self.activate_pen)
        self.left_panel.addWidget(self.pen_button)

        # Eraser Button
        self.eraser_button = QPushButton("Eraser", self)
        self.eraser_button.clicked.connect(self.activate_eraser)
        self.left_panel.addWidget(self.eraser_button)

        # Color Picker Button
        self.color_button = QPushButton("Color Picker", self)
        self.color_button.clicked.connect(self.open_color_picker)
        self.left_panel.addWidget(self.color_button)

        # Save Button
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_canvas)
        self.left_panel.addWidget(self.save_button)

        # Clear Canvas Button
        self.clear_button = QPushButton("Clear Layer", self)
        self.clear_button.clicked.connect(self.clear_canvas)
        self.left_panel.addWidget(self.clear_button)

    def add_layer_manager(self):
        # Add Layer Button
        self.add_layer_button = QPushButton("Add Layer", self)
        self.add_layer_button.clicked.connect(self.canvas.add_layer)
        self.right_panel.addWidget(self.add_layer_button)

        # Delete Layer Button
        self.delete_layer_button = QPushButton("Delete Layer", self)
        self.delete_layer_button.clicked.connect(self.canvas.delete_layer)
        self.right_panel.addWidget(self.delete_layer_button)

        # Layer List
        self.layer_list = QListWidget(self)
        self.layer_list.currentRowChanged.connect(self.select_layer)
        self.right_panel.addWidget(self.layer_list)
        self.update_layer_list()

    def activate_pen(self):
        self.current_color = self.pen_color
        self.pen_width = 2

    def activate_eraser(self):
        self.current_color = self.eraser_color
        self.pen_width = 10

    def save_canvas(self):
        # Save flattened image (all layers combined)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            flattened_image = QImage(self.canvas.width, self.canvas.height, QImage.Format_ARGB32)
            flattened_image.fill(Qt.transparent)

            painter = QPainter(flattened_image)
            for layer in self.canvas.layers:
                if layer.visible:
                    painter.drawImage(0, 0, layer.image)
            painter.end()

            flattened_image.save(file_path)

    def clear_canvas(self):
        if self.canvas.current_layer_index != -1:
            self.canvas.layers[self.canvas.current_layer_index].image.fill(Qt.transparent)
            self.canvas.update()

    def open_color_picker(self):
        """Open a color picker dialog and set the pen color."""
        color = QColorDialog.getColor(initial=self.current_color, parent=self, title="Select Pen Color")
        if color.isValid():
            self.pen_color = color
            self.activate_pen()

    def select_layer(self, index):
        """Switch the active layer."""
        self.canvas.current_layer_index = index

    def update_layer_list(self):
        """Update the QListWidget to reflect the current layers."""
        self.layer_list.clear()
        for i, layer in enumerate(self.canvas.layers):
            item = QListWidgetItem(f"Layer {i + 1}")
            if not layer.visible:
                item.setForeground(Qt.gray)  # Grayed out for hidden layers
            self.layer_list.addItem(item)
        if self.canvas.current_layer_index != -1:
            self.layer_list.setCurrentRow(self.canvas.current_layer_index)

    def eventFilter(self, obj, event):
        if obj == self.canvas:
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.drawing = True
                    self.last_point = event.pos()
            elif event.type() == event.MouseMove:
                if self.drawing and self.canvas.current_layer_index != -1:
                    current_layer = self.canvas.layers[self.canvas.current_layer_index]
                    painter = QPainter(current_layer.image)
                    if self.current_color == self.eraser_color:  # Check if the eraser is active
                        painter.setCompositionMode(QPainter.CompositionMode_Clear)
                        pen = QPen(Qt.transparent, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                    else:
                        pen = QPen(self.current_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                    painter.setPen(pen)
                    painter.drawLine(self.last_point, event.pos())
                    self.last_point = event.pos()
                    self.canvas.update()
            elif event.type() == event.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.drawing = False
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtApp()
    window.show()
    sys.exit(app.exec_())
