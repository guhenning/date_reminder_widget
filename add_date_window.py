from pathlib import Path
import tkinter as tk
from tkinter import ttk  # Import ttk for styling
import csv
from tkcalendar import DateEntry

csv_path = Path("dates.csv")

# Create the CSV file if it doesn't exist and add column headers
if not csv_path.is_file():
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Description"])


class AddDateWindow(tk.Tk):
    def __init__(self, parent, settings=None):
        super().__init__()

        self.parent = parent

        self.translation_option = {
            "EN": (
                "Add New Date",
                "Name",
                "Date",
                "Description",
                "Cancel",
                "New Date Added",
            ),
            "BR": (
                "Adicionar Nova Data",
                "Nome",
                "Data",
                "Descrição",
                "Cancelar",
                "Nova Data Adicionada",
            ),
            "ES": (
                "Agregar Nueva Fecha",
                "Nombre",
                "Fecha",
                "Descripción",
                "Cancelar",
                "Nueva Fecha Agregada",
            ),
            "IT": (
                "Aggiungi Nuova Data",
                "Nome",
                "Data",
                "Descrizione",
                "Annulla",
                "Nuova Data Aggiunta",
            ),
        }

        self.language_set = settings["language"]

        # Tuple index 0 is "Settings"
        self.title(self.translation_option[self.language_set][0])

        # Set window size and position
        self.geometry("400x400")
        self.center_window()

        # Create style for the entry widgets
        self.style = ttk.Style()
        self.style.configure(
            "CustomEntry.TEntry",
            borderwidth=2,
            relief="solid",
            font=("Arial", 10),
            foreground="black",
        )
        font = ("Arial", 10, "bold")
        # Create labels and entry fields
        ttk.Label(
            self, text=f"{self.translation_option[self.language_set][1]}:", font=font
        ).place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.name_entry = ttk.Entry(self, style="CustomEntry.TEntry", width=30)
        self.name_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        ttk.Label(
            self, text=f"{self.translation_option[self.language_set][2]}:", font=font
        ).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.date_entry = DateEntry(
            self, borderwidth=2, relief="solid", date_pattern="dd/MM/yyyy"
        )
        self.date_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(
            self, text=f"{self.translation_option[self.language_set][3]}:", font=font
        ).place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.description_entry = ttk.Entry(self, style="CustomEntry.TEntry", width=30)
        self.description_entry.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Create a frame to contain the buttons
        button_frame = ttk.Frame(self)
        button_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Create "Cancel" button
        ttk.Button(
            button_frame,
            text=self.translation_option[self.language_set][4],
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=5)

        # Create "Add" button
        ttk.Button(
            button_frame,
            text=self.translation_option[self.language_set][0],
            command=self.add_row,
        ).pack(side=tk.LEFT, padx=5)

    def add_row(self):
        name = self.name_entry.get().strip()
        date = (
            self.date_entry.get_date().strftime("%d-%b")
            if self.date_entry.get_date()
            else ""
        )
        description = self.description_entry.get().strip()

        if name and date:
            # Add row to CSV file
            with open(csv_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, date, description])
            # Reload the widget in the parent window
            # Show temporary text "New Date Added"
            self.show_temporary_text()
            if self.parent:
                self.parent.reload_widget()

    def show_temporary_text(self):
        # Create a label widget to display temporary text
        label = tk.Label(self, text=f"{self.translation_option[self.language_set][5]}!")
        label.place(relx=0.5, rely=0.80, anchor=tk.CENTER)

        # Schedule the label to be removed after 2 seconds
        label.after(2000, label.destroy)

    def center_window(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position to center window on screen
        x = (screen_width - 400) // 2
        y = (screen_height - 400) // 2

        # Set window position
        self.geometry("+{}+{}".format(x, y))

    def is_open(self):
        try:
            return self.winfo_exists()
        except tk.TclError:
            return False


if __name__ == "__main__":
    app = AddDateWindow(None)
    app.mainloop()
