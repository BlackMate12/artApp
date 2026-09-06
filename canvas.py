import tkinter as tk
from layer import Layer  # Assuming Layer is in a separate module

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []
        self.zoom_level = 1.0  # Default zoom level (100%)
        self.max_zoom = 5.0    # Maximum zoom (500%)
        self.min_zoom = 0.1    # Minimum zoom (10%)
        self.offset_x = 0      # Horizontal pan offset
        self.offset_y = 0      # Vertical pan offset

        # Create a Tkinter Canvas widget
        self.tk_canvas = tk.Canvas(width=self.width, height=self.height, bg="white")
        self.tk_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.tk_canvas.bind("<Button-1>", self.start_drag)
        self.tk_canvas.bind("<B1-Motion>", self.perform_drag)

        # Variables to track dragging
        self.last_mouse_x = None
        self.last_mouse_y = None

    def add_layer(self):
        """Add a new empty layer to the canvas."""
        layer = Layer(self.width, self.height)
        self.layers.append(layer)
        print(f"Added new layer. Total layers: {len(self.layers)}")

    def remove_layer(self, index):
        """Remove a layer by index."""
        if 0 <= index < len(self.layers):
            del self.layers[index]
            print(f"Removed layer at index {index}. Total layers: {len(self.layers)}")
        else:
            print("Invalid layer index")

    def on_mouse_wheel(self, event):
        """Handle zooming in and out with the mouse wheel."""
        # Determine zoom direction
        zoom_in = event.delta > 0

        # Calculate new zoom level
        if zoom_in:
            new_zoom = min(self.zoom_level * 1.1, self.max_zoom)
        else:
            new_zoom = max(self.zoom_level / 1.1, self.min_zoom)

        # Calculate zoom scaling factor
        scale = new_zoom / self.zoom_level

        # Calculate mouse position relative to canvas
        mouse_x = self.tk_canvas.canvasx(event.x)
        mouse_y = self.tk_canvas.canvasy(event.y)

        # Adjust offsets to zoom towards the cursor
        self.offset_x = (mouse_x - self.offset_x) * (1 - scale) + self.offset_x
        self.offset_y = (mouse_y - self.offset_y) * (1 - scale) + self.offset_y

        self.zoom_level = new_zoom
        self.redraw_canvas()

    def start_drag(self, event):
        """Record the starting point for dragging."""
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def perform_drag(self, event):
        """Handle dragging (panning) of the canvas."""
        if self.last_mouse_x is not None and self.last_mouse_y is not None:
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y

            self.offset_x += dx
            self.offset_y += dy

            self.last_mouse_x = event.x
            self.last_mouse_y = event.y

            self.redraw_canvas()

    def redraw_canvas(self):
        """Redraw the canvas with the current zoom level and offsets."""
        self.tk_canvas.delete("all")  # Clear the canvas

        # Apply transformations and draw layers
        for layer in self.layers:
            # Draw each layer with current zoom and offsets
            layer_image = layer.get_content()  # Assuming Layer has a `get_image` method
            if layer_image:
                self.tk_canvas.create_image(
                    self.offset_x, self.offset_y,
                    anchor=tk.NW,
                    image=layer_image.zoom(int(self.zoom_level * 100))
                )

    def pack(self, **kwargs):
        """Expose the pack method for embedding the canvas in a Tkinter window."""
        self.tk_canvas.pack(**kwargs)
