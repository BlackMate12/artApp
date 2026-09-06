import json
from canvas import Canvas


class File:
    """
    A class responsible for saving and loading canvas data.
    """
    def __init__(self, filename):
        self.filename = filename

    def save_canvas(self, canvas: Canvas):
        """
        Save the canvas to a JSON file, including all layers and their properties.
        """
        canvas_data = {
            "width": canvas.width,
            "height": canvas.height,
            "bg_color": canvas.bg_color,
            "layers": [
                {
                    "id": layer.id,
                    "visible": layer.visible,
                    "opacity": layer.opacity
                }
                for layer in canvas.layers
            ]
        }

        try:
            with open(self.filename, "w") as file:
                json.dump(canvas_data, file, indent=4)
            print(f"Canvas successfully saved to {self.filename}.")
        except Exception as e:
            print(f"Failed to save canvas: {e}")

    def load_canvas(self):
        """
        Load the canvas from a JSON file.
        """
        try:
            with open(self.filename, "r") as file:
                canvas_data = json.load(file)

            canvas = Canvas(
                width=canvas_data["width"],
                height=canvas_data["height"],
                bg_color=canvas_data["bg_color"]
            )

            for layer_data in canvas_data["layers"]:
                canvas.add_layer(
                    layer_id=layer_data["id"],
                    visible=layer_data["visible"],
                    opacity=layer_data["opacity"]
                )

            print(f"Canvas successfully loaded from {self.filename}.")
            return canvas

        except FileNotFoundError:
            print(f"File {self.filename} not found.")
            return None
        except Exception as e:
            print(f"Failed to load canvas: {e}")
            return None
