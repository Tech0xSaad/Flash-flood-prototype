import React, { useEffect, useRef } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const RISK_COLORS = {
  LOW:      '#22c55e',
  MODERATE: '#eab308',
  HIGH:     '#f97316',
  SEVERE:   '#ef4444',
}

const RISK_BG = {
  LOW:      '#dcfce7',
  MODERATE: '#fef9c3',
  HIGH:     '#ffedd5',
  SEVERE:   '#fee2e2',
}

// Only pan when the selected location actually changes (not on every render)
function MapController({ center }) {
  const map     = useMap()
  const prevRef = useRef(null)

  useEffect(() => {
    if (!center) return
    const key = center.join(',')
    if (key !== prevRef.current) {
      prevRef.current = key
      map.setView(center, map.getZoom(), { animate: true })
    }
  }, [center, map])

  return null
}

export default function FloodMap({ predictions, selectedLocation, onLocationSelect }) {
  const selected = predictions.find((p) => p.location_id === selectedLocation)
  const center = selected
    ? [selected.lat, selected.lng]
    : [27.41, 85.37]

  return (
    <div className="map-wrapper">
      <MapContainer
        center={[27.41, 85.37]}
        zoom={11}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapController center={center} />

        {predictions.map((p) => {
          const color     = RISK_COLORS[p.risk_level] || '#6b7280'
          const bgColor   = RISK_BG[p.risk_level] || '#f3f4f6'
          const isSelected = p.location_id === selectedLocation
          const radius    = isSelected ? 18 : 13

          return (
            <CircleMarker
              key={p.location_id}
              center={[p.lat, p.lng]}
              radius={radius}
              pathOptions={{
                color: isSelected ? '#1e3a5f' : color,
                fillColor: color,
                fillOpacity: 0.85,
                weight: isSelected ? 3 : 2,
              }}
              eventHandlers={{
                click: () => onLocationSelect(p.location_id),
              }}
            >
              <Popup>
                <div style={{ minWidth: 160, fontFamily: 'inherit' }}>
                  <div style={{
                    background: bgColor,
                    borderLeft: `4px solid ${color}`,
                    padding: '7px 10px',
                    borderRadius: 4,
                    marginBottom: 8,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: 8,
                  }}>
                    <strong style={{ fontSize: 13 }}>{p.location_name}</strong>
                    <span style={{
                      background: color,
                      color: '#fff',
                      fontSize: 10,
                      fontWeight: 700,
                      padding: '2px 7px',
                      borderRadius: 10,
                      whiteSpace: 'nowrap',
                    }}>
                      {p.risk_level}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 2px' }}>
                    <span style={{ color: '#6b7280' }}>Flood Probability</span>
                    <span style={{ fontWeight: 700, color, fontSize: 15 }}>
                      {p.flood_probability}%
                    </span>
                  </div>
                  <div style={{ fontSize: 10, color: '#9ca3af', marginTop: 6, padding: '0 2px' }}>
                    Click marker to select location
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          )
        })}
      </MapContainer>

      {/* Map legend */}
      <div className="map-legend">
        <div className="legend-title">Risk Level</div>
        {Object.entries(RISK_COLORS).map(([level, color]) => (
          <div key={level} className="legend-item">
            <span className="legend-dot" style={{ background: color }} />
            <span className="legend-label">{level}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
