import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/QueryHistory.css'

function QueryHistory() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/queries/history?limit=100')
      setHistory(response.data)
    } catch (error) {
      console.error('Erreur:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette entrée ?')) {
      try {
        await axios.delete(`/api/queries/history/${id}`)
        fetchHistory()
      } catch (error) {
        alert('Erreur: ' + error.message)
      }
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('fr-FR')
  }

  return (
    <div className="history-container">
      <h2>📜 Historique des Requêtes</h2>

      {loading ? (
        <p>Chargement...</p>
      ) : history.length === 0 ? (
        <p className="empty-message">Aucun historique</p>
      ) : (
        <div className="history-list">
          {history.map(entry => (
            <div key={entry.id} className={`history-item ${entry.status}`}>
              <div className="history-item-header">
                <span className={`status-badge ${entry.status}`}>
                  {entry.status === 'success' ? '✓' : '✗'}
                </span>
                <span className="execution-time">{entry.execution_time}ms</span>
                <span className="timestamp">{formatDate(entry.created_at)}</span>
              </div>
              <div className="history-item-query">
                <code>{entry.query.substring(0, 200)}{entry.query.length > 200 ? '...' : ''}</code>
              </div>
              {entry.error_message && (
                <div className="error-message">{entry.error_message}</div>
              )}
              <button
                onClick={() => handleDelete(entry.id)}
                className="btn-danger-small"
              >
                🗑️ Supprimer
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default QueryHistory
