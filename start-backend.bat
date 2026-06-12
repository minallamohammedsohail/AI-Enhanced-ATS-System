@echo off
echo Starting ATS Backend Server...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
if not exist venv\Lib\site-packages\flask (
    echo Upgrading pip and setuptools for Python 3.12+ compatibility...
    python -m pip install --upgrade pip setuptools>=69.0.0
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Downloading spaCy model...
    python -m spacy download en_core_web_sm
)
echo Starting Flask server...
python app.py
pause

