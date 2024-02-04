import tkinter as tk
from datetime import datetime, timedelta
import csv
from option_window import OptionWindow


class DraggableWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("")  # Set an empty title to remove the default label
        self.overrideredirect(True)  # Remove window borders
        self.attributes("-alpha", 0.8)  # Set window transparency

        # Load data from the CSV file
        self.data = self.load_data("dates.csv")

        # Find all entries with the nearest date
        nearest_dates = self.find_nearest_dates()

        # Set the initial size
        size = len(nearest_dates) * 100  # 100 padding for each item

        # Calculate the widget start position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_centered = screen_width - 275  # right margin 275
        # print(f"X main: {x_centered}")

        y_centered = screen_height - (screen_height - 50)  # top margin 50
        # print(f"Y main: {y_centered}")

        # Set the window size and position with equal padding
        self.geometry(f"250x{size}+{x_centered}+{y_centered}")

        # Default language
        self.language = "EN"

        # Create a frame for centering labels
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.X)

        # Display information for all entries with the nearest date
        for nearest_date, nearest_data in nearest_dates:
            label_text = f"{self.get_text('Name')}: {nearest_data['name']}\n{self.get_text('Date')}: {nearest_data['date']}\n{self.get_text('Description')}: {nearest_data['description']}"
            label = tk.Label(
                frame,
                text=label_text,
                anchor="center",
                justify="center",
                wraplength=200,
            )
            label.pack(pady=10)

        # Bind mouse events for dragging to the entire window
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)

        # Bind key events
        self.bind("<Delete>", self.close_widget)
        self.bind("o", self.open_option_window)

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
            (datetime.strptime(x["date"], "%d-%b").date(), x)
            for x in self.data
            if datetime.strptime(x["date"], "%d-%b").date().replace(year=today.year)
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
            self.option_window = OptionWindow()
            self.option_window.mainloop()

    def get_text(self, key):
        translation = {
            "EN": {"Name": "Name", "Date": "Date", "Description": "Description"},
            "IT": {"Name": "Nome", "Date": "Data", "Description": "Descrizione"},
            "BR": {"Name": "Nome", "Date": "Data", "Description": "Descrição"},
            "ES": {"Name": "Nombre", "Date": "Fecha", "Description": "Descripción"},
        }
        return translation[self.language][key]


if __name__ == "__main__":
    app = DraggableWindow()
    app.mainloop()
