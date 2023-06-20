@echo off

rem Step 1: Check if "venv" directory exists
if exist venv (
    echo "venv" directory already exists. Skipping installation process.
) else (
    rem Step 2: Create "venv" directory
    mkdir venv
    mkdir audio_fragments

    rem Step 3: Set up Python venv inside "venv" directory
    python -m venv venv

    rem Step 4: Activate the virtual environment
    call venv\Scripts\activate.bat

    rem Step 5: Install required packages
    pip install -r requirements.txt

    rem Step 6: Check if the setup is complete
    echo Checking if the setup is complete...
    python -c "import sys; print('Setup complete.') if hasattr(sys, 'real_prefix') else sys.exit('Setup not complete.')"

    rem Deactivate the virtual environment
    deactivate
)

rem Step 7: Activate the virtual environment
call venv\Scripts\activate.bat

rem Step 8: Run main.py
echo Running main.py...
python main.py

rem Step 9: Deactivate the virtual environment
deactivate

rem Pause at the end to see the output
pause
