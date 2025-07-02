import React from 'react';

function MissingKeywords({ keywords }) {
  return (
    <div className="missing-keywords">
      <h3>Missing Keywords</h3>
      {keywords.length > 0 ? (
        <div className="keywords-container">
          {keywords.map((keyword, index) => (
            <span key={index} className="keyword-pill">
              {keyword}
            </span>
          ))}
        </div>
      ) : (
        <p>Great job! You've included all important keywords.</p>
      )}
    </div>
  );
}

export default MissingKeywords;