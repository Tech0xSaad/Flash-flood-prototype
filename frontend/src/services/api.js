import axios from 'axios'

// Use relative paths so Vite's dev proxy handles routing to the backend.
// In production, configure a reverse proxy (e.g. nginx) to forward /api → :8000.
const api = axios.create({
  baseURL: '',
  timeout: 10000,
})

export const getLocations = async () => {
  const { data } = await api.get('/api/locations')
  return data.locations
}

export const predict = async (locationId, scenario) => {
  const { data } = await api.post('/api/predict', {
    location_id: locationId,
    scenario,
  })
  return data
}

export const predictAll = async (scenario) => {
  const { data } = await api.get(`/api/predict/all?scenario=${scenario}`)
  return data.predictions
}

export const getSummary = async () => {
  const { data } = await api.get('/api/summary')
  return data
}

export default api
