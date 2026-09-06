import tkinter as tk
from tkinter import ttk


# Observer Interface
class Observer:
    def update(self):
        pass


# Subject (Observable) Class
class LayeredCanvas:
    def __init__(self):
        self.layers = []
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

    def add_layer(self):
        self.layers.append(f"Layer {len(self.layers) + 1}")
        self.notify_observers()

    def delete_layer(self, index):
        if 0 <= index < len(self.layers):
            del self.layers[index]
            self.notify_observers()


# Observer (UI)
class UIObserver(Observer):
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        # Create main UI layout
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Canvas display (left side)
        self.canvas_display = tk.Canvas(self.main_frame, width=300, height=400, bg="white")
        self.canvas_display.grid(column=0, row=0, rowspan=2, padx=10, pady=10)

        # Layer list and buttons (right side)
        self.layer_listbox = tk.Listbox(self.main_frame, height=20, width=30)
        self.layer_listbox.grid(column=1, row=0, padx=10, pady=10)

        # Add Layer button
        self.add_layer_button = ttk.Button(self.main_frame, text="Add Layer", command=self.add_layer)
        self.add_layer_button.grid(column=1, row=1, sticky=(tk.W, tk.E))

        # Delete Layer button
        self.delete_layer_button = ttk.Button(self.main_frame, text="Delete Selected Layer", command=self.delete_layer)
        self.delete_layer_button.grid(column=1, row=2, sticky=(tk.W, tk.E))

        # Configure resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def add_layer(self):
        self.canvas.add_layer()

    def delete_layer(self):
        # Delete the selected layer
        selected = self.layer_listbox.curselection()
        if selected:
            self.canvas.delete_layer(selected[0])

    def update(self):
        # Update the listbox with the current layers
        self.layer_listbox.delete(0, tk.END)
        for layer in self.canvas.layers:
            self.layer_listbox.insert(tk.END, layer)


# Main Application
def main():
    root = tk.Tk()
    root.title("Observer Pattern Example")

    # Create the observable canvas
    layered_canvas = LayeredCanvas()

    # Create the observer (UI)
    ui = UIObserver(layered_canvas, root)

    # Add observer to the canvas
    layered_canvas.add_observer(ui)

    root.mainloop()


if __name__ == "__main__":
    main()
