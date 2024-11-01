@echo off

:: Check if virtual environment exists, if not create it
if not exist venv (
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Install required packages
pip install -r requirements.txt

:: Prompt for email and password
set /p email=Enter your email: 
set /p password=Enter your password: 

:: Run the Python script with email and password as arguments
python your_script.py %email% %password%

:: Deactivate the virtual environment
deactivate