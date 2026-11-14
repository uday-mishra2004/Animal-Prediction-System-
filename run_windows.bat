@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m src.train
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m streamlit run app.py
pause
exit /b
:fail
echo Setup failed. Review the error above. Python 3.11 or 3.12 recommended.
pause
exit /b 1
