
call activate.bat
::call pyinstaller --onefile main_widget.py
call pyinstaller --onefile --noconsole main_widget.py
call python copy_files_to_dist.py
echo The .exe file is Ready to use FilePath: dist/main_widget.exe

