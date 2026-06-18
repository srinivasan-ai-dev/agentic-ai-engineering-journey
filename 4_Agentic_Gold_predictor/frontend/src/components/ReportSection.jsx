import ReactMarkdown from 'react-markdown'
import './ReportSection.css'

export default function ReportSection({ report = '' }) {
  if (!report) {
    return (
      <div className="report-section glass-card">
        <p className="text-muted">No report generated yet.</p>
      </div>
    )
  }

  return (
    <div className="report-section glass-card">
      <div className="report-content">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  )
}
