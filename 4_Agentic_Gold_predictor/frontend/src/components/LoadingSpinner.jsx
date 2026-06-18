import './LoadingSpinner.css'

export default function LoadingSpinner() {
  const steps = [
    'Fetching live market data...',
    'Scanning macroeconomic news...',
    'Running sentiment analysis...',
    'Executing ML prediction model...',
    'Generating intelligence report...',
  ]

  return (
    <div className="loading-overlay animate-fade-in-up">
      <div className="loading-card glass-card">
        <div className="loading-ring">
          <div className="ring-outer"></div>
          <div className="ring-inner"></div>
          <svg className="ring-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v12M8 10l4-4 4 4"/>
          </svg>
        </div>
        <h3 className="loading-title">Analyzing Markets</h3>
        <div className="loading-steps">
          {steps.map((step, i) => (
            <div key={i} className="loading-step" style={{ animationDelay: `${i * 0.15}s` }}>
              <div className="step-dot"></div>
              <span>{step}</span>
            </div>
          ))}
        </div>
        <p className="loading-note">This may take 15-30 seconds</p>
      </div>
    </div>
  )
}
