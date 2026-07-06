import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Home from './pages/Home'
import TryPage from './pages/TryPage'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Pricing from './pages/Pricing'
import DevConsolePage from './pages/DevConsolePage'
import AdminPage from './pages/AdminPage'
import PhoneSimulatorPage from './pages/PhoneSimulatorPage'
import JanAIWidget from './components/JanAIAgent/JanAIWidget'
import { AuthProvider } from './context/AuthContext'

const API_BASE = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_BASE || 'https://7hrrqf2fol.execute-api.us-east-1.amazonaws.com/prod'
const VAANI_API = import.meta.env.VITE_VAANI_API || 'https://d70je9he55.execute-api.us-east-1.amazonaws.com/prod'

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-white text-content-primary font-sans">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/try" element={<TryPage />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/pricing" element={<Pricing />} />
              {/* Dev tools — not in main nav */}
              <Route path="/dev" element={<DevConsolePage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/sim" element={<PhoneSimulatorPage />} />
            </Routes>
          </main>

          {/* Floating AI Agent — JanAI, JanAI's dedicated web assistant */}
          <JanAIWidget apiBaseUrl={API_BASE} janaiApiUrl={VAANI_API} />
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
