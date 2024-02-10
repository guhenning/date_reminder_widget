# Date Reminder App

## Gustavo Henning

## gustavo.henning@outlook.com

# A App for Reminding Important Dates like Birhdays or Annyversaris

## Commands:

## To run those open cmd and type the name of the file Ex.: runner.bat

- update_requirements.bat It get all the list of all the necessary modules of the project and update the requirements.txt.

- runner.bat Is used for an easy run of a file default is main_widget but can be commented with :: and uncomment the call for another file.

- make_exe.bat It generates the .exe file again with the current project and import necessary files to the dist folder where is the final .exe file.

- create_venv_install_requirements.bat This should be done after copying this repo on the first start so it get all the environment ready for the project.

- activate.bat This activate the enviroment to run the python files this is also needed when installing a new package.

## Files

- The .exe File is the final file of this version V0.01 that is in the dist folder.

- The .rar File can be used directly to run the app on your computer just unzip the files and run the .exe.

- The dates.csv is where the names, dates and descriptions are stored. It can be edited by hitting the Edit icon or also with any .csv reader.

- The settings.sqlite Is where we store the user options such as language text color etc.. An also the position of the dragable widget.

- The icons images for the buttons are in the icon folder and for running the .exe it need this folder in the same path.

## On Hover Buttons

### 1:

_Plus Icon_: The first button is to the AddDate Window to add a date to the .csv file.

### 2:

_Edit Icon_: The second button is to open the Edit Window where we can edit the .csv file.

### 3:

_Settings Icon_: The third button is to open the settings window where we can change language, text weight, text color, and opacity.

### 4:

_Close Icon_: The forth button is to close the window and the main app.

## Getting Started

### After making the pull request of this repository run the commands in this following order:

- create_venv_install_requirements.bat

- make_exe.bat

#### And if necessary for testing delete the currenct dates.csv and rename the dummy_dates.csv to dates.csv

## Windows

- DraggableWidget this is where the data of the nearest date found is shown

### Keybord Shortcuts

a: Open the AddDateWindow
e: Open the CSVEditorWindow
o: Open the OptionWindow
Del/Delete: Close the app

- AddDateWindow this is where we edit the .csv file

### Keybord Shortcuts

s: Save changes
Esc/Escape: Close the edit window

- CSVEditorWindow this is where we edit the .csv file

### Keybord Shortcuts

s: Save changes
Esc/Escape: Close the edit window
