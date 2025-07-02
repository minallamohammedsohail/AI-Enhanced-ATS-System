// src/components/ResultsDisplay.js
import React from 'react';
import ScoreGauge from './ScoreGauge';
import MissingKeywords from './MissingKeywords';
import Suggestions from './Suggestions';
import Insights from './Insights';

function ResultsDisplay({ results }) {
  return (
    <div className="results-display">
      <h2>Resume Analysis Results</h2>
      
      <div className="results-grid">
        <div className="score-section">
          <ScoreGauge score={results.ats_score} />
        </div>
        
        <div className="keywords-section">
          <MissingKeywords keywords={results.missing_keywords} />
        </div>
        
        <div className="suggestions-section">
          <Suggestions suggestions={results.improvement_suggestions} />
        </div>
        
        <div className="insights-section">
          <Insights insights={results.ai_insights} />
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;