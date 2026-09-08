import React, { useEffect } from 'react'

const LEVEL_META = {
  HIGH:   { bg: '#fff7ed', border: '#f97316', accent: '#ea580c', icon: '⚠️' },
  SEVERE: { bg: '#fef2f2', border: '#ef4444', accent: '#dc2626', icon: '🚨' },
}

const ACTIONS = {
  HIGH: [
    'Monitor local emergency broadcasts',
    'Prepare emergency supplies and evacuation bag',
    'Avoid low-lying roads and stream crossings',
    'Alert household members of the risk',
  ],
  SEVERE: [
    'Evacuate low-lying areas immediately',
    'Move to higher ground without delay',
    'Avoid all contact with floodwaters',
    'Call emergency services if in immediate danger',
    'Do not attempt to drive through flooded roads',
  ],
}

export default function WarningModal({ prediction, onClose }) {
  const level = prediction?.risk_level
  if (!prediction || !['HIGH', 'SEVERE'].includes(level)) return null

  const meta    = LEVEL_META[level]
  const actions = ACTIONS[level]

  // Close on Escape key
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-box"
        style={{ borderColor: meta.border, background: meta.bg }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="modal-header" style={{ borderBottomColor: meta.border }}>
          <div className="modal-title-row">
            <span className="modal-icon">{meta.icon}</span>
            <div>
              <div className="modal-title" style={{ color: meta.accent }}>
                FLASH FLOOD {level === 'SEVERE' ? 'EMERGENCY' : 'WARNING'}
              </div>
              <div className="modal-location">{prediction.location_name}</div>
            </div>
          </div>
          <button className="modal-close" onClick={onClose} aria-label="Close warning">✕</button>
        </div>

        {/* Stats */}
        <div className="modal-stats">
          <div className="modal-stat">
            <div className="modal-stat-value" style={{ color: meta.accent }}>
              {prediction.flood_probability}%
            </div>
            <div className="modal-stat-label">Flood Probability</div>
          </div>
          <div className="modal-stat-divider" />
          <div className="modal-stat">
            <div className="modal-stat-value" style={{ color: meta.accent }}>
              {prediction.risk_level}
            </div>
            <div className="modal-stat-label">Risk Level</div>
          </div>
          <div className="modal-stat-divider" />
          <div className="modal-stat">
            <div className="modal-stat-value" style={{ fontSize: 14, color: '#374151' }}>
              Next Few Hours
            </div>
            <div className="modal-stat-label">Forecast Window</div>
          </div>
        </div>

        {/* Message */}
        <p className="modal-message">{prediction.warning}</p>

        {/* Recommended actions */}
        <div className="modal-actions-section">
          <div className="modal-actions-title">Recommended Actions</div>
          <ul className="modal-actions-list">
            {actions.map((a, i) => (
              <li key={i} className="modal-action-item">
                <span className="modal-action-dot" style={{ background: meta.accent }} />
                {a}
              </li>
            ))}
          </ul>
        </div>

        <div className="modal-footer">
          <span className="modal-disclaimer">
            Demonstration prototype — synthetic data only. Not an official government warning.
          </span>
          <button
            className="modal-dismiss-btn"
            style={{ background: meta.accent }}
            onClick={onClose}
          >
            Acknowledge
          </button>
        </div>
      </div>
    </div>
  )
}
