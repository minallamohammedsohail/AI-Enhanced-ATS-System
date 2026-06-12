import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function ScoreChart({ scores }) {
  const data = [
    { name: 'Similarity', score: scores.similarity_score },
    { name: 'Skills', score: scores.skills_match },
    { name: 'Tone', score: scores.tone_score },
    { name: 'Readability', score: scores.readability_score },
  ]

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Bar dataKey="score" fill="hsl(var(--primary))" />
      </BarChart>
    </ResponsiveContainer>
  )
}

