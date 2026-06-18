import './PredictionCard.css'

export default function PredictionCard({ direction = 'N/A', confidence = 0, outlook = 'neutral' }) {
  const isUp = direction === 'UP'
  const confidencePct = (confidence * 100).toFixed(1)

  const outlookConfig = {
    bullish: { label: 'Bullish', cls: 'bullish', icon: '↑' },
    bearish: { label: 'Bearish', cls: 'bearish', icon: '↓' },
    neutral: { label: 'Neutral', cls: 'neutral', icon: '→' },
  }

  const o = outlookConfig[outlook] || outlookConfig.neutral

  return (
    <div className="prediction-card glass-card">
      {/* Direction */}
      <div className="pred-direction-row">
        <div className={`pred-arrow ${isUp ? 'up' : 'down'}`}>
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            {isUp ? (
              <><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></>
            ) : (
              <><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></>
            )}
          </svg>
        </div>
        <div className="pred-direction-info">
          <span className="pred-direction-label">Direction</span>
          <span className={`pred-direction-value ${isUp ? 'text-green' : 'text-red'}`}>
            {direction}
          </span>
        </div>
      </div>

      {/* Confidence bar */}
      <div className="pred-confidence">
        <div className="pred-confidence-header">
          <span className="pred-confidence-label">Model Confidence</span>
          <span className="pred-confidence-value mono">{confidencePct}%</span>
        </div>
        <div className="pred-confidence-track">
          <div
            className={`pred-confidence-bar ${isUp ? 'green' : 'red'}`}
            style={{ width: `${confidencePct}%` }}
          />
          <div className="pred-confidence-marker" style={{ left: '50%' }} />
        </div>
      </div>

      {/* Combined Outlook */}
      <div className="pred-outlook">
        <span className="pred-outlook-label">Combined Outlook</span>
        <span className={`badge badge-${o.cls}`}>
          {o.icon} {o.label}
        </span>
      </div>
    </div>
  )
}
