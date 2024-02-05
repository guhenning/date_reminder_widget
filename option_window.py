import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from db_connection import DatabaseConnection


class OptionWindow(tk.Tk):
    def __init__(self, parent, settings=None):
        super().__init__()

        self.parent = parent

        translation_option = {
            "EN": (
                "Settings",
                "Language",
                "Font Weight",
                "Opacity",
                "Text Colour",
                "Hex Code",
                "Change Color",
                "Cancel",
            ),
            "IT": (
                "Impostazioni",
                "Lingua",
                "Peso del Carattere",
                "Opacità",
                "Colore del Testo",
                "Codice Esadecimale",
                "Cambia Colore",
                "Annulla",
            ),
            "BR": (
                "Configurações",
                "Idioma",
                "Peso da Fonte",
                "Opacidade",
                "Cor do Texto",
                "Código Hexadecimal",
                "Mudar Cor",
                "Cancelar",
            ),
            "ES": (
                "Configuraciones",
                "Idioma",
                "Peso de la Fuente",
                "Opacidad",
                "Color del Texto",
                "Código Hexadecimal",
                "Cambiar Color",
                "Cancelar",
            ),
        }

        language_set = settings["language"]

        # tuple index 0 "Settings"
        self.title(translation_option[language_set][0])

        # Create language selection list
        self.language_var = tk.StringVar()
        # tuple index one "Language"
        language_label = tk.Label(self, text=f"{translation_option[language_set][1]}:")
        language_label.pack(pady=5)
        language_list = ttk.Combobox(
            self, values=["EN", "ES", "BR", "IT"], textvariable=self.language_var
        )
        language_list.pack(pady=5)
        # set language initial value from data base
        self.language_var.set(language_set)
        language_index_dict = {"EN": 0, "ES": 1, "BR": 2, "IT": 3}
        language_list.current(language_index_dict[language_set])
        # update selected language
        language_list.bind("<<ComboboxSelected>>", self.update_language_var)

        # Create font weight selection list
        self.weight_var = tk.StringVar()
        # tuple index 2 "Font Weight"
        weight_label = tk.Label(self, text=f"{translation_option[language_set][2]}:")
        weight_label.pack(pady=5)
        weight_list = ttk.Combobox(
            self, values=["NORMAL", "BOLD"], textvariable=self.weight_var
        )
        weight_list.pack(pady=5)
        # set font_weight initial value from data base
        self.weight_var.set(settings["font_weight"])
        font_weight_from_db = settings["font_weight"]
        font_weight_index_dict = {"NORMAL": 0, "BOLD": 1}
        weight_list.current(font_weight_index_dict[font_weight_from_db])
        # update selected font_weight
        weight_list.bind("<<ComboboxSelected>>", self.update_weight_var)

        # opacity
        # Create opacity selection list
        self.opacity_var = tk.StringVar()
        # tuple index 3 "Opacity"
        opacity_label = tk.Label(self, text=f"{translation_option[language_set][3]}:")
        opacity_label.pack(pady=5)
        opacity_list = ttk.Combobox(
            self,
            values=[f"{i}%" for i in range(10, 101, 10)],  # 10% 20% 30%..... 100%
            textvariable=self.opacity_var,
        )
        opacity_list.pack(pady=5)
        # set opacity initial value from data base
        self.opacity_var.set(settings["opacity"])
        opacity_from_db = settings["opacity"]
        opacity_dict = {
            f"{i}%": (i // 10) for i in range(0, 101, 10)
        }  # 10%:0 20%:1 30%:2..... 100%:9
        opacity_list.current(opacity_dict[opacity_from_db])
        # update selected font_opacity
        opacity_list.bind("<<ComboboxSelected>>", self.update_opacity_var)

        # Create color picker
        self.color_var = tk.StringVar()
        self.color_var.set(
            settings.get("text_colour", "black")
        )  # Set text color from database
        # tuple index 4 "Text Colour"
        color_label = tk.Label(self, text=f"{translation_option[language_set][4]}:")
        color_label.pack(pady=5)

        # Color viewer
        self.color_viewer_frame = tk.Frame(
            self, bg=self.color_var.get(), width=45, height=45
        )
        self.color_viewer_frame.pack(pady=5)
        # tuple index 5 "Hex Code"
        self.hex_code_translation = translation_option[language_set][5]
        self.hex_code_label = tk.Label(
            self,
            text=f"{self.hex_code_translation}: {self.color_var.get()}",
            font=("Arial", 8),
        )
        self.hex_code_label.pack(pady=5)
        # tuple index 6 "Change Color"

        color_button = tk.Button(
            self,
            text=f"{translation_option[language_set][6]}",
            command=self.pick_color,
        )
        color_button.pack(pady=5)

        # Add OK and Cancel buttons
        ok_button = tk.Button(self, text="  OK  ", command=self.okay_button_click)
        ok_button.pack(side=tk.RIGHT, padx=(0, 60), anchor=tk.CENTER)
        # tuple index 7 "Cancel"
        cancel_button = tk.Button(
            self,
            text=f"{translation_option[language_set][7]}",
            command=self.cancel_button_click,
        )
        cancel_button.pack(side=tk.LEFT, padx=(60, 0), anchor=tk.CENTER)

        # Calculate the widget start position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_centered = screen_width - 550  # right margin 500
        # print(f"X option: {x_centered}")
        y_centered = screen_height - (screen_height - 50)  # top margin 50
        # print(f"Y option: {y_centered}")

        # Set the window size and position with equal padding
        self.geometry(f"250x450+{x_centered}+{y_centered}")

    def update_language_var(self, event):
        # Update language variable when a different language is selected
        self.language_var.set(event.widget.get())

    def update_weight_var(self, event):
        # Update font weight variable when a different weight is selected
        self.weight_var.set(event.widget.get())

    def update_opacity_var(self, event):

        self.opacity_var.set(event.widget.get())

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        self.color_var.set(color)  # Set the selected color to the color variable

        self.update_color_viewer(self.hex_code_translation)

    def update_color_viewer(self, text_translated):
        # Update color viewer and hex code label
        self.color_viewer_frame.configure(bg=self.color_var.get())
        self.hex_code_label.configure(text=f"{text_translated}: {self.color_var.get()}")

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
                    "opacity": self.opacity_var.get(),
                },
            )
        # Reload the widget in the parent window
        if self.parent:
            self.parent.reload_widget()
        self.destroy()

    def cancel_button_click(self):
        # Add any necessary processing when Cancel button is clicked
        self.destroy()

    def is_open(self):
        try:
            return self.winfo_exists()
        except tk.TclError:
            return False
