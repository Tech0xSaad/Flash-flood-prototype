import React from 'react'

export default function Header() {
  return (
    <header className="header">
      <div className="header-left">
        <div className="header-icon">🌊</div>
        <div>
          <h1 className="header-title">AI-Powered Flash Flood Prediction</h1>
          <p className="header-subtitle">Hilly Region Early Warning System</p>
        </div>
      </div>
      <div className="header-right">
        <span className="demo-badge">Demonstration Prototype — Uses Synthetic Data</span>
      </div>
    </header>
  )
}
