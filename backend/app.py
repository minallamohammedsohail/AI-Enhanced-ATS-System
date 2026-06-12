from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from ats_analyzer import ATSAnalyzer

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize ATS Analyzer
ats_analyzer = ATSAnalyzer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'ATS API is running'})

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    files_to_cleanup = []
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed'}), 400
        
        # Save resume file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        files_to_cleanup.append(filepath)
        
        # Handle job description file upload (takes precedence over text)
        if 'job_description_file' in request.files:
            jd_file = request.files['job_description_file']
            if jd_file.filename != '' and allowed_file(jd_file.filename):
                jd_filename = secure_filename(jd_file.filename)
                # Prefix to avoid name collision with resume
                jd_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'jd_' + jd_filename)
                jd_file.save(jd_filepath)
                files_to_cleanup.append(jd_filepath)
                try:
                    job_description = ats_analyzer.parse_document(jd_filepath)
                except Exception as e:
                    raise Exception(f"Error reading job description file: {str(e)}")
            elif jd_file.filename != '' and not allowed_file(jd_file.filename):
                raise Exception('Invalid job description file type. Only PDF and DOCX files are allowed')
        
        if not job_description.strip():
            raise Exception('Please provide a job description (paste text or upload a document)')
        
        try:
            # Analyze resume
            result = ats_analyzer.analyze_resume(filepath, job_description)
            
            # Clean up uploaded files
            for f in files_to_cleanup:
                if os.path.exists(f):
                    os.remove(f)
            
            return jsonify(result)
        except Exception as e:
            raise e
            
    except Exception as e:
        # Clean up all files on error
        for f in files_to_cleanup:
            if os.path.exists(f):
                os.remove(f)
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-skills', methods=['POST'])
def extract_skills():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        skills = ats_analyzer.extract_skills(text)
        return jsonify({'skills': skills})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

