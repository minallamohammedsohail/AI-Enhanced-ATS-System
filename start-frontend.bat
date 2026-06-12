@echo off
echo Starting ATS Frontend...
cd frontend
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)
echo Starting development server...
call npm run dev
pause

