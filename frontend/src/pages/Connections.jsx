import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/Connections.css'

function Connections() {
  const [connections, setConnections] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    type: 'postgresql',
    host: '',
    port: '',
    user: '',
    password: '',
    database: ''
  })

  useEffect(() => {
    fetchConnections()
  }, [])

  const fetchConnections = async () => {
    try {
      const response = await axios.get('/api/connections')
      setConnections(response.data)
    } catch (error) {
      console.error('Erreur lors du chargement des connexions:', error)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await axios.post('/api/connections', formData)
      setFormData({
        name: '',
        type: 'postgresql',
        host: '',
        port: '',
        user: '',
        password: '',
        database: ''
      })
      setShowForm(false)
      fetchConnections()
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleTest = async (id) => {
    try {
      const response = await axios.post(`/api/connections/${id}/test`)
      alert(response.data.message)
    } catch (error) {
      alert('Erreur: ' + (error.response?.data?.message || error.message))
    }
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette connexion ?')) {
      try {
        await axios.delete(`/api/connections/${id}`)
        fetchConnections()
      } catch (error) {
        alert('Erreur: ' + error.message)
      }
    }
  }

  return (
    <div className="connections-container">
      <div className="connections-header">
        <h2>🔗 Gestion des Connexions</h2>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary">
          {showForm ? 'Fermer' : '+ Nouvelle Connexion'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="connection-form">
          <div className="form-grid">
            <input
              type="text"
              name="name"
              placeholder="Nom de la connexion"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
            <select name="type" value={formData.type} onChange={handleInputChange}>
              <option value="postgresql">PostgreSQL</option>
              <option value="mysql">MySQL</option>
              <option value="sqlite">SQLite</option>
              <option value="mongodb">MongoDB</option>
            </select>
            <input
              type="text"
              name="host"
              placeholder="Hôte"
              value={formData.host}
              onChange={handleInputChange}
            />
            <input
              type="number"
              name="port"
              placeholder="Port"
              value={formData.port}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="user"
              placeholder="Utilisateur"
              value={formData.user}
              onChange={handleInputChange}
            />
            <input
              type="password"
              name="password"
              placeholder="Mot de passe"
              value={formData.password}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="database"
              placeholder="Base de données"
              value={formData.database}
              onChange={handleInputChange}
            />
          </div>
          <button type="submit" className="btn-success" disabled={loading}>
            {loading ? 'Création...' : 'Créer Connexion'}
          </button>
        </form>
      )}

      <div className="connections-list">
        {connections.length === 0 ? (
          <p className="empty-message">Aucune connexion pour le moment</p>
        ) : (
          connections.map(conn => (
            <div key={conn.id} className="connection-card">
              <div className="connection-info">
                <h3>{conn.name}</h3>
                <p><strong>Type:</strong> {conn.type}</p>
                {conn.host && <p><strong>Hôte:</strong> {conn.host}:{conn.port}</p>}
                {conn.database && <p><strong>Base:</strong> {conn.database}</p>}
                <span className={`status ${conn.is_active ? 'active' : 'inactive'}`}>
                  {conn.is_active ? '✓ Actif' : '✗ Inactif'}
                </span>
              </div>
              <div className="connection-actions">
                <button onClick={() => handleTest(conn.id)} className="btn-secondary">
                  Tester
                </button>
                <button onClick={() => handleDelete(conn.id)} className="btn-danger">
                  Supprimer
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Connections
