import React from 'react'

export default function StatusPanel({ loading, lastUpdated }) {
  const timeStr = lastUpdated
    ? lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : '—'

  return (
    <div className="status-panel">
      <div className="status-panel-title">System Status</div>
      <div className="status-rows">
        <div className="status-row">
          <span className="status-dot status-dot--sim" />
          <span className="status-key">Data Source</span>
          <span className="status-val">Simulation Data</span>
        </div>
        <div className="status-row">
          <span className="status-dot status-dot--active" />
          <span className="status-key">AI Model</span>
          <span className="status-val">Active</span>
        </div>
        <div className="status-row">
          <span className={`status-dot ${loading ? 'status-dot--loading' : 'status-dot--active'}`} />
          <span className="status-key">Prediction</span>
          <span className="status-val">{loading ? 'Updating…' : `Updated ${timeStr}`}</span>
        </div>
      </div>
    </div>
  )
}
