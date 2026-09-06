import tkinter as tk
from tkinter import ttk
import sys
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageTk
from PyQt5.QtGui import QImage

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

    def add_layer(self, name):
        """Add a new empty layer to the canvas."""
        #layer_name = name or f"Layer {len(self.layers) + 1}"
        layer = Layer(name, self.width, self.height)
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
        zoom_in = event.delta > 0
        new_zoom = self.zoom_level * (1.1 if zoom_in else 0.9)
        new_zoom = max(self.min_zoom, min(new_zoom, self.max_zoom))

        # Calculate the scaling factor
        scale = new_zoom / self.zoom_level

        # Adjust offsets to keep zoom centered on cursor
        mouse_x = self.tk_canvas.canvasx(event.x)
        mouse_y = self.tk_canvas.canvasy(event.y)
        self.offset_x -= mouse_x * (scale - 1)
        self.offset_y -= mouse_y * (scale - 1)

        # Update zoom level and redraw
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

        # Store references to prevent garbage collection
        if not hasattr(self, '_image_refs'):
            self._image_refs = []
        self._image_refs.clear()

        # Apply transformations and draw layers
        for layer in self.layers:
            if not layer.visible:
                continue

            # Convert QImage to PIL Image
            qimage = layer.get_content()
            width = qimage.width()
            height = qimage.height()
            buffer = qimage.bits().asstring(width * height * 4)
            pil_image = Image.frombytes("RGBA", (width, height), buffer)

            # Resize the image for the current zoom level
            zoomed_width = int(width * self.zoom_level)
            zoomed_height = int(height * self.zoom_level)
            pil_image = pil_image.resize((zoomed_width, zoomed_height), Image.LANCZOS)

            # Convert to Tkinter-compatible PhotoImage
            tk_image = ImageTk.PhotoImage(pil_image)

            # Draw the image with the current offsets
            self.tk_canvas.create_image(
                self.offset_x, self.offset_y, anchor=tk.NW, image=tk_image
            )

            # Keep reference to prevent garbage collection
            self._image_refs.append(tk_image)

    def pack(self, **kwargs):
        """Expose the pack method for embedding the canvas in a Tkinter window."""
        self.tk_canvas.pack(**kwargs)

class Tool:
    def __init__(self, name):
        self.name = name

    def on_mouse_down(self, event, canvas):
        """Called when the mouse is pressed on the canvas."""
        pass

    def on_mouse_move(self, event, canvas):
        """Called when the mouse is moved with the button held down."""
        pass

    def on_mouse_up(self, event, canvas):
        """Called when the mouse button is released."""
        pass

class BrushTool(Tool):
    def __init__(self):
        super().__init__("Brush")
        self.last_x = None
        self.last_y = None

    def on_mouse_down(self, event, canvas):
        self.last_x, self.last_y = event.x, event.y

    def on_mouse_move(self, event, canvas):
        if self.last_x is not None and self.last_y is not None:
            canvas.tk_canvas.create_line(
                self.last_x, self.last_y, event.x, event.y, fill="black", width=3
            )
            self.last_x, self.last_y = event.x, event.y

    def on_mouse_up(self, event, canvas):
        self.last_x, self.last_y = None, None

class EraserTool(Tool):
    def __init__(self):
        super().__init__("Eraser")

    def on_mouse_down(self, event, canvas):
        canvas.tk_canvas.create_rectangle(
            event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="white", outline=""
        )

    def on_mouse_move(self, event, canvas):
        canvas.tk_canvas.create_rectangle(
            event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="white", outline=""
        )

class ToolManager:
    def __init__(self):
        self.tools = {}
        self.active_tool = None

    def add_tool(self, tool):
        self.tools[tool.name] = tool

    def set_active_tool(self, tool_name):
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]
            print(f"Switched to tool: {tool_name}")
        else:
            print(f"Tool '{tool_name}' not found!")

    def handle_mouse_down(self, event, canvas):
        if self.active_tool:
            self.active_tool.on_mouse_down(event, canvas)

    def handle_mouse_move(self, event, canvas):
        if self.active_tool:
            self.active_tool.on_mouse_move(event, canvas)

    def handle_mouse_up(self, event, canvas):
        if self.active_tool:
            self.active_tool.on_mouse_up(event, canvas)


class ArtAppUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Art Application")
        self.state('zoomed')

        self.tool_manager = ToolManager()  # Initialize ToolManager

        # Add tools to the manager
        self.tool_manager.add_tool(BrushTool())
        self.tool_manager.add_tool(EraserTool())

        # Example: Set default tool
        self.tool_manager.set_active_tool("Brush")

        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        left_pane = ttk.PanedWindow(main_pane, orient=tk.HORIZONTAL)
        main_pane.add(left_pane, weight=1)

        tools_frame = ttk.LabelFrame(left_pane, text="Tools", width=50)
        left_pane.add(tools_frame)

        tool_options_frame = ttk.LabelFrame(left_pane, text="Tool Options", width=125)
        left_pane.add(tool_options_frame)

        canvas_placeholder = ttk.Frame(main_pane, relief=tk.SUNKEN, style="CanvasPlaceholder.TFrame")
        main_pane.add(canvas_placeholder, weight=100)

        right_frame = ttk.LabelFrame(main_pane, text="Layers", width=125)
        main_pane.add(right_frame)

        self.create_tools_pane(tools_frame)

        self.create_tool_options_pane(tool_options_frame)

        self.canvas = Canvas(800, 600)  # Initialize Canvas
        self.canvas.pack(expand=True, fill=tk.BOTH)
        canvas_placeholder.bind("<Configure>", lambda e: self.center_canvas(canvas_placeholder))

        self.create_layers_pane(right_frame)

        self.configure_styles()

    def create_tools_pane(self, frame):

        # Example Tool Buttons
        for tool in ["Brush", "Eraser", "Fill", "Color Picker", "Selection"]:
            button = ttk.Button(frame, text=tool)
            button.pack(fill=tk.X, pady=2)

    def create_tool_options_pane(self, frame):
        # Example Options
        ttk.Label(frame, text="Option 1:").pack(anchor="w", padx=5)
        ttk.Entry(frame).pack(fill=tk.X, padx=5)

        ttk.Label(frame, text="Option 2:").pack(anchor="w", padx=5)
        ttk.Entry(frame).pack(fill=tk.X, padx=5)

    def create_layers_pane(self, frame):
        """Create the layers pane."""

        # Frame for Listbox and Scrollbar
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Listbox for layers
        self.layers_listbox = tk.Listbox(listbox_frame)
        self.layers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #layers_listbox.grid(row=0, column=0, padx=5, pady=5)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.layers_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #scrollbar.grid(row=0, column=1, padx=5, pady=5)

        self.layers_listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(frame, text="Add Layer", command=self.add_layer).pack(fill=tk.X, pady=2)
        #button.pack(fill=tk.X, pady=2)
        #button.grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(frame, text="Delete Layer", command=self.delete_layer).pack(fill=tk.X, pady=2)
        #button.grid(row=2, column=0, padx=5, pady=5)

        self.layers_listbox.insert(tk.END, f"Layer 1")
        self.canvas.add_layer("Layer 1")

    def center_canvas(self, placeholder):
        placeholder_width = placeholder.winfo_width()
        placeholder_height = placeholder.winfo_height()

        canvas_width = self.canvas.tk_canvas.winfo_reqwidth()
        canvas_height = self.canvas.tk_canvas.winfo_reqheight()

        x_offset = max((placeholder_width - canvas_width) // 2, 0)
        y_offset = max((placeholder_height - canvas_height) // 2, 0)

        self.canvas.tk_canvas.place(x=400, y=100)

    def add_layer(self):
        name = f"Layer {len(self.canvas.layers) + 1}"
        self.canvas.add_layer(name)
        self.layers_listbox.insert(tk.END, name)

    def delete_layer(self):
        selected_index = self.layers_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.layers_listbox.delete(index)
            self.canvas.remove_layer(index)

    def configure_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        style.configure("CanvasPlaceholder.TFrame", background="#e0e0e0", relief=tk.SUNKEN)


if __name__ == "__main__":
    app = ArtAppUI()
    app.mainloop()
