import React from 'react';

function Suggestions({ suggestions }) {
  return (
    <div className="suggestions">
      <h3>Resume Improvement Suggestions</h3>
      <ul className="suggestions-list">
        {suggestions.map((suggestion, index) => (
          <li key={index}>{suggestion}</li>
        ))}
      </ul>
    </div>
  );
}

export default Suggestions;