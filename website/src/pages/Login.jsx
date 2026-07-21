import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ArrowLeft, Loader2, LogIn } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showForgotModal, setShowForgotModal] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const [forgotMsg, setForgotMsg] = useState('')
  const [forgotErr, setForgotErr] = useState('')
  const [forgotLoading, setForgotLoading] = useState(false)

  const { login, forgotPassword } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !password) { setError('Please fill in all fields'); return }

    setLoading(true)
    setError('')

    try {
      await login(email, password)
      navigate('/profile')
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    }
    setLoading(false)
  }

  const handleForgotSubmit = async (e) => {
    e.preventDefault()
    if (!forgotEmail) { setForgotErr('Please enter your email address'); return }
    setForgotLoading(true)
    setForgotErr('')
    setForgotMsg('')

    try {
      await forgotPassword(forgotEmail)
      setForgotMsg('Password reset link has been sent to your email!')
    } catch (err) {
      setForgotErr(err.message || 'Failed to send reset link.')
    }
    setForgotLoading(false)
  }

  return (
    <div className="min-h-screen bg-surface-secondary pt-20 flex items-start justify-center">
      <div className="w-full max-w-md mx-auto px-6 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-sm text-content-secondary hover:text-accent-500 transition-colors mb-8">
          <ArrowLeft size={16} /> Back to Home
        </Link>

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
          <div className="text-center mb-8">
            <div className="w-14 h-14 bg-gradient-accent rounded-2xl flex items-center justify-center mx-auto mb-4">
              <LogIn size={24} className="text-white" />
            </div>
            <h1 className="text-2xl font-bold text-content-primary">Welcome Back</h1>
            <p className="text-sm text-content-secondary mt-1">Log in to your JanAI account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-content-primary mb-1.5">Email</label>
              <input
                type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-content-primary bg-white focus:border-accent-500 focus:ring-1 focus:ring-accent-500 outline-none transition-colors"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-sm font-medium text-content-primary">Password</label>
                <button
                  type="button"
                  onClick={() => { setForgotEmail(email); setShowForgotModal(true); setForgotMsg(''); setForgotErr(''); }}
                  className="text-xs font-semibold text-accent-500 hover:text-accent-600"
                >
                  Forgot Password?
                </button>
              </div>
              <input
                type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-content-primary bg-white focus:border-accent-500 focus:ring-1 focus:ring-accent-500 outline-none transition-colors"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <button
              type="submit" disabled={loading}
              className="btn-primary w-full text-base py-3.5 disabled:opacity-50"
            >
              {loading ? <><Loader2 size={18} className="animate-spin" /> Logging in...</> : 'Log In'}
            </button>
          </form>

          <p className="text-center text-sm text-content-secondary mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-accent-500 font-semibold hover:text-accent-600">Sign up</Link>
          </p>
        </div>

        {/* Forgot Password Modal */}
        {showForgotModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-sm w-full p-6 shadow-xl relative animate-in fade-in zoom-in-95">
              <h3 className="text-lg font-bold text-content-primary mb-1">Reset Password</h3>
              <p className="text-xs text-content-secondary mb-4">Enter your email address to receive a password reset link.</p>

              <form onSubmit={handleForgotSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-content-primary mb-1">Your Email</label>
                  <input
                    type="email" value={forgotEmail} onChange={(e) => setForgotEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm outline-none focus:border-accent-500"
                  />
                </div>

                {forgotErr && <p className="text-xs text-red-600 bg-red-50 p-2 rounded-lg">{forgotErr}</p>}
                {forgotMsg && <p className="text-xs text-green-600 bg-green-50 p-2 rounded-lg">{forgotMsg}</p>}

                <div className="flex gap-2 pt-2">
                  <button
                    type="button" onClick={() => setShowForgotModal(false)}
                    className="btn-secondary flex-1 text-sm py-2"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit" disabled={forgotLoading}
                    className="btn-primary flex-1 text-sm py-2 disabled:opacity-50"
                  >
                    {forgotLoading ? <Loader2 size={14} className="animate-spin mx-auto" /> : 'Send Reset Link'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
