from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkFont
import csv
from pathlib import Path
import tkinter as tk


##
# - 2024 Gustavo Henning gustavo.henning@outlook.com
##


##
#   TODO: Add + / - buttons to create/remove rows & coloumns
#   TODO: Add resizing of cells
##
class CSVEditorWindow(tk.Toplevel):
    def __init__(self, parent, settings=None):
        super().__init__()
        self.parent = parent
        self.csv_path = Path("dates.csv")
        self.translation_option = {
            "EN": ("Editor", "File", "Exit", "Save", "Add Line"),
            "BR": ("Editor", "Arquivo", "Sair", "Salvar", "Adicionar Linha"),
            "ES": ("Editor", "Archivo", "Salir", "Guardar", "Agregar línea"),
            "IT": ("Editor", "File", "Uscita", "Salva", "Aggiungi riga"),
        }

        self.language_set = settings["language"]
        icons_path = Path("icons")
        edit_icon = tk.PhotoImage(file=icons_path / "edit_icon.png")
        # Set window icon
        self.iconphoto(True, edit_icon)

        self.createDefaultWidgets()
        # Set Title
        self.title(self.translation_option[self.language_set][0])
        ## CODE ENTRY ###
        default_font = tkFont.nametofont("TkTextFont")
        default_font.configure(family="Helvetica")

        self.option_add("*Font", default_font)
        self.option_add("*Font", default_font)

        # Initialize defalut values for numbers of row and columns
        self.current_columns_number = 3
        self.current_rows_number = 1
        # Load Date Cels
        self.loadCells()

        # Create Menu
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(
            label=self.translation_option[self.language_set][4], command=self.addNewCell
        )
        # Save
        filemenu.add_command(
            label=self.translation_option[self.language_set][3], command=self.save
        )
        # Exit horizontal menu
        filemenu.add_command(
            label=self.translation_option[self.language_set][2], command=self.close
        )
        # File
        menubar.add_cascade(
            label=self.translation_option[self.language_set][1], menu=filemenu
        )
        # Exit cascade menu
        menubar.add_command(
            label=self.translation_option[self.language_set][2], command=self.close
        )
        self.config(menu=menubar)

        # Bind esc keyboard to close window
        self.bind("<Escape>", self.close)

        # filemenu.add_command(label="New", command=app.newCells)  # add save dialog
        # add save dialog
        #  filemenu.add_command(label="Open", command=app.loadCells)
        # filemenu.add_command(label="Open File", command=app.openAndloadCells)
        # filemenu.add_command(label="Save as", command=app.saveAs)

    cellList = []
    currentCells = []
    currentCell = None

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if j >= len(self.currentCells[0]) - 1:
                        j = -1
                    self.currentCells[i][j + 1].focus()
        return "break"

    def focus_left(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if j == 0:
                        j = len(self.currentCells[0])
                    self.currentCells[i][j - 1].focus()
        return "break"

    def focus_up(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if i < 0:
                        i = len(self.currentCells)
                    self.currentCells[i - 1][j].focus()
        return "break"

    def focus_down(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if i >= len(self.currentCells) - 1:
                        i = -1
                    self.currentCells[i + 1][j].focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    def saveFile(self, event):
        self.saveAs()

    # TODO: Create bind for arrow keys and enter

    def createDefaultWidgets(self):
        w, h = 7, 1
        self.sizeX = 4
        self.sizeY = 6
        self.defaultCells = []
        for i in range(self.sizeY):
            self.defaultCells.append([])
            for j in range(self.sizeX):
                self.defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", lambda event: self.save())
                # TODO: Add resize check on column when changing focus
                tmp.insert(END, "")
                tmp.grid(padx=0, pady=0, column=j, row=i)

                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)

        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
        self.currentCell = self.currentCells[0][0]

        # TODO: Add buttons to create new rows/columns

    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while len(self.cellList) > 0:
            for cell in self.cellList:
                # print str(i) + str(j)
                cell.destroy()
                self.cellList.remove(cell)

    def openAndloadCells(self):
        filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select file",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
        )
        ary = []
        col = -1
        rows = []

        # get array size & get contents of rows
        with open(filename, "r", encoding="utf-8") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])

        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print rows[i][j]
                ary[i][j] = rows[i][j]

        self.removeCells()

        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if len(ary[i][j]) >= mx:
                    mx = len(ary[i][j])
        w = mx

        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", lambda event: self.save())
                tmp.insert(END, ary[i][j])

                if i == 0:
                    tmp.config(font=("Helvetica", 10, tkFont.BOLD))
                    tmp.config(relief=FLAT, bg=self.cget("bg"))

                loadCells[i][j] = tmp
                tmp.focus_force()
                self.cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]

    def loadCells(self):
        ary = []
        col = -1
        rows = []

        # get array size & get contents of rows
        with open(self.csv_path, "r", encoding="utf-8") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)

        self.current_columns_number = len(row)
        self.current_rows_number = len(rows)

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])

        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print rows[i][j]
                ary[i][j] = rows[i][j]

        self.removeCells()

        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if len(ary[i][j]) >= mx:
                    mx = len(ary[i][j])
        w = mx

        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", lambda event: self.save())
                tmp.insert(END, ary[i][j])

                if i == 0:
                    tmp.config(font=("Helvetica", 10, tkFont.BOLD))
                    tmp.config(relief=FLAT, bg=self.cget("bg"))

                loadCells[i][j] = tmp
                tmp.focus_force()
                self.cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]

    def addNewCell(self):
        # Read the existing CSV file
        with open(self.csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        # Determine the position to insert the new line
        insert_index = len(rows)  # Insert at the end of the file

        # Create a new list with the additional row
        new_row = ["" for _ in range(len(rows[0]))]  # Create a row with empty values
        rows.insert(insert_index, new_row)

        # Write the modified data to a new CSV file
        with open(self.csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        # Reload the cells to reflect the changes
        self.loadCells()
        # Move the cursor back to the first column of the added line
        self.currentCells[insert_index][0].focus_force()

    def saveAs(self):
        filename = filedialog.asksaveasfilename(
            initialdir=".",
            title="Save File",
            filetypes=(("csv files", "*.csv"), ("all files", "*.*")),
            defaultextension=".csv",
        )

        vals = []
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                vals.append(self.currentCells[i][j].get(1.0, END).strip())

        with open(filename, "w", encoding="utf-8") as csvfile:
            for rw in range(len(self.currentCells)):
                row = ""
                for i in range(len(self.currentCells[0])):
                    x = rw * len(self.currentCells[0])
                    if i != len(self.currentCells[0]) - 1:
                        row += vals[x + i] + ","
                    else:
                        row += vals[x + i]

                csvfile.write(row + "\n")
        if self.parent:
            self.parent.reload_widget()
        messagebox.showinfo("", "Saved!")

    def save(self):
        vals = []
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                vals.append(self.currentCells[i][j].get(1.0, END).strip())

        with open(self.csv_path, "w", encoding="utf-8") as csvfile:
            for rw in range(len(self.currentCells)):
                row = ""
                for i in range(len(self.currentCells[0])):
                    x = rw * len(self.currentCells[0])
                    if i != len(self.currentCells[0]) - 1:
                        row += vals[x + i] + ","
                    else:
                        row += vals[x + i]

                csvfile.write(row + "\n")
        if self.parent:
            self.parent.reload_widget()
        messagebox.showinfo("", "Saved!")

    def is_open(self):
        try:
            return self.winfo_exists()
        except tk.TclError:
            return False

    def close(self, event=None):
        self.destroy()


# End Class #


# Begin functions #


def hello():
    messagebox.showinfo("", "Hello!")


# End functions #
