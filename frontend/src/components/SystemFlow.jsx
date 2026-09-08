import React from 'react'

const STEPS = [
  { icon: '📡', label: 'Data', desc: 'Environmental sensors' },
  { icon: '⚙️', label: 'Processing', desc: 'Feature extraction' },
  { icon: '🤖', label: 'AI Model', desc: 'Random Forest' },
  { icon: '📊', label: 'Risk', desc: 'Probability score' },
  { icon: '🚨', label: 'Warning', desc: 'Alert generation' },
]

export default function SystemFlow() {
  return (
    <div className="system-flow">
      <div className="flow-title">System Pipeline</div>
      <div className="flow-steps">
        {STEPS.map((step, i) => (
          <React.Fragment key={step.label}>
            <div className="flow-step">
              <div className="flow-step-icon">{step.icon}</div>
              <div className="flow-step-label">{step.label}</div>
              <div className="flow-step-desc">{step.desc}</div>
            </div>
            {i < STEPS.length - 1 && (
              <div className="flow-arrow">→</div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  )
}
