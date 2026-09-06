import tkinter as tk
from canvas import Canvas
from toolmanager import ToolManager


class ArtAppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professional Art Program")
        self.geometry("1200x800")
        self.configure(bg="gray20")

        # Initialize ToolManager
        self.tool_manager = ToolManager()

        # Layout: Left Toolbar
        self.create_toolbar()

        # Layout: Tool Options Panel
        self.create_tool_options_panel()

        # Layout: Canvas Area
        self.canvas_frame = tk.Frame(self, bg="black", width=800, height=600)
        self.canvas_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.canvas = Canvas(800, 600)
        self.canvas.pack(fill="both", expand=True)

        # Layout: Right Panel
        self.create_right_panel()

        # Configure grid layout
        self.columnconfigure(1, weight=1)  # Canvas area expands horizontally
        self.rowconfigure(0, weight=1)    # Canvas area expands vertically

    def create_toolbar(self):
        """Create the thin vertical toolbar on the left."""
        toolbar = tk.Frame(self, bg="gray30", width=50, relief=tk.RAISED, bd=2)
        toolbar.grid(row=0, column=0, sticky="ns")

        # Add buttons for each tool
        tools = ["Brush", "Eraser", "Fill", "Hand", "Selection"]
        for tool in tools:
            button = tk.Button(
                toolbar,
                text=tool[0],  # Display the first letter
                width=2,
                height=2,
                bg="gray40",
                fg="white",
                command=lambda t=tool: self.select_tool(t),
            )
            button.pack(pady=5)

    def create_tool_options_panel(self):
        """Create the tool options panel next to the toolbar."""
        self.tool_options_panel = tk.Frame(self, bg="gray25", height=50)
        self.tool_options_panel.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.update_tool_options_panel()

    def update_tool_options_panel(self):
        """Update the tool options panel dynamically based on the selected tool."""
        for widget in self.tool_options_panel.winfo_children():
            widget.destroy()

        current_tool = self.tool_manager.active_tool
        label = tk.Label(
            self.tool_options_panel,
            text=f"Tool: {current_tool.name}",
            fg="white",
            bg="gray25",
            font=("Arial", 12),
        )
        label.pack(side="left", padx=10)

        # Example: Add size adjustment slider for Brush
        if current_tool.name == "Brush":
            slider = tk.Scale(
                self.tool_options_panel,
                from_=1,
                to=50,
                orient="horizontal",
                label="Size",
                bg="gray25",
                fg="white",
            )
            slider.pack(side="left", padx=10)

    def select_tool(self, tool_name):
        """Handle tool selection from the toolbar."""
        self.tool_manager.select_tool(tool_name)
        self.update_tool_options_panel()
        print(f"Selected tool: {tool_name}")

    def create_right_panel(self):
        """Create the right-side panel for layers and canvas preview."""
        right_panel = tk.Frame(self, bg="gray30", width=200, relief=tk.RAISED, bd=2)
        right_panel.grid(row=0, column=2, sticky="ns")

        # Layer Management Section
        layer_label = tk.Label(
            right_panel, text="Layers", bg="gray30", fg="white", font=("Arial", 12)
        )
        layer_label.pack(pady=5)

        self.layer_listbox = tk.Listbox(
            right_panel, bg="gray25", fg="white", height=10, selectbackground="gray50"
        )
        self.layer_listbox.pack(padx=10, pady=5, fill="x")

        # Add/Delete Layer Buttons
        add_button = tk.Button(
            right_panel,
            text="Add Layer",
            bg="gray40",
            fg="white",
            command=self.add_layer,
        )
        add_button.pack(pady=5)

        delete_button = tk.Button(
            right_panel,
            text="Delete Layer",
            bg="gray40",
            fg="white",
            command=self.delete_layer,
        )
        delete_button.pack(pady=5)

        # Canvas Preview Section
        preview_label = tk.Label(
            right_panel, text="Canvas Preview", bg="gray30", fg="white", font=("Arial", 12)
        )
        preview_label.pack(pady=10)

        self.canvas_preview = tk.Canvas(right_panel, width=150, height=150, bg="white")
        self.canvas_preview.pack(padx=10, pady=5)

    def add_layer(self):
        """Add a new layer to the canvas and update the layer list."""
        self.canvas.add_layer()
        self.update_layer_list()

    def delete_layer(self):
        """Delete the selected layer."""
        selected_index = self.layer_listbox.curselection()
        if selected_index:
            self.canvas.remove_layer(selected_index[0])
            self.update_layer_list()

    def update_layer_list(self):
        """Refresh the layer list to show current layers."""
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.canvas.layers):
            self.layer_listbox.insert(tk.END, f"Layer {i + 1}")


if __name__ == "__main__":
    app = ArtAppUI()
    app.mainloop()
