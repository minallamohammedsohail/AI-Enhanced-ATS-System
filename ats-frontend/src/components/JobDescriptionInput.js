import React from 'react';

function JobDescriptionInput({ jobDescription, setJobDescription }) {
  return (
    <div className="job-description-container">
      <h2>Job Description</h2>
      <textarea
        placeholder="Paste the job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        className="job-description-input"
        rows={10}
      />
    </div>
  );
}

export default JobDescriptionInput;