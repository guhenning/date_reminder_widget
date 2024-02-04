import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from db_connection import DatabaseConnection


class OptionWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        with DatabaseConnection() as db_connection:
            settings = db_connection.get_settings()[0]

        self.title("Options")

        # Create language selection list
        self.language_var = tk.StringVar()
        self.language_var.set(
            settings.get("language", "EN")
        )  # Set language from database
        language_label = tk.Label(self, text="Select Language:")
        language_label.pack(pady=5)
        language_list = ttk.Combobox(
            self, values=["EN", "IT", "BR", "ES"], textvariable=self.language_var
        )
        language_list.pack(pady=5)

        # Create font weight selection list
        self.weight_var = tk.StringVar()
        self.weight_var.set(
            settings.get("font_weight", "Normal")
        )  # Set font weight from database
        weight_label = tk.Label(self, text="Select Font Weight:")
        weight_label.pack(pady=5)
        weight_list = ttk.Combobox(
            self, values=["Normal", "Bold"], textvariable=self.weight_var
        )
        weight_list.pack(pady=5)

        # Create color picker
        self.color_var = tk.StringVar()
        self.color_var.set(
            settings.get("text_colour", "black")
        )  # Set text color from database
        color_label = tk.Label(self, text="Select Text Color:")
        color_label.pack(pady=5)
        color_button = tk.Button(self, text="Pick Color", command=self.pick_color)
        color_button.pack(pady=5)

        # Color viewer
        self.color_viewer_frame = tk.Frame(
            self, bg=self.color_var.get(), width=30, height=30
        )
        self.color_viewer_frame.pack(pady=5)
        self.hex_code_label = tk.Label(
            self, text=f"Hex Code: {self.color_var.get()}", font=("Arial", 8)
        )
        self.hex_code_label.pack(pady=5)

        # Add OK and Cancel buttons
        ok_button = tk.Button(self, text="  OK  ", command=self.okay_button_click)
        ok_button.pack(side=tk.RIGHT, padx=(0, 60), anchor=tk.CENTER)
        cancel_button = tk.Button(self, text="Cancel", command=self.cancel_button_click)
        cancel_button.pack(side=tk.LEFT, padx=(60, 0), anchor=tk.CENTER)

        # Calculate the widget start position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_centered = screen_width - 550  # right margin 500
        print(f"X option: {x_centered}")
        y_centered = screen_height - (screen_height - 50)  # top margin 50
        print(f"Y option: {y_centered}")

        # Set the window size and position with equal padding
        self.geometry(f"250x350+{x_centered}+{y_centered}")

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        self.color_var.set(color)  # Set the selected color to the color variable
        self.update_color_viewer()

    def update_color_viewer(self):
        # Update color viewer and hex code label
        self.color_viewer_frame.configure(bg=self.color_var.get())
        self.hex_code_label.configure(text=f"Hex Code: {self.color_var.get()}")

    def okay_button_click(self):
        # Add any necessary processing when OK button is clicked
        with DatabaseConnection() as db_connection:
            # Update values in the database
            db_connection.update_row(
                1,
                {
                    "language": self.language_var.get(),
                    "font_weight": self.weight_var.get(),
                    "text_colour": self.color_var.get(),
                },
            )
        self.destroy()

    def cancel_button_click(self):
        # Add any necessary processing when Cancel button is clicked
        self.destroy()

    def is_open(self):
        try:
            return self.winfo_exists()
        except tk.TclError:
            return False
