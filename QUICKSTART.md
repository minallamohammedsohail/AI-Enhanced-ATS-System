# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Quick Setup (Windows)

### Option 1: Using Batch Scripts (Easiest)

1. **Start Backend:**
   - Double-click `start-backend.bat`
   - Wait for "Running on http://127.0.0.1:5000"

2. **Start Frontend:**
   - Open a new terminal/command prompt
   - Double-click `start-frontend.bat`
   - Wait for the dev server to start

3. **Open Browser:**
   - Navigate to `http://localhost:3000`

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Upload a resume (PDF or DOCX format)
2. Paste the job description
3. Click "Analyze Resume"
4. View your ATS score and recommendations

## Troubleshooting

### Backend Issues
- **spaCy model not found**: Run `python -m spacy download en_core_web_sm`
- **Port 5000 already in use**: Change port in `backend/app.py`
- **Import errors**: Make sure virtual environment is activated

### Frontend Issues
- **Port 3000 already in use**: Vite will automatically use the next available port
- **Module not found**: Run `npm install` again
- **API connection error**: Ensure backend is running on port 5000

## Features

✅ PDF and DOCX resume parsing
✅ AI-powered skill extraction
✅ Semantic similarity analysis
✅ Tone and readability scoring
✅ Real-time ATS score calculation
✅ Personalized recommendations
✅ Modern, responsive UI

