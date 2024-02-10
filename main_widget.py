import tkinter as tk
from datetime import datetime, timedelta
import csv
from option_window import OptionWindow
from add_date_window import AddDateWindow
from csv_editor import CSVEditorWindow
from db_connection import DatabaseConnection


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
            "EN": {"name": "Name", "date": "Date", "description": "Description"},
            "IT": {"name": "Nome", "date": "Data", "description": "Descrizione"},
            "BR": {"name": "Nome", "date": "Data", "description": "Descrição"},
            "ES": {"name": "Nombre", "date": "Fecha", "description": "Descripción"},
        }
        self.translated_text = self.translations[self.language]

        # Find all entries with the nearest date
        nearest_dates = self.find_nearest_dates()

        # Set the initial size
        size = len(nearest_dates) * 100  # 100 padding for each item

        # Calculate the widget start position
        x = self.settings["widget_x_position"]  # default 275
        y = self.settings["widget_y_position"]  #  default 50

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # x  # right margin 275
        # y  # top margin 50

        # Set the window size and position with equal padding
        self.geometry(f"250x{size}+{x}+{y}")

        # Create a frame for centering labels
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.X)

        custom_font = ("Arial", 10, self.settings["font_weight"].lower())

        # Display information for all entries with the nearest date
        for nearest_date, nearest_data in nearest_dates:
            label_text = f"{self.translated_text['name']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['date']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['description']}: {nearest_data[self.translated_text['name']]}"
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
    def close_widget(self, event):
        self.destroy()

    def open_option_window(self, event):
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

    def open_add_date_window(self, event):
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

    def open_edit_dates_window(self, event):
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

        # Destroy existing labels and frame
        for widget in self.winfo_children():
            widget.destroy()

        # Create a new frame
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.X)

        # Display information for all entries with the nearest date
        for nearest_date, nearest_data in nearest_dates:
            label_text = f"{self.translated_text['name']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['date']}: {nearest_data[self.translated_text['name']]}\n{self.translated_text['description']}: {nearest_data[self.translated_text['name']]}"
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


if __name__ == "__main__":
    app = DraggableWindow()
    app.mainloop()
