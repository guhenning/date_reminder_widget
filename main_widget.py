import tkinter as tk
from datetime import datetime
import csv
from option_window import OptionWindow
from add_date_window import AddDateWindow
from csv_editor import CSVEditorWindow
from db_connection import DatabaseConnection
from utils import resize_icon
from pathlib import Path

icons_path = Path("icons")


class DraggableWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        with DatabaseConnection() as db_connection:
            # Connect to the SQLite database and get settings
            self.settings = db_connection.get_settings()[0]

        self.title("")  # Set an empty title to remove the default label
        self.overrideredirect(True)  # Remove window borders

        opacity_percentage_dict = {f"{i}%": i / 100 for i in range(10, 101, 10)}
        self.attributes(
            "-alpha", opacity_percentage_dict[self.settings["opacity"]]
        )  # Set window transparency

        # Load data from the CSV file
        self.data = self.load_data("dates.csv")

        # language
        self.language = self.settings["language"]
        self.translations = {
            "EN": {
                "name": "Name",
                "date": "Date",
                "description": "Description",
                "no_date": "Oh No!! No Dates Found, Add New Dates!!!",
            },
            "IT": {
                "name": "Nome",
                "date": "Data",
                "description": "Descrizione",
                "no_date": "Oh No!! Nessuna data trovata, aggiungi nuove date!!!",
            },
            "BR": {
                "name": "Nome",
                "date": "Data",
                "description": "Descrição",
                "no_date": "Oh Não!! Nenhuma data encontrada, adicione novas datas!!!",
            },
            "ES": {
                "name": "Nombre",
                "date": "Fecha",
                "description": "Descripción",
                "no_date": "Oh No!! No se encontraron fechas, ¡Agrega nuevas fechas!!!",
            },
        }
        self.translated_text = self.translations[self.language]

        # Find all entries with the nearest date
        nearest_dates = self.find_nearest_dates()

        self.set_widget_size(len(nearest_dates))

        # Create a frame for centering labels
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.X)

        custom_font = ("Arial", 10, self.settings["font_weight"].lower())

        # if len is 0 dont have any dates on file as user to add!
        if len(nearest_dates) == 0:
            # Display information for all entries with the nearest date
            label = tk.Label(
                frame,
                text=f"{self.translated_text['no_date']}",
                anchor="center",
                justify="center",
                wraplength=200,
                font=custom_font,
                fg=self.settings["text_colour"],
            )
            label.pack(pady=10)

        # Display information for all entries with the nearest date
        for nearest_date, nearest_data in nearest_dates:
            label_text = f"{self.translated_text['name']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['date']}: {nearest_data[self.translated_text['date']]}\n{self.translated_text['description']}: {nearest_data[self.translated_text['description']]}"
            label = tk.Label(
                frame,
                text=label_text,
                anchor="center",
                justify="center",
                wraplength=200,
                font=custom_font,
                fg=self.settings["text_colour"],
            )
            label.pack(pady=10)

        ##############################################################################
        # Hover Buttons
        # Create a frame the buttons
        self.initialize_hover_buttons()
        # Bind events to show and hide the buttons
        self.bind("<Enter>", self.show_buttons)
        self.bind("<Leave>", self.hide_buttons)

        ##############################################################################

        # Bind mouse events for dragging to the entire window
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        # Bind mouse button release event
        self.bind("<ButtonRelease-1>", self.on_drag_release)

        # Bind key events
        self.bind("<Delete>", self.close_widget)
        self.bind("o", self.open_option_window)
        self.bind("a", self.open_add_date_window)
        self.bind("e", self.open_edit_dates_window)

    def load_data(self, file_path):
        data = []
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return data

    def find_nearest_dates(self):
        today = datetime.now().date()
        future_dates = [
            (datetime.strptime(x[self.translated_text["date"]], "%d-%b").date(), x)
            for x in self.data
            if datetime.strptime(x[self.translated_text["date"]], "%d-%b")
            .date()
            .replace(year=today.year)
            >= today
        ]
        if future_dates:
            min_date = min(d[0] for d in future_dates)
            nearest_entries = [
                (d[0].strftime("%d-%b"), d[1]) for d in future_dates if d[0] == min_date
            ]
            return nearest_entries
        else:
            return []

    # click and drag
    def on_drag_start(self, event):
        self.x = event.x
        self.y = event.y

    # click and drag motion
    def on_drag_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def on_drag_release(self, event):
        # Record the position when the user releases the mouse button
        with DatabaseConnection() as db_connection:
            # Update position values in the database
            db_connection.update_row(
                1,
                {
                    "widget_x_position": self.winfo_x(),
                    "widget_y_position": self.winfo_y(),
                },
            )

    # closing the widget
    def close_widget(self, event=None):
        self.destroy()

    def close_draggable_window(self):
        # Close the draggable window instance
        # Needs to be another function if not it closes the other window open
        self.destroy()

    def open_option_window(self, event=None):
        if (
            hasattr(self, "option_window")
            and self.option_window is not None
            and self.option_window.is_open()
        ):
            # If the option window is open, close it
            self.option_window.destroy()
            self.option_window = None
        else:
            # If the option window is closed, open it
            with DatabaseConnection() as db_connection:
                # get the updated settings
                self.settings = db_connection.get_settings()[0]
            self.option_window = OptionWindow(self, self.settings)
            self.option_window.lift()
            # self.option_window.mainloop()

    def open_add_date_window(self, event=None):
        if not (
            hasattr(self, "add_date_window")
            and self.add_date_window is not None
            and self.add_date_window.is_open()
        ):
            #     # If the add_date window is open, close it
            #     self.add_date_window.destroy()
            #     self.add_date_window = None
            # else:
            self.add_date_window = AddDateWindow(self, self.settings)
            self.add_date_window.lift()
            # self.add_date_window.mainloop()

    def open_edit_dates_window(self, event=None):
        if not (
            hasattr(self, "edit_dates_window")
            and self.edit_dates_window is not None
            and self.edit_dates_window.is_open()
        ):
            #     # If the option window is open, close it
            #     self.edit_dates_window.destroy()
            #     self.edit_dates_window = None
            # else:
            try:
                self.edit_dates_window = CSVEditorWindow(self, self.settings)
                self.edit_dates_window.lift()
            except Exception as e:
                print(f"Error: {e}")

    def reload_widget(self):
        with DatabaseConnection() as db_connection:
            # Connect to the SQLite database and get settings
            self.settings = db_connection.get_settings()[0]

        # language
        if self.language != self.settings["language"]:
            self.language = self.settings["language"]
            self.translated_text = self.translations[self.language]
            self.update_first_row_language("dates.csv")

        custom_font = ("Arial", 10, self.settings["font_weight"].lower())

        # Reload data from the CSV file
        self.data = self.load_data("dates.csv")

        # Find all entries with the nearest date
        nearest_dates = self.find_nearest_dates()
        self.set_widget_size(len(nearest_dates))

        # Destroy existing labels and frame
        for widget in self.winfo_children():
            widget.destroy()

        # Create a new frame
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.X)

        # if len is 0 dont have any dates on file as user to add!
        if len(nearest_dates) == 0:
            # Display information for all entries with the nearest date
            label = tk.Label(
                frame,
                text=f"{self.translated_text['no_date']}",
                anchor="center",
                justify="center",
                wraplength=200,
                font=custom_font,
                fg=self.settings["text_colour"],
            )
            label.pack(pady=10)
        for nearest_date, nearest_data in nearest_dates:
            label_text = f"{self.translated_text['name']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['date']}: {nearest_data[self.translated_text['date']]}\n{self.translated_text['description']}: {nearest_data[self.translated_text['description']]}"
            label = tk.Label(
                frame,
                text=label_text,
                anchor="center",
                justify="center",
                wraplength=200,
                font=custom_font,
                fg=self.settings["text_colour"],
            )
            label.pack(pady=10)
        self.initialize_hover_buttons()

    def update_first_row_language(self, csv_path):
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            lines = csvfile.readlines()

        # Update the first row with translated column headers
        if lines:
            lines[0] = (
                f"{self.translated_text['name']},{self.translated_text['date']},{self.translated_text['description']}\n"
            )

            # Write the updated contents back to the CSV file
            with open(csv_path, "w", encoding="utf-8") as csvfile:
                csvfile.writelines(lines)

    ################################################################################
    # Hover Buttons

    def initialize_hover_buttons(self):
        # Create a frame for the buttons
        self.button_frame = tk.Frame(
            self, bg="white"
        )  # Adjust background color as needed
        self.button_frame.place(relx=1, rely=0, anchor="ne", relwidth=0.1)

        # Create four square buttons and add them to the frame
        # Plus Button
        self.plus_button = tk.Button(
            self.button_frame,
            width=2,
            height=25,
            command=self.open_add_date_window,
            bg="white",  # Set background color to white (or any color that matches your background)
            bd=0,  # Set border width to 0 to remove the border
            highlightthickness=0,  # Set highlightthickness to 0 to remove the highlight
            activebackground="white",
        )
        self.plus_button.pack(fill=tk.X, padx=0, pady=0, ipadx=0, ipady=0)

        # Edit Button
        self.edit_button = tk.Button(
            self.button_frame,
            width=2,
            height=25,
            command=self.open_edit_dates_window,
            bg="white",  # Set background color to white (or any color that matches your background)
            bd=0,  # Set border width to 0 to remove the border
            highlightthickness=0,  # Set highlightthickness to 0 to remove the highlight
            activebackground="white",
        )
        self.edit_button.pack(fill=tk.X, padx=0, pady=0, ipadx=0, ipady=0)

        # Settings Button
        self.settings_button = tk.Button(
            self.button_frame,
            width=2,
            height=25,
            command=self.open_option_window,
            bg="white",  # Set background color to white (or any color that matches your background)
            bd=0,  # Set border width to 0 to remove the border
            highlightthickness=0,  # Set highlightthickness to 0 to remove the highlight
            activebackground="white",
        )
        self.settings_button.pack(fill=tk.X, padx=0, pady=0, ipadx=0, ipady=0)

        # Close Button
        self.close_button = tk.Button(
            self.button_frame,
            width=2,
            height=25,
            command=self.close_draggable_window,
            bg="white",  # Set background color to white (or any color that matches your background)
            bd=0,  # Set border width to 0 to remove the border
            highlightthickness=0,  # Set highlightthickness to 0 to remove the highlight
            activebackground="white",
        )
        self.close_button.pack(fill=tk.X, padx=0, pady=0, ipadx=0, ipady=0)

        # Resize icons to fit button
        self.plus_icon = resize_icon(
            icons_path / "plus_icon.png",
            self.plus_button.winfo_reqwidth(),
            self.plus_button.winfo_reqwidth(),
        )
        self.edit_icon = resize_icon(
            icons_path / "edit_icon.png",
            self.edit_button.winfo_reqwidth(),
            self.edit_button.winfo_reqwidth(),
        )
        self.settings_icon = resize_icon(
            icons_path / "settings_icon.png",
            self.settings_button.winfo_reqwidth(),
            self.settings_button.winfo_reqwidth(),
        )
        self.close_icon = resize_icon(
            icons_path / "close_icon.png",
            self.close_button.winfo_reqwidth(),
            self.close_button.winfo_reqwidth(),
        )

        # Set the icons to the buttons
        self.plus_button.config(image=self.plus_icon)
        self.edit_button.config(image=self.edit_icon)
        self.settings_button.config(image=self.settings_icon)
        self.close_button.config(image=self.close_icon)
        # Initiallu hide buttons
        self.hide_buttons()

    def show_buttons(self, event):
        # Adjust the position to show the buttons with a slight offset to the left
        self.button_frame.place_configure(relx=1)

    def hide_buttons(self, event=None):
        # Hide the buttons by moving them to the right side
        self.button_frame.place_configure(relx=1.2)

    def set_widget_size(self, lenth):
        # Set the initial size
        if lenth == 0:
            size = 100
        else:
            size = lenth * 100  # 100 padding for each item

        # Calculate the widget start position
        x = self.settings["widget_x_position"]  # default 275
        y = self.settings["widget_y_position"]  #  default 50

        # Set the window size and position with equal padding
        self.geometry(f"250x{size}+{x}+{y}")

    #################################################################################


if __name__ == "__main__":
    app = DraggableWindow()
    app.mainloop()
