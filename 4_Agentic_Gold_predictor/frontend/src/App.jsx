import { useState, useEffect } from 'react'
import './App.css'
import MarketCard from './components/MarketCard'
import SentimentGauge from './components/SentimentGauge'
import PredictionCard from './components/PredictionCard'
import ReportSection from './components/ReportSection'
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/api/analyze')
      if (!res.ok) throw new Error(`API error: ${res.status}`)
      const result = await res.json()
      setData(result)
      setLastUpdated(new Date())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const market = data?.market_data || {}
  const prediction = data?.ml_prediction || {}

  // Determine overall outlook from report content
  const getOutlook = () => {
    if (!data?.final_report) return 'neutral'
    const report = data.final_report.toLowerCase()
    if (report.includes('**bullish**') || report.includes('verdict: bullish')) return 'bullish'
    if (report.includes('**bearish**') || report.includes('verdict: bearish')) return 'bearish'
    return 'neutral'
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header animate-fade-in-up">
        <div className="header-left">
          <div className="logo">
            <div className="logo-icon">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v12M8 10l4-4 4 4M8 14l4 4 4-4"/>
              </svg>
            </div>
            <div>
              <h1 className="logo-title">Gold Predictor</h1>
              <p className="logo-subtitle">Agentic AI Intelligence</p>
            </div>
          </div>
        </div>
        <div className="header-right">
          {lastUpdated && (
            <span className="last-updated mono">
              {lastUpdated.toLocaleTimeString()}
            </span>
          )}
          <button
            className={`analyze-btn ${loading ? 'loading' : ''}`}
            onClick={runAnalysis}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="btn-spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                </svg>
                Run Analysis
              </>
            )}
          </button>
        </div>
      </header>

      {/* Loading State */}
      {loading && <LoadingSpinner />}

      {/* Error State */}
      {error && (
        <div className="error-banner animate-fade-in-up">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          {error}
        </div>
      )}

      {/* Empty State */}
      {!data && !loading && !error && (
        <div className="empty-state animate-fade-in-up">
          <div className="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v12M8 10l4-4 4 4M8 14l4 4 4-4"/>
            </svg>
          </div>
          <h2>Ready to Analyze</h2>
          <p>Click <strong>Run Analysis</strong> to fetch live market data, analyze sentiment, and generate an AI-powered gold prediction.</p>
        </div>
      )}

      {/* Dashboard Content */}
      {data && !loading && (
        <main className="dashboard">
          {/* Market Overview Cards */}
          <section className="section animate-fade-in-up animate-delay-1">
            <h2 className="section-title">Market Overview</h2>
            <div className="market-grid">
              <MarketCard
                label="Gold"
                symbol="XAU"
                price={market.gold_price}
                change={market.gold_change}
                icon="gold"
                delay={1}
              />
              <MarketCard
                label="Crude Oil"
                symbol="WTI"
                price={market.oil_price}
                change={market.oil_change}
                icon="oil"
                delay={2}
              />
              <MarketCard
                label="Dollar Index"
                symbol="DXY"
                price={market.dxy_price}
                change={market.dxy_change}
                icon="dollar"
                delay={3}
              />
              <MarketCard
                label="10Y Treasury"
                symbol="TNX"
                price={market.yield_price}
                change={market.yield_change}
                icon="yield"
                suffix="%"
                delay={4}
              />
            </div>
          </section>

          {/* Analysis Row: Sentiment + ML Prediction */}
          <section className="analysis-row animate-fade-in-up animate-delay-3">
            <div className="analysis-col">
              <h2 className="section-title">Sentiment Analysis</h2>
              <SentimentGauge
                score={data.sentiment_score}
                rationale={data.sentiment_rationale}
              />
            </div>
            <div className="analysis-col">
              <h2 className="section-title">ML Prediction</h2>
              <PredictionCard
                direction={prediction.direction}
                confidence={prediction.confidence}
                outlook={getOutlook()}
              />
            </div>
          </section>

          {/* Full Report */}
          <section className="animate-fade-in-up animate-delay-5">
            <h2 className="section-title">Intelligence Report</h2>
            <ReportSection report={data.final_report} />
          </section>
        </main>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>Powered by XGBoost + Groq LLM + DuckDuckGo + yFinance</p>
      </footer>
    </div>
  )
}

export default App
