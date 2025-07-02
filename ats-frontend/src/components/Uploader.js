import React, { useState } from 'react';
import JobDescriptionInput from './JobDescriptionInput';

function Uploader({ onSubmit }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [fileError, setFileError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileType = file.type;
      if (
        fileType === 'application/pdf' || 
        fileType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ) {
        setResumeFile(file);
        setFileError(null);
      } else {
        setResumeFile(null);
        setFileError('Please upload a PDF or DOCX file');
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (resumeFile && jobDescription.trim()) {
      onSubmit(resumeFile, jobDescription);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="uploader-form">
      <div className="file-upload-container">
        <h2>Upload Resume</h2>
        <input
          type="file"
          id="resume-upload"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          className="file-input"
        />
        <label htmlFor="resume-upload" className="file-label">
          {resumeFile ? resumeFile.name : 'Choose PDF or DOCX file'}
        </label>
        {fileError && <p className="error-message">{fileError}</p>}
      </div>
      
      <JobDescriptionInput 
        jobDescription={jobDescription}
        setJobDescription={setJobDescription}
      />
      
      <button 
        type="submit" 
        className="submit-button"
        disabled={!resumeFile || !jobDescription.trim()}
      >
        Analyze Resume
      </button>
    </form>
  );
}

export default Uploader;