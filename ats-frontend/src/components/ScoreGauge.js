// src/components/ScoreGauge.js
import React from 'react';

function ScoreGauge({ score }) {
  // Calculate color based on score
  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50'; // Green
    if (score >= 60) return '#FFC107'; // Yellow
    return '#F44336'; // Red
  };

  const color = getScoreColor(score);
  
  return (
    <div className="score-gauge">
      <h3>ATS Compatibility Score</h3>
      <div className="gauge-container">
        <div className="gauge">
          <div 
            className="gauge-fill" 
            style={{ 
              width: `${score}%`,
              backgroundColor: color
            }}
          ></div>
        </div>
        <div className="gauge-value" style={{ color }}>
          {score}/100
        </div>
      </div>
      <p className="score-description">
        {score >= 80 ? (
          'Your resume is well-matched to this job description!'
        ) : score >= 60 ? (
          'Your resume matches partially with this job description.'
        ) : (
          'Your resume needs significant improvements for this job.'
        )}
      </p>
    </div>
  );
}

export default ScoreGauge;