from abc import ABC, abstractmethod


# Base Tool Class
class Tool(ABC):
    def __init__(self, name):
        self.name = name
        self.settings = {}  # Dictionary for storing tool-specific settings

    @abstractmethod
    def use(self):
        """Define how the tool is used (to be implemented by subclasses)."""
        pass

    def update_settings(self, **kwargs):
        """Update tool-specific settings."""
        self.settings.update(kwargs)
        print(f"{self.name} settings updated: {self.settings}")


# Specific Tool Implementations
class Brush(Tool):
    def __init__(self):
        super().__init__("Brush")
        self.settings = {"size": 5, "color": "black"}

    def use(self):
        print("Using Brush with settings:", self.settings)


class Eraser(Tool):
    def __init__(self):
        super().__init__("Eraser")
        self.settings = {"size": 10}

    def use(self):
        print("Using Eraser with settings:", self.settings)


class Fill(Tool):
    def __init__(self):
        super().__init__("Fill")
        self.settings = {"tolerance": 20, "gap_closing": "medium"}

    def use(self):
        print("Using Fill with settings:", self.settings)


class Selection(Tool):
    def __init__(self):
        super().__init__("Selection")
        self.settings = {"type": "rectangle"}

    def use(self):
        print("Using Selection with settings:", self.settings)


# ToolManager Class
class ToolManager:
    def __init__(self):
        # Dictionary to hold single instances of tools
        self.tools = {}
        self.active_tool = None

    def get_tool(self, tool_name):
        """Retrieve a tool instance by name, creating it if it doesn't exist."""
        if tool_name not in self.tools:
            tool_class = globals().get(tool_name)
            if tool_class and issubclass(tool_class, Tool):
                self.tools[tool_name] = tool_class()
            else:
                raise ValueError(f"Tool {tool_name} does not exist.")
        return self.tools[tool_name]

    def set_active_tool(self, tool_name):
        """Set the active tool by name."""
        tool = self.get_tool(tool_name)
        self.active_tool = tool
        print(f"Active tool set to: {tool.name}")

    def use_active_tool(self):
        """Use the currently active tool."""
        if self.active_tool:
            self.active_tool.use()
        else:
            print("No active tool selected.")

    def update_active_tool_settings(self, **kwargs):
        """Update settings for the currently active tool."""
        if self.active_tool:
            self.active_tool.update_settings(**kwargs)
        else:
            print("No active tool selected to update settings.")


# Example Usage
if __name__ == "__main__":
    tool_manager = ToolManager()

    # Activate and use the Brush
    tool_manager.set_active_tool("Brush")
    tool_manager.use_active_tool()
    tool_manager.update_active_tool_settings(size=10, color="red")

    # Activate and use the Eraser
    tool_manager.set_active_tool("Eraser")
    tool_manager.use_active_tool()
    tool_manager.update_active_tool_settings(size=15)

    # Switch back to Brush and verify settings
    tool_manager.set_active_tool("Brush")
    tool_manager.use_active_tool()
