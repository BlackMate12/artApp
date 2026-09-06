class User:
    """
    Base class representing a generic user of the application.
    """
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type

    def login(self, username, password):
        """
        Simulate user login.
        :param username: Username entered by the user
        :param password: Password entered by the user
        :return: True if login is successful, False otherwise
        """
        return self.username == username and self.password == password

    def logout(self):
        """
        Simulate user logout.
        """
        print(f"{self.username} has logged out.")


class Artist(User):
    """
    Represents an artist user, who can create and edit canvases.
    """
    def __init__(self, username, password):
        super().__init__(username, password, "Artist")

    def select_tool(self, tool):
        """
        Simulate selecting a tool.
        :param tool: Tool to be selected
        """
        print(f"{self.username} selected the tool: {tool}")

    def create_canvas(self):
        """
        Simulate creating a new canvas.
        :return: A new Canvas object
        """
        from canvas import Canvas  # Import here to avoid circular imports
        print(f"{self.username} created a new canvas.")
        return Canvas()

    def edit_layer(self, layer, operation):
        """
        Simulate editing a layer.
        :param layer: The layer to edit
        :param operation: A string describing the operation
        """
        print(f"{self.username} performed '{operation}' on Layer {layer.id}.")


class Admin(User):
    """
    Represents an admin user, who can manage other users and configure the app.
    """
    def __init__(self, username, password):
        super().__init__(username, password, "Admin")

    def manage_users(self, user_list):
        """
        Simulate managing users (e.g., viewing or removing them).
        :param user_list: A list of User objects
        """
        print(f"{self.username} is managing users.")
        for user in user_list:
            print(f"- {user.username} ({user.user_type})")

    def configure_app(self, setting, value):
        """
        Simulate configuring application settings.
        :param setting: The setting to configure
        :param value: The new value for the setting
        """
        print(f"{self.username} set {setting} to {value}.")


class Viewer(User):
    """
    Represents a viewer user, who can only view canvases or files.
    """
    def __init__(self, username, password):
        super().__init__(username, password, "Viewer")

    def open_file(self, filename):
        """
        Simulate opening a file for viewing.
        :param filename: The name of the file to open
        """
        print(f"{self.username} is viewing the file: {filename}.")
