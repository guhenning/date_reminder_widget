# Date Reminder App

## Gustavo Henning

Contact: gustavo.henning@outlook.com

---

An application for reminding important dates such as birthdays or anniversaries.

### Commands:

To run these commands, open CMD and type the name of the file, e.g., `runner.bat`

- `update_requirements.bat`: Retrieves the list of all necessary modules for the project and updates the `requirements.txt` file.
- `runner.bat`: Facilitates the easy run of a file. The default file is `main_widget`, but you can comment out the call and uncomment the call for another file.

- `make_exe.bat`: Generates the `.exe` file again with the current project and imports necessary files to the `dist` folder where the final `.exe` file is located.

- `create_venv_install_requirements.bat`: This should be done after copying this repository for the first time. It sets up the environment necessary for the project.

- `activate.bat`: Activates the environment to run the Python files. This is also needed when installing a new package.

### Files:

- The `.exe` file is the final file of this version (V0.01) located in the `dist` folder.

- The `.rar` file can be directly used to run the app on your computer. Simply unzip the files and run the `.exe`.

- `dates.csv` stores names, dates, and descriptions. It can be edited by clicking the Edit icon or using any `.csv` reader.

- `settings.sqlite` stores user options such as language, text color, etc., as well as the position of the draggable widget.

- Icon images for the buttons are located in the `icon` folder. For running the `.exe`, this folder needs to be in the same path.

### On Hover Buttons:

1. **Plus Icon**: Opens the AddDate Window to add a date to the `.csv` file.
2. **Edit Icon**: Opens the Edit Window where the `.csv` file can be edited.
3. **Settings Icon**: Opens the settings window where language, text weight, text color, and opacity can be changed.
4. **Close Icon**: Closes the window and the main app.

### Getting Started:

After making the pull request of this repository, run the following commands in this order:

- `create_venv_install_requirements.bat`
- `make_exe.bat`

If necessary for testing, delete the current `dates.csv` and rename `dummy_dates.csv` to `dates.csv`.

### Windows:

- **DraggableWidget**: This is where the data of the nearest date found is shown.

#### Keyboard Shortcuts of DraggableWidget:

- `a`: Opens the AddDateWindow
- `e`: Opens the CSVEditorWindow
- `o`: Opens the OptionWindow
- `Del/Delete`: Closes the entire app

- **CSVEditorWindow**: This is where the `.csv` file is edited.

#### Keyboard Shortcuts of CSVEditorWindow:

- `s`: Save changes
- `Esc/Escape`: Close the CSVEditorWindow
