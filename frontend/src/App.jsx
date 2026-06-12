import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Button } from './components/ui/button'
import { Progress } from './components/ui/progress'
import { Textarea } from './components/ui/textarea'
import { Label } from './components/ui/label'
import { Badge } from './components/ui/badge'
import { Upload, FileText, TrendingUp, CheckCircle2, AlertCircle, Loader2, ClipboardPaste, ArrowRightLeft, X } from 'lucide-react'
import axios from 'axios'
import ScoreChart from './components/ScoreChart'
import Recommendations from './components/Recommendations'

function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jdFile, setJdFile] = useState(null)
  const [jdInputMode, setJdInputMode] = useState('text') // 'text' or 'file'
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      if (selectedFile.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB')
        return
      }
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleJdFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      if (selectedFile.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB')
        return
      }
      setJdFile(selectedFile)
      setError(null)
    }
  }

  const toggleJdMode = () => {
    setJdInputMode(prev => prev === 'text' ? 'file' : 'text')
    setJdFile(null)
    setJobDescription('')
    setError(null)
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a resume file')
      return
    }
    if (jdInputMode === 'text' && !jobDescription.trim()) {
      setError('Please enter a job description')
      return
    }
    if (jdInputMode === 'file' && !jdFile) {
      setError('Please upload a job description file')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('resume', file)
      if (jdInputMode === 'file' && jdFile) {
        formData.append('job_description_file', jdFile)
        formData.append('job_description', '') // empty fallback
      } else {
        formData.append('job_description', jobDescription)
      }

      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResults(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while analyzing the resume')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI-Powered Applicant Tracking System
          </h1>
          <p className="text-lg text-gray-600">
            Intelligent resume screening and analysis powered by NLP and machine learning
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Input */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Upload Resume
                </CardTitle>
                <CardDescription>
                  Upload your resume in PDF or DOCX format
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="resume-upload">Resume File</Label>
                  <div className="mt-2 flex items-center gap-4">
                    <input
                      id="resume-upload"
                      type="file"
                      accept=".pdf,.docx,.doc"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                    <label
                      htmlFor="resume-upload"
                      className="flex items-center gap-2 px-4 py-2 border border-dashed rounded-lg cursor-pointer hover:bg-accent transition-colors"
                    >
                      <Upload className="h-4 w-4" />
                      {file ? file.name : 'Choose file'}
                    </label>
                    {file && (
                      <Badge variant="secondary" className="text-xs">
                        {(file.size / 1024).toFixed(2)} KB
                      </Badge>
                    )}
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <Label>Job Description</Label>
                    <button
                      type="button"
                      onClick={toggleJdMode}
                      className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors px-2 py-1 rounded-md hover:bg-accent"
                    >
                      <ArrowRightLeft className="h-3 w-3" />
                      {jdInputMode === 'text' ? 'Upload file instead' : 'Paste text instead'}
                    </button>
                  </div>

                  {jdInputMode === 'text' ? (
                    <Textarea
                      id="job-description"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                      className="min-h-[200px]"
                    />
                  ) : (
                    <div className="flex items-center gap-4 mt-1">
                      <input
                        id="jd-upload"
                        type="file"
                        accept=".pdf,.docx,.doc"
                        onChange={handleJdFileChange}
                        className="hidden"
                      />
                      <label
                        htmlFor="jd-upload"
                        className="flex items-center gap-2 px-4 py-2 border border-dashed rounded-lg cursor-pointer hover:bg-accent transition-colors"
                      >
                        <Upload className="h-4 w-4" />
                        {jdFile ? jdFile.name : 'Choose JD file (PDF/DOCX)'}
                      </label>
                      {jdFile && (
                        <>
                          <Badge variant="secondary" className="text-xs">
                            {(jdFile.size / 1024).toFixed(2)} KB
                          </Badge>
                          <button
                            type="button"
                            onClick={() => setJdFile(null)}
                            className="text-muted-foreground hover:text-destructive transition-colors"
                          >
                            <X className="h-4 w-4" />
                          </button>
                        </>
                      )}
                    </div>
                  )}
                </div>

                <Button
                  onClick={handleAnalyze}
                  disabled={loading || !file || (jdInputMode === 'text' ? !jobDescription.trim() : !jdFile)}
                  className="w-full"
                  size="lg"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="mr-2 h-4 w-4" />
                      Analyze Resume
                    </>
                  )}
                </Button>

                {error && (
                  <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
                    <AlertCircle className="h-4 w-4" />
                    <span className="text-sm">{error}</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {results && (
              <>
                {/* Overall Score */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5" />
                      ATS Score
                    </CardTitle>
                    <CardDescription>
                      Overall compatibility score with the job description
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center mb-4">
                      <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBgColor(results.ats_scores.overall_score)} mb-4`}>
                        <span className={`text-4xl font-bold ${getScoreColor(results.ats_scores.overall_score)}`}>
                          {results.ats_scores.overall_score}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">out of 100</p>
                    </div>
                    <Progress value={results.ats_scores.overall_score} className="h-3" />
                  </CardContent>
                </Card>

                {/* Detailed Scores */}
                <Card>
                  <CardHeader>
                    <CardTitle>Detailed Analysis</CardTitle>
                    <CardDescription>
                      Breakdown of different scoring factors
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ScoreChart scores={results.ats_scores} />
                    
                    <div className="mt-6 space-y-4">
                      <div>
                        <div className="flex justify-between mb-2">
                          <span className="text-sm font-medium">Similarity Score</span>
                          <span className="text-sm font-semibold">{results.ats_scores.similarity_score}%</span>
                        </div>
                        <Progress value={results.ats_scores.similarity_score} className="h-2" />
                      </div>
                      <div>
                        <div className="flex justify-between mb-2">
                          <span className="text-sm font-medium">Skills Match</span>
                          <span className="text-sm font-semibold">{results.ats_scores.skills_match}%</span>
                        </div>
                        <Progress value={results.ats_scores.skills_match} className="h-2" />
                      </div>
                      <div>
                        <div className="flex justify-between mb-2">
                          <span className="text-sm font-medium">Tone Score</span>
                          <span className="text-sm font-semibold">{results.ats_scores.tone_score}%</span>
                        </div>
                        <Progress value={results.ats_scores.tone_score} className="h-2" />
                      </div>
                      <div>
                        <div className="flex justify-between mb-2">
                          <span className="text-sm font-medium">Readability Score</span>
                          <span className="text-sm font-semibold">{results.ats_scores.readability_score}%</span>
                        </div>
                        <Progress value={results.ats_scores.readability_score} className="h-2" />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Skills */}
                {results.skills && results.skills.length > 0 && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Extracted Skills</CardTitle>
                      <CardDescription>
                        Skills identified in your resume
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {results.skills.map((skill, index) => (
                          <Badge key={index} variant="secondary">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Recommendations */}
                {results.recommendations && (
                  <Recommendations recommendations={results.recommendations} />
                )}

                {/* Resume Stats */}
                <Card>
                  <CardHeader>
                    <CardTitle>Resume Statistics</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Word Count</p>
                        <p className="text-2xl font-bold">{results.word_count}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Character Count</p>
                        <p className="text-2xl font-bold">{results.char_count}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}

            {!results && !loading && (
              <Card>
                <CardContent className="flex items-center justify-center h-64">
                  <div className="text-center text-gray-400">
                    <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Upload a resume and job description to get started</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

