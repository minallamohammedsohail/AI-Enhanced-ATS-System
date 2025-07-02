// src/App.js
import React, { useState } from 'react';
import './App.css';
import Uploader from './components/Uploader';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (resumeFile, jobDescription) => {
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('job_description', jobDescription);
      
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to analyze resume');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Resume Analyzer</h1>
        <p>Upload your resume and job description to get AI-powered insights</p>
      </header>
      
      <main className="App-main">
        {!results && (
          <div className="input-container">
            <Uploader onSubmit={handleSubmit} />
          </div>
        )}
        
        {loading && <div className="loading">Analyzing your resume...</div>}
        
        {error && <div className="error">Error: {error}</div>}
        
        {results && (
          <div className="results-container">
            <ResultsDisplay results={results} />
            <button 
              className="reset-button"
              onClick={() => setResults(null)}
            >
              Analyze Another Resume
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;