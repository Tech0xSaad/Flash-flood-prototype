import React from 'react'

const RISK_META = {
  LOW:      { color: '#22c55e', bg: '#f0fdf4', border: '#bbf7d0', label: 'Low Risk'      },
  MODERATE: { color: '#d97706', bg: '#fffbeb', border: '#fde68a', label: 'Moderate Risk' },
  HIGH:     { color: '#ea580c', bg: '#fff7ed', border: '#fed7aa', label: 'High Risk'     },
  SEVERE:   { color: '#dc2626', bg: '#fef2f2', border: '#fecaca', label: 'Severe Risk'   },
}

function ProbabilityGauge({ probability, color }) {
  const clampedProb = Math.min(100, Math.max(0, probability))
  const circumference = 2 * Math.PI * 44  // r=44
  const dashOffset = circumference * (1 - clampedProb / 100)

  return (
    <div className="gauge-container">
      <svg width="120" height="120" viewBox="0 0 100 100">
        {/* Background circle */}
        <circle cx="50" cy="50" r="44" fill="none" stroke="#e5e7eb" strokeWidth="8" />
        {/* Progress circle */}
        <circle
          cx="50" cy="50" r="44"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          transform="rotate(-90 50 50)"
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
        <text x="50" y="46" textAnchor="middle" fontSize="20" fontWeight="700" fill={color}>
          {clampedProb}%
        </text>
        <text x="50" y="62" textAnchor="middle" fontSize="9" fill="#6b7280">
          probability
        </text>
      </svg>
    </div>
  )
}

export default function RiskCard({ prediction, loading }) {
  if (loading) {
    return (
      <div className="risk-card risk-card--loading">
        <div className="loading-spinner" />
        <p className="loading-text">Analysing conditions…</p>
      </div>
    )
  }

  if (!prediction) return null

  const meta = RISK_META[prediction.risk_level] || RISK_META.LOW

  return (
    <div
      className="risk-card"
      style={{ borderColor: meta.border, background: meta.bg }}
    >
      <div className="risk-card-header">
        <div>
          <div className="risk-location-name">{prediction.location_name}</div>
          <div
            className="risk-badge"
            style={{ background: meta.color }}
          >
            {prediction.risk_level}
          </div>
        </div>
        <ProbabilityGauge probability={prediction.flood_probability} color={meta.color} />
      </div>

      <div className="risk-meta-row">
        <div className="risk-meta-item">
          <span className="risk-meta-label">Forecast Window</span>
          <span className="risk-meta-value">Next Few Hours</span>
        </div>
        <div className="risk-meta-item">
          <span className="risk-meta-label">Status</span>
          <span className="risk-meta-value" style={{ color: meta.color, fontWeight: 700 }}>
            {meta.label}
          </span>
        </div>
      </div>

      {prediction.warning && (
        <div className="risk-warning" style={{ borderColor: meta.color, color: meta.color }}>
          <span className="warning-icon">⚠</span>
          <span>{prediction.warning}</span>
        </div>
      )}
    </div>
  )
}
