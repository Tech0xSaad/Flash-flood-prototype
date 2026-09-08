import React from 'react'

const CONDITION_CARDS = [
  {
    key: 'rainfall_1h',
    label: 'Rainfall (1h)',
    unit: 'mm',
    icon: '🌧️',
    thresholds: [25, 55],
  },
  {
    key: 'rainfall_6h',
    label: 'Rainfall (6h)',
    unit: 'mm',
    icon: '💧',
    thresholds: [80, 150],
  },
  {
    key: 'soil_moisture',
    label: 'Soil Moisture',
    unit: '%',
    icon: '🌱',
    thresholds: [50, 75],
  },
  {
    key: 'slope',
    label: 'Slope',
    unit: '°',
    icon: '⛰️',
    thresholds: [25, 40],
  },
  {
    key: 'elevation',
    label: 'Elevation',
    unit: 'm',
    icon: '📏',
    thresholds: [null, null],  // no threshold colouring for elevation
  },
  {
    key: 'antecedent_rainfall',
    label: 'Prior Rainfall',
    unit: 'mm',
    icon: '📊',
    thresholds: [60, 110],
  },
]

function getValueColor(value, thresholds) {
  const [warn, danger] = thresholds
  if (!warn) return '#374151'
  if (value >= danger) return '#dc2626'
  if (value >= warn)   return '#d97706'
  return '#16a34a'
}

function formatValue(value) {
  return typeof value === 'number' ? value.toLocaleString() : value ?? '—'
}

export default function ConditionsPanel({ prediction }) {
  if (!prediction?.conditions) return null

  const { conditions } = prediction

  return (
    <div className="conditions-panel">
      <h3 className="panel-title">Environmental Conditions</h3>

      <div className="conditions-grid">
        {CONDITION_CARDS.map(({ key, label, unit, icon, thresholds }) => {
          const value = conditions[key]
          const color = getValueColor(value, thresholds)
          return (
            <div key={key} className="condition-card">
              <div className="condition-icon">{icon}</div>
              <div className="condition-body">
                <div className="condition-label">{label}</div>
                <div className="condition-value" style={{ color }}>
                  {formatValue(value)}
                  <span className="condition-unit"> {unit}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Land cover row */}
      <div className="land-cover-row">
        <span className="condition-label">Land Cover</span>
        <span className="land-cover-badge">
          {conditions.land_cover?.replace('_', ' ') || '—'}
        </span>
      </div>

      {/* Contributing factors — explainability section */}
      {prediction.factors?.length > 0 && (
        <div className="factors-section">
          <h3 className="panel-title" style={{ marginTop: 0 }}>
            Why is this location at risk?
          </h3>
          <ul className="factors-list">
            {prediction.factors.map((f, i) => (
              <li key={i} className="factor-item">
                <span className="factor-check">✓</span>
                {f}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
