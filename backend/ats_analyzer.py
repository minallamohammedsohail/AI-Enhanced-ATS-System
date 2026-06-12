import fitz  # PyMuPDF
from docx import Document
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from typing import Dict, List, Tuple
import textstat

class ATSAnalyzer:
    def __init__(self):
        # Load spaCy model (download if not available: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Common skills database
        self.skills_db = [
            'python', 'javascript', 'java', 'react', 'node.js', 'flask', 'django',
            'sql', 'mongodb', 'postgresql', 'aws', 'docker', 'kubernetes', 'git',
            'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch',
            'html', 'css', 'typescript', 'angular', 'vue.js', 'express', 'rest api',
            'agile', 'scrum', 'ci/cd', 'jenkins', 'linux', 'bash', 'powershell',
            'data analysis', 'pandas', 'numpy', 'scikit-learn', 'tableau', 'power bi',
            'project management', 'leadership', 'communication', 'problem solving'
        ]
        
    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file using PyMuPDF"""
        try:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file using python-docx"""
        try:
            doc = Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def parse_document(self, filepath: str) -> str:
        """Parse document based on file extension"""
        ext = filepath.rsplit('.', 1)[1].lower()
        
        if ext == 'pdf':
            return self.extract_text_from_pdf(filepath)
        elif ext in ['docx', 'doc']:
            return self.extract_text_from_docx(filepath)
        else:
            raise Exception(f"Unsupported file format: {ext}")
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP and keyword matching"""
        if not self.nlp:
            # Fallback to simple keyword matching
            text_lower = text.lower()
            found_skills = [skill for skill in self.skills_db if skill.lower() in text_lower]
            return list(set(found_skills))
        
        # Use spaCy for better extraction
        doc = self.nlp(text.lower())
        
        # Extract skills using keyword matching and named entity recognition
        found_skills = []
        
        # Keyword matching
        text_lower = text.lower()
        for skill in self.skills_db:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Extract technical terms (nouns and proper nouns)
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                if token.text.lower() in [s.lower() for s in self.skills_db]:
                    found_skills.append(token.text)
        
        return list(set(found_skills))
    
    def compute_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Compute TF-IDF based cosine similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def analyze_tone(self, text: str) -> Dict[str, float]:
        """Analyze the tone of the text"""
        if not text:
            return {'professional': 0.0, 'confident': 0.0, 'positive': 0.0}
        
        text_lower = text.lower()
        
        # Professional indicators
        professional_words = ['experience', 'achieved', 'implemented', 'developed', 
                            'managed', 'led', 'collaborated', 'delivered', 'optimized']
        professional_score = sum(1 for word in professional_words if word in text_lower) / len(professional_words)
        
        # Confident indicators
        confident_words = ['expert', 'proficient', 'skilled', 'experienced', 
                          'accomplished', 'successful', 'strong']
        confident_score = sum(1 for word in confident_words if word in text_lower) / len(confident_words)
        
        # Positive indicators
        positive_words = ['success', 'achievement', 'improved', 'enhanced', 
                         'exceeded', 'excellent', 'outstanding', 'award']
        positive_score = sum(1 for word in positive_words if word in text_lower) / len(positive_words)
        
        return {
            'professional': min(professional_score * 10, 1.0),
            'confident': min(confident_score * 10, 1.0),
            'positive': min(positive_score * 10, 1.0)
        }
    
    def compute_readability_score(self, text: str) -> Dict[str, float]:
        """Compute readability metrics"""
        if not text:
            return {'flesch_reading_ease': 0.0, 'flesch_kincaid_grade': 0.0}
        
        try:
            flesch_ease = textstat.flesch_reading_ease(text)
            flesch_grade = textstat.flesch_kincaid_grade(text)
            
            # Normalize flesch reading ease (0-100 scale, higher is better)
            normalized_ease = max(0, min(1, flesch_ease / 100))
            
            # Normalize grade level (lower is better, assume 20 is max)
            normalized_grade = max(0, min(1, 1 - (flesch_grade / 20)))
            
            return {
                'flesch_reading_ease': normalized_ease,
                'flesch_kincaid_grade': normalized_grade,
                'raw_flesch_ease': flesch_ease,
                'raw_grade_level': flesch_grade
            }
        except:
            return {'flesch_reading_ease': 0.5, 'flesch_kincaid_grade': 0.5}
    
    def compute_ats_score(self, resume_text: str, job_description: str) -> Dict:
        """Compute comprehensive ATS score"""
        if not resume_text or not job_description:
            return {
                'overall_score': 0.0,
                'similarity_score': 0.0,
                'skills_match': 0.0,
                'tone_score': 0.0,
                'readability_score': 0.0
            }
        
        # TF-IDF similarity (40% weight)
        similarity_score = self.compute_tfidf_similarity(resume_text, job_description)
        
        # Skills matching (30% weight)
        resume_skills = set(self.extract_skills(resume_text))
        job_skills = set(self.extract_skills(job_description))
        
        if job_skills:
            skills_match = len(resume_skills.intersection(job_skills)) / len(job_skills)
        else:
            skills_match = 0.0
        
        # Tone analysis (15% weight)
        tone = self.analyze_tone(resume_text)
        tone_score = (tone['professional'] + tone['confident'] + tone['positive']) / 3
        
        # Readability (15% weight)
        readability = self.compute_readability_score(resume_text)
        readability_score = (readability['flesch_reading_ease'] + readability['flesch_kincaid_grade']) / 2
        
        # Weighted overall score
        overall_score = (
            similarity_score * 0.40 +
            skills_match * 0.30 +
            tone_score * 0.15 +
            readability_score * 0.15
        )
        
        return {
            'overall_score': round(overall_score * 100, 2),
            'similarity_score': round(similarity_score * 100, 2),
            'skills_match': round(skills_match * 100, 2),
            'tone_score': round(tone_score * 100, 2),
            'readability_score': round(readability_score * 100, 2),
            'tone_breakdown': tone,
            'readability_breakdown': readability
        }
    
    def analyze_resume(self, filepath: str, job_description: str) -> Dict:
        """Main method to analyze a resume"""
        # Parse document
        resume_text = self.parse_document(filepath)
        
        if not resume_text.strip():
            raise Exception("Could not extract text from the document")
        
        # Extract skills
        skills = self.extract_skills(resume_text)
        
        # Compute ATS score
        ats_scores = self.compute_ats_score(resume_text, job_description)
        
        # Extract key information
        word_count = len(resume_text.split())
        char_count = len(resume_text)
        
        return {
            'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text,
            'skills': skills,
            'word_count': word_count,
            'char_count': char_count,
            'ats_scores': ats_scores,
            'recommendations': self.generate_recommendations(ats_scores, skills, job_description)
        }
    
    def generate_recommendations(self, scores: Dict, skills: List[str], job_description: str) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if scores['overall_score'] < 50:
            recommendations.append("Your resume has a low ATS score. Consider improving keyword matching with the job description.")
        
        if scores['similarity_score'] < 50:
            recommendations.append("Low similarity with job description. Try incorporating more relevant keywords and phrases from the job posting.")
        
        if scores['skills_match'] < 50:
            job_skills = set(self.extract_skills(job_description))
            missing_skills = job_skills - set(skills)
            if missing_skills:
                recommendations.append(f"Consider highlighting these skills: {', '.join(list(missing_skills)[:5])}")
        
        if scores['tone_score'] < 60:
            recommendations.append("Enhance the professional tone of your resume. Use action verbs and quantify achievements.")
        
        if scores['readability_score'] < 60:
            recommendations.append("Improve readability by using shorter sentences and clearer structure.")
        
        if not recommendations:
            recommendations.append("Your resume looks good! Keep up the great work.")
        
        return recommendations

