@echo off

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

echo Setting up the Django backend...
python -m venv venv
IF NOT EXIST venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists and is valid.
)

cd Webapp
pip install -r requirements.txt
start python manage.py runserver

node -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed. Please install Node.js and try again.
    pause
    exit /b
)

cd ../frontend
npm install && start npm run dev && timeout /t 10 && start http://localhost:5173




