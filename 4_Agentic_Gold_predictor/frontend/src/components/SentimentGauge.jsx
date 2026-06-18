import { useEffect, useRef } from 'react'
import './SentimentGauge.css'

export default function SentimentGauge({ score = 0, rationale = '' }) {
  const needleRef = useRef(null)

  // Map score from [-1, 1] to angle [–90°, +90°]
  const angle = score * 90

  // Determine sentiment label
  const getLabel = () => {
    if (score >= 0.5) return { text: 'Bullish', cls: 'bullish' }
    if (score >= 0.15) return { text: 'Mildly Bullish', cls: 'bullish' }
    if (score > -0.15) return { text: 'Neutral', cls: 'neutral' }
    if (score > -0.5) return { text: 'Mildly Bearish', cls: 'bearish' }
    return { text: 'Bearish', cls: 'bearish' }
  }

  const label = getLabel()

  useEffect(() => {
    if (needleRef.current) {
      needleRef.current.style.transform = `rotate(${angle}deg)`
    }
  }, [angle])

  return (
    <div className="sentiment-gauge glass-card">
      <div className="gauge-container">
        <svg viewBox="0 0 200 120" className="gauge-svg">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth="12"
            strokeLinecap="round"
          />
          {/* Gradient arc */}
          <defs>
            <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="var(--red)" />
              <stop offset="35%" stopColor="var(--amber)" />
              <stop offset="50%" stopColor="#a3a3a3" />
              <stop offset="65%" stopColor="var(--gold-300)" />
              <stop offset="100%" stopColor="var(--green)" />
            </linearGradient>
          </defs>
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="url(#gaugeGrad)"
            strokeWidth="12"
            strokeLinecap="round"
            opacity="0.8"
          />
          {/* Center dot */}
          <circle cx="100" cy="100" r="5" fill="var(--text-muted)" />
          {/* Needle */}
          <g ref={needleRef} style={{ transformOrigin: '100px 100px', transition: 'transform 1s cubic-bezier(0.34, 1.56, 0.64, 1)' }}>
            <line
              x1="100" y1="100"
              x2="100" y2="30"
              stroke="var(--text-primary)"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            <circle cx="100" cy="100" r="4" fill="var(--text-primary)" />
          </g>
          {/* Labels */}
          <text x="15" y="118" fill="var(--red)" fontSize="9" fontWeight="600" fontFamily="var(--font-sans)">-1.0</text>
          <text x="91" y="18" fill="var(--text-muted)" fontSize="8" fontFamily="var(--font-sans)">0</text>
          <text x="170" y="118" fill="var(--green)" fontSize="9" fontWeight="600" fontFamily="var(--font-sans)">+1.0</text>
        </svg>
        <div className="gauge-score mono">{score.toFixed(2)}</div>
        <div className={`gauge-label badge badge-${label.cls}`}>{label.text}</div>
      </div>
      <div className="gauge-rationale">
        <p>{rationale}</p>
      </div>
    </div>
  )
}
