@echo off
cd /d "%~dp0"
echo Creating venv...
python -m venv .venv
call .venv\Scripts\activate
echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt
echo Starting server at http://127.0.0.1:8000
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
