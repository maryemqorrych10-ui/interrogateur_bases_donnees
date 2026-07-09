import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/QueryEditor.css'

function QueryEditor() {
  const [connections, setConnections] = useState([])
  const [selectedConnection, setSelectedConnection] = useState('')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchConnections()
  }, [])

  const fetchConnections = async () => {
    try {
      const response = await axios.get('/api/connections')
      setConnections(response.data)
      if (response.data.length > 0) {
        setSelectedConnection(response.data[0].id)
      }
    } catch (error) {
      console.error('Erreur:', error)
    }
  }

  const handleExecute = async () => {
    if (!selectedConnection || !query.trim()) {
      setError('Veuillez sélectionner une connexion et entrer une requête')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await axios.post('/api/queries/execute', {
        connection_id: parseInt(selectedConnection),
        query: query
      })
      setResults(response.data)
    } catch (error) {
      setError('Erreur: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (format) => {
    if (!results?.data) return
    try {
      const response = await axios.post('/api/queries/export', {
        format,
        data: results.data,
        filename: 'query_result'
      })
      const element = document.createElement('a')
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(response.data.data))
      element.setAttribute('download', response.data.filename)
      element.style.display = 'none'
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)
    } catch (error) {
      alert('Erreur lors de l\'export: ' + error.message)
    }
  }

  return (
    <div className="editor-container">
      <h2>📝 Éditeur de Requêtes</h2>

      <div className="editor-controls">
        <select
          value={selectedConnection}
          onChange={(e) => setSelectedConnection(e.target.value)}
          className="connection-select"
        >
          <option value="">Sélectionner une connexion...</option>
          {connections.map(conn => (
            <option key={conn.id} value={conn.id}>
              {conn.name} ({conn.type})
            </option>
          ))}
        </select>
        <button
          onClick={handleExecute}
          className="btn-primary"
          disabled={loading}
        >
          {loading ? 'Exécution...' : '▶ Exécuter'}
        </button>
      </div>

      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Entrez votre requête SQL ici..."
        className="query-editor"
        spellCheck="false"
      />

      {error && <div className="error-message">{error}</div>}

      {results && (
        <div className="results-container">
          <div className="results-header">
            <h3>📊 Résultats ({results.row_count} lignes)</h3>
            <div className="results-info">
              <span>Temps: {results.execution_time}ms</span>
              {results.success && (
                <>
                  <button onClick={() => handleExport('json')} className="btn-secondary">📥 JSON</button>
                  <button onClick={() => handleExport('csv')} className="btn-secondary">📥 CSV</button>
                </>
              )}
            </div>
          </div>

          {results.error ? (
            <div className="error-box">{results.error}</div>
          ) : (
            results.data && results.data.length > 0 ? (
              <div className="table-wrapper">
                <table className="results-table">
                  <thead>
                    <tr>
                      {results.columns.map(col => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {results.data.map((row, idx) => (
                      <tr key={idx}>
                        {results.columns.map(col => (
                          <td key={`${idx}-${col}`}>
                            {row[col] !== null ? String(row[col]) : <em>NULL</em>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="empty-message">Aucun résultat</div>
            )
          )}
        </div>
      )}
    </div>
  )
}

export default QueryEditor
