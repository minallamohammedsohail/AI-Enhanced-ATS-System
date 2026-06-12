# AI-Powered Applicant Tracking System (ATS)

A full-stack AI-enhanced Applicant Tracking System that enables intelligent resume screening and analysis using Natural Language Processing (NLP) and machine learning techniques.

## Features

- **Intelligent Resume Screening**: Automated analysis of resumes against job descriptions
- **Document Parsing**: Support for PDF and DOCX file formats using PyMuPDF and python-docx
- **NLP-Powered Analysis**: 
  - Skill extraction using spaCy
  - Semantic similarity using TF-IDF and cosine similarity
  - Tone analysis for professional writing assessment
  - Readability scoring using Flesch-Kincaid metrics
- **ATS Score Computation**: Comprehensive scoring system combining multiple factors
- **Modern UI**: Built with React.js and shadcn/ui components
- **Real-time Feedback**: Interactive interface with instant analysis results
- **Secure Communication**: RESTful API with CORS protection

## Tech Stack

### Backend
- **Flask**: Python web framework
- **spaCy**: Natural Language Processing
- **scikit-learn**: Machine learning (TF-IDF, cosine similarity)
- **PyMuPDF**: PDF document parsing
- **python-docx**: DOCX document parsing
- **textstat**: Readability analysis

### Frontend
- **React.js**: UI framework
- **Vite**: Build tool
- **shadcn/ui**: Modern UI component library
- **Tailwind CSS**: Styling
- **Recharts**: Data visualization
- **Axios**: HTTP client

## Installation

### Prerequisites
- Python 3.8+ (Python 3.12+ recommended, fully compatible)
- Node.js 16+
- npm or yarn

**Note**: For Python 3.12+, the project uses updated dependencies that are compatible with the removal of the deprecated `imp` module. The setup scripts automatically handle this.

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

6. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Start both the backend and frontend servers
2. Open your browser and navigate to `http://localhost:3000`
3. Upload a resume file (PDF or DOCX format)
4. Paste the job description in the text area
5. Click "Analyze Resume" to get instant feedback

## ATS Scoring System

The ATS score is computed using a weighted combination of:

- **Similarity Score (40%)**: TF-IDF based cosine similarity between resume and job description
- **Skills Match (30%)**: Percentage of job-required skills found in the resume
- **Tone Score (15%)**: Professional, confident, and positive language indicators
- **Readability Score (15%)**: Flesch Reading Ease and Flesch-Kincaid Grade Level

## API Endpoints

### `GET /api/health`
Health check endpoint

### `POST /api/analyze`
Analyze a resume against a job description
- **Form Data**:
  - `resume`: File (PDF or DOCX)
  - `job_description`: String

### `POST /api/extract-skills`
Extract skills from text
- **JSON Body**:
  - `text`: String

## Project Structure

```
ATS/
├── backend/
│   ├── app.py                 # Flask application
│   ├── ats_analyzer.py        # Core ATS analysis logic
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ui/           # shadcn/ui components
│   │   │   ├── ScoreChart.jsx
│   │   │   └── Recommendations.jsx
│   │   ├── App.jsx           # Main application component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Features in Detail

### Document Parsing
- Supports PDF files using PyMuPDF (fitz)
- Supports DOCX files using python-docx
- Extracts text content for analysis

### Skill Extraction
- Uses spaCy NLP for named entity recognition
- Keyword matching against a skills database
- Identifies technical and soft skills

### Semantic Similarity
- TF-IDF vectorization of resume and job description
- Cosine similarity computation
- Identifies keyword relevance and context

### Tone Analysis
- Professional language detection
- Confidence indicators
- Positive language assessment

### Readability Scoring
- Flesch Reading Ease score
- Flesch-Kincaid Grade Level
- Normalized scoring for ATS compatibility

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

