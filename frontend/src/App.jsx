import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Connections from './pages/Connections'
import QueryEditor from './pages/QueryEditor'
import QueryHistory from './pages/QueryHistory'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="logo">🗄️ Database Interrogator</h1>
            <ul className="nav-menu">
              <li><Link to="/">Connexions</Link></li>
              <li><Link to="/editor">Requêtes</Link></li>
              <li><Link to="/history">Historique</Link></li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Connections />} />
            <Route path="/editor" element={<QueryEditor />} />
            <Route path="/history" element={<QueryHistory />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
