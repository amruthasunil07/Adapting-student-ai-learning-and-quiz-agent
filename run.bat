@echo off
echo ========================================================
echo  Starting Adapting Student AI Learning and Quiz Agent
echo ========================================================
echo.
echo URL: http://localhost:8000
echo.

cd /d "%~dp0backend"
start http://localhost:8000
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
