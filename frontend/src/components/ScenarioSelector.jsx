import React from 'react'

const SCENARIOS = [
  {
    id: 'normal',
    label: 'Normal',
    description: 'Typical dry conditions',
    icon: '☀️',
  },
  {
    id: 'heavy_rain',
    label: 'Heavy Rain',
    description: 'Sustained heavy rainfall',
    icon: '🌧️',
  },
  {
    id: 'extreme_rain',
    label: 'Extreme Rain',
    description: 'Severe storm event',
    icon: '⛈️',
  },
]

export default function ScenarioSelector({ locations, selectedLocation, scenario, onLocationChange, onScenarioChange }) {
  return (
    <div className="control-panel">
      <div className="control-section">
        <label className="control-label">Select Location</label>
        <select
          className="select-input"
          value={selectedLocation}
          onChange={(e) => onLocationChange(e.target.value)}
        >
          {locations.map((loc) => (
            <option key={loc.id} value={loc.id}>
              {loc.name}
            </option>
          ))}
        </select>
      </div>

      <div className="control-section">
        <label className="control-label">Weather Scenario</label>
        <div className="scenario-buttons">
          {SCENARIOS.map((s) => (
            <button
              key={s.id}
              className={`scenario-btn ${scenario === s.id ? 'scenario-btn--active' : ''}`}
              onClick={() => onScenarioChange(s.id)}
            >
              <span className="scenario-icon">{s.icon}</span>
              <span className="scenario-label">{s.label}</span>
              <span className="scenario-desc">{s.description}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
