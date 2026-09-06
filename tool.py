class Tool:
    """
    Base class for all tools.
    """
    def __init__(self, name, size=1, color="#000000"):
        self.name = name
        self.size = size
        self.color = color

    def apply(self, x, y):
        """
        Apply the tool at the given (x, y) position.
        To be overridden by subclasses.
        """
        raise NotImplementedError("The 'apply' method must be implemented by subclasses.")

    def select_tool(self):
        """
        Simulate selecting the tool.
        """
        print(f"Tool '{self.name}' selected.")

    def __str__(self):
        return f"{self.name} Tool (Size: {self.size}, Color: {self.color})"


class Brush(Tool):
    """
    A brush tool for painting on the canvas.
    """
    def __init__(self, size=5, color="#000000"):
        super().__init__(name="Brush", size=size, color=color)

    def apply(self, x, y):
        print(f"Brush applied at ({x}, {y}) with size {self.size} and color {self.color}.")


class Eraser(Tool):
    """
    An eraser tool for removing parts of a layer.
    """
    def __init__(self, size=10):
        super().__init__(name="Eraser", size=size, color="#FFFFFF")  # Erasers usually "erase" to white.

    def apply(self, x, y):
        print(f"Eraser applied at ({x}, {y}) with size {self.size}.")


class Selection(Tool):
    """
    A selection tool for selecting parts of a layer.
    """
    def __init__(self):
        super().__init__(name="Selection")

    def apply(self, x, y):
        print(f"Selection made at ({x}, {y}).")

class ToolManager:
    """Manages all tools and handles tool selection."""
    def __init__(self):
        self.tools = {
            "brush": Brush(),
            "eraser": Eraser(),
            # Add more tools as needed...
        }
        self.current_tool = None

    def select_tool(self, tool_name):
        """Select a tool by its name."""
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]
            print(f"Selected tool: {self.current_tool.name}")
        else:
            print(f"Tool '{tool_name}' not found.")

    def get_current_tool(self):
        """Return the currently selected tool."""
        return self.current_tool

# Example of tools being instantiated and used:
if __name__ == "__main__":
    brush = Brush(size=10, color="#FF5733")
    eraser = Eraser(size=15)
    selection = Selection()

    brush.select_tool()
    brush.apply(100, 200)

    eraser.select_tool()
    eraser.apply(150, 250)

    selection.select_tool()
    selection.apply(300, 400)
