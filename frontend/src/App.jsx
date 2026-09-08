import React, { useState, useEffect, useRef } from 'react'
import Header from './components/Header.jsx'
import ScenarioSelector from './components/ScenarioSelector.jsx'
import FloodMap from './components/FloodMap.jsx'
import RiskCard from './components/RiskCard.jsx'
import ConditionsPanel from './components/ConditionsPanel.jsx'
import WarningModal from './components/WarningModal.jsx'
import SystemFlow from './components/SystemFlow.jsx'
import StatusPanel from './components/StatusPanel.jsx'
import { getLocations, predict, predictAll } from './services/api.js'

export default function App() {
  const [locations, setLocations]               = useState([])
  const [selectedLocation, setSelectedLocation] = useState('valley_a')
  const [scenario, setScenario]                 = useState('normal')
  const [prediction, setPrediction]             = useState(null)
  const [allPredictions, setAllPredictions]     = useState([])
  const [loading, setLoading]                   = useState(false)
  const [showWarning, setShowWarning]           = useState(false)
  const [error, setError]                       = useState(null)
  const [lastUpdated, setLastUpdated]           = useState(null)

  // Keep a stable ref to locations so the prediction effect doesn't re-run
  // every time the locations array identity changes
  const locationsRef = useRef([])
  locationsRef.current = locations

  // Step 1 — load locations once on mount
  useEffect(() => {
    getLocations()
      .then(setLocations)
      .catch(() =>
        setError('Cannot reach backend. Make sure the API server is running on port 8000.')
      )
  }, [])

  // Step 2 — run prediction whenever location or scenario changes, but only
  // after locations have loaded. Using a single effect with explicit deps avoids
  // the double-fetch caused by the old useCallback + useEffect combo.
  useEffect(() => {
    if (locationsRef.current.length === 0) return

    let cancelled = false
    setLoading(true)
    setError(null)

    Promise.all([
      predict(selectedLocation, scenario),
      predictAll(scenario),
    ])
      .then(([pred, allPreds]) => {
        if (cancelled) return

        setPrediction(pred)

        // Merge lat/lng from stable ref — no dependency on locations state
        setAllPredictions(
          allPreds.map((p) => {
            const loc = locationsRef.current.find((l) => l.id === p.location_id)
            return { ...p, lat: loc?.lat, lng: loc?.lng }
          })
        )

        setLastUpdated(new Date())
        setShowWarning(['HIGH', 'SEVERE'].includes(pred.risk_level))
      })
      .catch(() => {
        if (!cancelled)
          setError('Prediction failed. Make sure the API server is running on port 8000.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  // locations.length as a trigger so the effect fires once locations arrive,
  // but we read the actual array from the ref to avoid stale-closure issues
  }, [selectedLocation, scenario, locations.length]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleLocationChange = (locId) => {
    setShowWarning(false)
    setSelectedLocation(locId)
  }

  const handleScenarioChange = (sc) => {
    setShowWarning(false)
    setScenario(sc)
  }

  return (
    <div className="app">
      <Header />

      {error && (
        <div className="error-banner">⚠ {error}</div>
      )}

      <div className="app-body">
        {/* Left sidebar */}
        <aside className="sidebar">
          <ScenarioSelector
            locations={locations}
            selectedLocation={selectedLocation}
            scenario={scenario}
            onLocationChange={handleLocationChange}
            onScenarioChange={handleScenarioChange}
          />

          <StatusPanel loading={loading} lastUpdated={lastUpdated} />

          <RiskCard prediction={prediction} loading={loading} />

          <ConditionsPanel prediction={prediction} />
        </aside>

        {/* Main map + pipeline */}
        <main className="main-content">
          <FloodMap
            predictions={allPredictions}
            selectedLocation={selectedLocation}
            onLocationSelect={handleLocationChange}
          />
          <SystemFlow />
        </main>
      </div>

      {showWarning && (
        <WarningModal
          prediction={prediction}
          onClose={() => setShowWarning(false)}
        />
      )}
    </div>
  )
}
