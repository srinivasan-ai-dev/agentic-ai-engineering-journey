import './MarketCard.css'

const ICONS = {
  gold: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><path d="M12 6v12M8 10l4-4 4 4"/>
    </svg>
  ),
  oil: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 2C6 8 2 12 2 16a10 10 0 0020 0c0-4-4-8-10-14z"/>
    </svg>
  ),
  dollar: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
    </svg>
  ),
  yield: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  ),
}

export default function MarketCard({ label, symbol, price, change, icon, suffix = '', delay = 0 }) {
  const isPositive = change >= 0
  const changeColor = isPositive ? 'var(--green)' : 'var(--red)'
  const changeGlow = isPositive ? 'var(--green-glow)' : 'var(--red-glow)'
  const arrow = isPositive ? '▲' : '▼'

  const formatPrice = (p) => {
    if (p == null || p === undefined) return 'N/A'
    return p >= 1000 ? p.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
                     : p.toFixed(2)
  }

  return (
    <div
      className={`market-card glass-card animate-fade-in-up animate-delay-${delay}`}
      style={{ '--accent': changeColor, '--accent-glow': changeGlow }}
    >
      <div className="market-card-header">
        <div className="market-card-icon" style={{ color: changeColor }}>
          {ICONS[icon]}
        </div>
        <span className="market-card-symbol mono">{symbol}</span>
      </div>
      <div className="market-card-price mono">
        {suffix === '%' ? '' : '$'}{formatPrice(price)}{suffix}
      </div>
      <div className="market-card-label">{label}</div>
      <div className="market-card-change" style={{ color: changeColor, background: changeGlow }}>
        <span>{arrow}</span>
        <span>{change != null ? Math.abs(change).toFixed(3) : '0.000'}%</span>
      </div>
    </div>
  )
}
