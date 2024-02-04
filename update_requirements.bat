call .\venv\Scripts\activate.bat

call pip freeze | findstr /V /C:"fii_project" > requirements.txt