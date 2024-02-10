call .\venv\Scripts\activate.bat

call pip freeze | findstr /V /C:"date_reminder" > requirements.txt