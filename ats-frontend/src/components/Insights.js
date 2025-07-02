import React from 'react';

function Insights({ insights }) {
  return (
    <div className="insights">
      <h3>AI-Generated Insights</h3>
      
      <div className="insight-card">
        <h4>Tone & Formality</h4>
        <p>{insights.tone_analysis}</p>
      </div>
      
      <div className="insight-card">
        <h4>Resume Readability</h4>
        <p>{insights.readability}</p>
        <div className="readability-bar">
          <div 
            className="readability-fill"
            style={{ 
              width: `${insights.readability_score}%`,
              backgroundColor: 
                insights.readability_score >= 80 ? '#4CAF50' :
                insights.readability_score >= 60 ? '#FFC107' : '#F44336'
            }}
          ></div>
        </div>
        <div className="readability-score">
          Score: {insights.readability_score}/100
        </div>
      </div>
      
      <div className="insight-card">
        <h4>Achievement Quantification</h4>
        <p>{insights.achievement_analysis}</p>
        <ul className="achievement-suggestions">
          {insights.achievement_suggestions.map((suggestion, index) => (
            <li key={index}>{suggestion}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Insights;