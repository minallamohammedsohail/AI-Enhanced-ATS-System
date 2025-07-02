# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import fitz  # PyMuPDF
import docx
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load spaCy model
nlp = spacy.load("en_core_web_md")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file."""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

def extract_skills(text):
    """Extract skills from text using spaCy and a predefined skill list."""
    # Common tech and soft skills (this would be more extensive in a real app)
    common_skills = [
        "python", "javascript", "react", "node", "aws", "docker", "kubernetes", 
        "sql", "nosql", "mongodb", "postgresql", "azure", "gcp", "machine learning",
        "artificial intelligence", "data science", "data analysis", "leadership",
        "communication", "teamwork", "problem solving", "critical thinking",
        "project management", "agile", "scrum", "devops", "ci/cd", "testing",
        "java", "c++", "c#", "ruby", "php", "html", "css", "typescript",
        "django", "flask", "fastapi", "spring", "express", "vue", "angular"
    ]
    
    # Process text with spaCy
    doc = nlp(text.lower())
    
    # Extract known skills
    found_skills = []
    for skill in common_skills:
        if skill in text.lower():
            found_skills.append(skill)
    
    # Extract potential skills using noun chunks and entity recognition
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower()
        # Check if chunk might be a skill (e.g., noun phrases that aren't just common words)
        if len(chunk_text.split()) >= 2 and not all(word in stopwords.words('english') for word in chunk_text.split()):
            found_skills.append(chunk_text)
    
    # Add named entities that might be technologies or frameworks
    for ent in doc.ents:
        if ent.label_ in ["PRODUCT", "ORG"]:
            found_skills.append(ent.text.lower())
    
    # Clean and deduplicate skills
    cleaned_skills = list(set([skill.strip() for skill in found_skills if len(skill.strip()) > 2]))
    return cleaned_skills

def extract_keywords(text, n=20):
    """Extract important keywords using TF-IDF."""
    # Process the text
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Create a string from filtered words for TF-IDF
    processed_text = ' '.join(filtered_words)
    
    # Calculate TF-IDF scores
    vectorizer = TfidfVectorizer(max_features=n)
    try:
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get scores and sort by importance
        tfidf_scores = zip(feature_names, tfidf_matrix.toarray()[0])
        sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
        
        # Return just the keywords
        return [item[0] for item in sorted_scores]
    except:
        # If we have too few features, return the filtered words
        return filtered_words[:n]

def calculate_ats_score(resume_text, job_description):
    """Calculate ATS compatibility score based on keyword matching and semantic similarity."""
    # Extract skills and keywords
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)
    
    # Calculate keyword overlap score (50% of total)
    if jd_skills:
        skill_overlap = sum(1 for skill in jd_skills if any(skill in rs.lower() for rs in resume_skills))
        keyword_score = (skill_overlap / len(jd_skills)) * 50
    else:
        keyword_score = 25  # Default score if no skills found
    
    # Calculate semantic similarity score (50% of total)
    resume_doc = nlp(resume_text[:10000])  # Limit text length for processing speed
    jd_doc = nlp(job_description[:10000])
    
    try:
        similarity_score = resume_doc.similarity(jd_doc) * 50
    except:
        similarity_score = 25  # Default if similarity calculation fails
    
    # Combine scores
    total_score = round(keyword_score + similarity_score)
    
    # Ensure score is within bounds
    return max(0, min(100, total_score))

def identify_missing_keywords(resume_text, job_description):
    """Identify keywords in the job description missing from the resume."""
    # Extract skills and keywords
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    
    # Find missing skills
    missing_skills = []
    for skill in jd_skills:
        if not any(skill in rs.lower() for rs in resume_skills):
            missing_skills.append(skill)
    
    # Extract important keywords from job description
    jd_keywords = extract_keywords(job_description, n=15)
    
    # Find missing keywords
    missing_keywords = []
    for keyword in jd_keywords:
        if keyword.lower() not in resume_text.lower():
            missing_keywords.append(keyword)
    
    # Combine and deduplicate
    all_missing = list(set(missing_skills + missing_keywords))
    
    # Return top N most important missing terms
    return sorted(all_missing)[:10]

def generate_improvement_suggestions(resume_text, job_description, missing_keywords):
    """Generate suggestions to improve resume based on job description."""
    suggestions = []
    
    # Basic suggestions based on missing keywords
    if missing_keywords:
        suggestions.append(f"Add these keywords to your resume: {', '.join(missing_keywords[:5])}")
    
    # Check if resume has quantifiable achievements
    if not re.search(r'\d+%|\d+ percent|increased|decreased|reduced|improved|achieved|delivered', resume_text, re.IGNORECASE):
        suggestions.append("Add quantifiable achievements (e.g., 'Increased sales by 20%', 'Reduced costs by $10K')")
    
    # Check for action verbs
    action_verbs = ["managed", "led", "developed", "created", "implemented", "designed", "analyzed"]
    if not any(verb in resume_text.lower() for verb in action_verbs):
        suggestions.append("Use more action verbs (e.g., 'managed', 'led', 'developed', 'implemented')")
    
    # Check resume length (rough estimation)
    word_count = len(resume_text.split())
    if word_count < 300:
        suggestions.append("Your resume seems short. Consider adding more details about your experience and skills.")
    elif word_count > 1000:
        suggestions.append("Your resume may be too long. Consider focusing on the most relevant experiences.")
    
    # Job description specific suggestion
    jd_doc = nlp(job_description)
    key_entities = [ent.text for ent in jd_doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE"]]
    if key_entities:
        unique_entities = list(set(key_entities))[:3]
        if unique_entities:
            suggestions.append(f"Mention experience with {', '.join(unique_entities)} if applicable")
    
    # Add generic but useful suggestions if we don't have enough
    if len(suggestions) < 3:
        additional_suggestions = [
            "Tailor your resume to match the job description more closely",
            "Ensure your most relevant experience is at the top of your resume",
            "Include a strong summary statement that highlights your relevant skills",
            "Use industry-specific terminology found in the job description"
        ]
        suggestions.extend(additional_suggestions)
    
    return suggestions[:5]  # Limit to top 5 suggestions

def analyze_tone_and_formality(text):
    """Analyze the tone and formality of the text."""
    # Count personal pronouns (I, me, my) - indicates more casual tone
    personal_pronouns = len(re.findall(r'\b(I|me|my|mine)\b', text, re.IGNORECASE))
    
    # Count passive voice constructions - indicates more formal tone
    doc = nlp(text)
    passive_constructions = 0
    for sent in doc.sents:
        if re.search(r'\b(was|were|been|be|is|am|are)\b\s+\w+ed\b', sent.text, re.IGNORECASE):
            passive_constructions += 1
    
    # Word formality indicators
    formal_words = ["utilize", "implement", "establish", "conduct", "demonstrate", "facilitate"]
    informal_words = ["use", "do", "start", "run", "show", "help"]
    
    formal_count = sum(1 for word in formal_words if re.search(rf'\b{word}\b', text, re.IGNORECASE))
    informal_count = sum(1 for word in informal_words if re.search(rf'\b{word}\b', text, re.IGNORECASE))
    
    # Calculate formality score
    formality_indicators = personal_pronouns * -1 + passive_constructions + formal_count - informal_count
    
    # Interpret results
    if formality_indicators > 10:
        return "Your resume has a highly formal tone, which works well for traditional industries but might be too stiff for startups or creative fields."
    elif formality_indicators > 5:
        return "Your resume has a professional, balanced tone appropriate for most industries."
    elif formality_indicators > 0:
        return "Your resume has a moderately formal tone with some personalization, which works well for most positions."
    else:
        return "Your resume has a somewhat casual tone. Consider increasing formality for more traditional roles."

def calculate_readability(text):
    """Calculate readability score and provide feedback."""
    # Calculate readability metrics
    flesch_score = textstat.flesch_reading_ease(text)
    grade_level = textstat.text_standard(text, float_output=True)
    
    # Calculate average sentence length
    sentences = sent_tokenize(text)
    avg_sentence_length = sum(len(word_tokenize(sent)) for sent in sentences) / len(sentences) if sentences else 0
    
    # Calculate bullet point ratio
    bullet_points = len(re.findall(r'•|\*|\-|\d+\.', text))
    bullet_ratio = bullet_points / len(sentences) if sentences else 0
    
    # Create readability score (0-100)
    readability_score = min(100, max(0, int((flesch_score * 0.5) + (100 - (grade_level * 5)) + (25 if bullet_ratio > 0.3 else 0))))
    
    # Generate feedback
    if readability_score >= 80:
        feedback = "Your resume is highly readable with good use of bullet points and concise sentences."
    elif readability_score >= 60:
        feedback = "Your resume is reasonably readable, but could benefit from more bullet points and shorter sentences."
    else:
        feedback = "Your resume may be difficult to scan quickly. Consider using more bullet points and shorter, focused sentences."
    
    if avg_sentence_length > 20:
        feedback += " Try to shorten your sentences for better readability."
    
    return feedback, readability_score

def analyze_achievements(text):
    """Analyze achievements and suggest improvements."""
    # Look for achievement patterns
    achievement_phrases = re.findall(r'(increased|decreased|reduced|improved|achieved|delivered|generated|saved|grew)[\w\s]+\d+%', text, re.IGNORECASE)
    
    # Check for quantifiable results
    quantified = re.findall(r'\d+%|\$\d+|\d+ percent|increased by \d+|decreased by \d+', text, re.IGNORECASE)
    
    # Generate analysis
    if len(achievement_phrases) >= 3:
        analysis = "Great job quantifying your achievements! This significantly strengthens your resume."
    elif len(achievement_phrases) > 0:
        analysis = "You have some quantified achievements, which is good. Adding more metrics would strengthen your impact."
    else:
        analysis = "Your resume would be stronger with quantified achievements showing your impact."
    
    # Generate suggestions for improvement
    sentences = sent_tokenize(text)
    achievement_suggestions = []
    
    # Find sentences that describe responsibilities but don't quantify results
    responsibility_patterns = [
        r'responsible for',
        r'managed',
        r'led', 
        r'developed',
        r'created',
        r'worked on'
    ]
    
    for sentence in sentences:
        for pattern in responsibility_patterns:
            if re.search(pattern, sentence, re.IGNORECASE) and not re.search(r'\d+%|\$\d+|\d+ percent', sentence, re.IGNORECASE):
                # Generate a suggestion to quantify this responsibility
                action = re.search(pattern, sentence, re.IGNORECASE).group(0)
                suggestion = f"Consider quantifying: \"{sentence.strip()}\" → \"...{action} resulting in X% improvement\""
                achievement_suggestions.append(suggestion)
    
    # Limit to top 3 suggestions
    achievement_suggestions = achievement_suggestions[:3]
    
    # Add generic suggestion if we don't have enough specific ones
    if not achievement_suggestions:
        achievement_suggestions = [
            "Add metrics such as \"Increased sales by 20%\" rather than just \"Increased sales\"",
            "Quantify your impact with numbers (%, $, time saved, etc.)",
            "Focus on results, not just responsibilities"
        ]
    
    return analysis, achievement_suggestions
# app.py (continued)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Main API endpoint to analyze resume against job description."""
    try:
        # Check if files and data are provided
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({
                'error': 'Missing resume file or job description'
            }), 400
        
        resume_file = request.files['resume']
        job_description = request.form['job_description']
        
        # Check if filename is empty
        if resume_file.filename == '':
            return jsonify({
                'error': 'No resume file selected'
            }), 400
        
        # Create a temporary file to store the uploaded resume
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(temp_path)
        
        # Extract text based on file type
        if resume_file.filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(temp_path)
        elif resume_file.filename.lower().endswith('.docx'):
            resume_text = extract_text_from_docx(temp_path)
        else:
            # Clean up temp file
            os.remove(temp_path)
            os.rmdir(temp_dir)
            return jsonify({
                'error': 'Unsupported file format. Please upload PDF or DOCX.'
            }), 400
        
        # Clean up the temp file
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        # Check if text extraction was successful
        if not resume_text:
            return jsonify({
                'error': 'Could not extract text from the resume'
            }), 400
        
        # Perform analysis
        ats_score = calculate_ats_score(resume_text, job_description)
        missing_keywords = identify_missing_keywords(resume_text, job_description)
        improvement_suggestions = generate_improvement_suggestions(resume_text, job_description, missing_keywords)
        
        # Generate additional insights
        tone_analysis = analyze_tone_and_formality(resume_text)
        readability_feedback, readability_score = calculate_readability(resume_text)
        achievement_analysis, achievement_suggestions = analyze_achievements(resume_text)
        
        # Construct response
        response = {
            'ats_score': ats_score,
            'missing_keywords': missing_keywords,
            'improvement_suggestions': improvement_suggestions,
            'ai_insights': {
                'tone_analysis': tone_analysis,
                'readability': readability_feedback,
                'readability_score': readability_score,
                'achievement_analysis': achievement_analysis,
                'achievement_suggestions': achievement_suggestions
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing resume: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)