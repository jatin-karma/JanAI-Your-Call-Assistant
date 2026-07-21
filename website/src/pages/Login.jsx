import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { ArrowLeft, Loader2, LogIn, KeyRound, MailCheck } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [searchParams] = useSearchParams()
  const [activeTab, setActiveTab] = useState('login') // 'login' | 'forgot' | 'reset'

  // Email login state
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Forgot password state
  const [forgotEmail, setForgotEmail] = useState('')
  const [forgotMsg, setForgotMsg] = useState('')
  const [forgotErr, setForgotErr] = useState('')
  const [forgotLoading, setForgotLoading] = useState(false)
  const [resetLink, setResetLink] = useState('')

  // Reset password state (from email link)
  const [resetToken, setResetToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [resetMsg, setResetMsg] = useState('')
  const [resetErr, setResetErr] = useState('')
  const [resetLoading, setResetLoading] = useState(false)
  const [resetDone, setResetDone] = useState(false)

  const { login, forgotPassword, resetPassword } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const tabParam = searchParams.get('tab')
    const tokenParam = searchParams.get('token')
    const emailParam = searchParams.get('email')
    if (tokenParam) {
      setActiveTab('reset')
      setResetToken(tokenParam)
      if (emailParam) setForgotEmail(emailParam)
    } else if (tabParam === 'forgot') {
      setActiveTab('forgot')
    }
  }, [searchParams])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !password) { setError('Please fill in all fields'); return }

    setLoading(true)
    setError('')

    try {
      await login(email, password)
      navigate('/profile')
    } catch (err) {
      setError(err.message || 'Login failed. Please check your email and password.')
    }
    setLoading(false)
  }

  const handleForgotSubmit = async (e) => {
    e.preventDefault()
    if (!forgotEmail) { setForgotErr('Please enter your email address'); return }
    setForgotLoading(true)
    setForgotErr('')
    setForgotMsg('')
    setResetLink('')

    try {
      const res = await forgotPassword(forgotEmail)
      setForgotMsg(`Password reset link has been generated and sent to ${forgotEmail}!`)
      if (res.reset_link) {
        setResetLink(res.reset_link)
      }
    } catch (err) {
      setForgotErr(err.message || 'Failed to send reset link.')
    }
    setForgotLoading(false)
  }

  const handleResetSubmit = async (e) => {
    e.preventDefault()
    if (!newPassword || newPassword.length < 8) {
      setResetErr('New password must be at least 8 characters long.')
      return
    }

    setResetLoading(true)
    setResetErr('')

    try {
      await resetPassword(forgotEmail || email, resetToken || 'demo', newPassword)
      setResetDone(true)
    } catch (err) {
      setResetErr(err.message || 'Failed to update password. Please try again.')
    }
    setResetLoading(false)
  }

  return (
    <div className="min-h-screen bg-surface-secondary pt-20 flex items-start justify-center">
      <div className="w-full max-w-md mx-auto px-6 py-12">
        <Link to="/" className="inline-flex items-center gap-2 text-sm text-content-secondary hover:text-accent-500 transition-colors mb-8">
          <ArrowLeft size={16} /> Back to Home
        </Link>

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
          <div className="text-center mb-6">
            <div className="w-14 h-14 bg-gradient-accent rounded-2xl flex items-center justify-center mx-auto mb-4">
              {activeTab === 'login' ? <LogIn size={24} className="text-white" /> : <KeyRound size={24} className="text-white" />}
            </div>
            <h1 className="text-2xl font-bold text-content-primary">
              {activeTab === 'login' ? 'Welcome Back' : activeTab === 'forgot' ? 'Reset Password' : 'Set New Password'}
            </h1>
            <p className="text-sm text-content-secondary mt-1">
              {activeTab === 'login' ? 'Log in to your JanAI account' : activeTab === 'forgot' ? 'We will send a reset link to your email' : 'Type your new password below'}
            </p>
          </div>

          {/* Prominent Tab Switcher */}
          <div className="flex bg-gray-50 rounded-xl p-1 mb-6 border border-gray-100 text-xs font-semibold">
            <button
              type="button"
              onClick={() => { setActiveTab('login'); setError(''); }}
              className={`flex-1 py-2 rounded-lg transition-all ${
                activeTab === 'login' ? 'bg-white text-content-primary shadow-sm' : 'text-content-secondary hover:text-content-primary'
              }`}
            >
              Log In
            </button>
            <button
              type="button"
              onClick={() => { setActiveTab('forgot'); setForgotEmail(email); setForgotErr(''); setForgotMsg(''); }}
              className={`flex-1 py-2 rounded-lg transition-all ${
                activeTab === 'forgot' || activeTab === 'reset' ? 'bg-white text-accent-600 shadow-sm' : 'text-content-secondary hover:text-content-primary'
              }`}
            >
              Forgot Password?
            </button>
          </div>

          {/* EMAIL LOGIN FORM */}
          {activeTab === 'login' && (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-content-primary mb-1.5">Email Address</label>
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
                    onClick={() => { setActiveTab('forgot'); setForgotEmail(email); setForgotErr(''); setForgotMsg(''); }}
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
          )}

          {/* FORGOT PASSWORD FORM (EMAIL LINK) */}
          {activeTab === 'forgot' && (
            <form onSubmit={handleForgotSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-medium text-content-primary mb-1.5">Registered Email Address</label>
                <input
                  type="email" value={forgotEmail} onChange={(e) => setForgotEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl text-content-primary bg-white focus:border-accent-500 focus:ring-1 focus:ring-accent-500 outline-none transition-colors"
                />
                <p className="text-xs text-content-tertiary mt-1">We will send a password reset link to this email address.</p>
              </div>

              {forgotErr && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl">
                  <p className="text-sm text-red-600">{forgotErr}</p>
                </div>
              )}

              {forgotMsg && (
                <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl space-y-2">
                  <div className="flex items-center gap-2 text-emerald-700 font-semibold text-sm">
                    <MailCheck size={18} /> Password Reset Link Dispatched!
                  </div>
                  <p className="text-xs text-emerald-800">{forgotMsg}</p>
                  {resetLink && (
                    <div className="pt-2 border-t border-emerald-200">
                      <p className="text-xs text-emerald-900 font-medium mb-1">🔗 Direct Link (Demo Access):</p>
                      <a
                        href={resetLink}
                        className="text-xs text-accent-600 font-mono underline break-all block"
                      >
                        {resetLink}
                      </a>
                    </div>
                  )}
                </div>
              )}

              <button
                type="submit" disabled={forgotLoading}
                className="btn-primary w-full text-base py-3.5 disabled:opacity-50"
              >
                {forgotLoading ? <><Loader2 size={18} className="animate-spin" /> Sending Email Link...</> : 'Send Password Reset Link →'}
              </button>

              <button
                type="button" onClick={() => setActiveTab('login')}
                className="w-full text-center text-sm text-content-secondary hover:text-content-primary mt-2"
              >
                ← Return to Log In
              </button>
            </form>
          )}

          {/* RESET PASSWORD FORM (TOKEN FROM LINK) */}
          {activeTab === 'reset' && (
            <div>
              {!resetDone ? (
                <form onSubmit={handleResetSubmit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-content-primary mb-1.5">New Password</label>
                    <input
                      type="password"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="Minimum 8 characters"
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl text-content-primary bg-white focus:border-accent-500 focus:ring-1 focus:ring-accent-500 outline-none"
                    />
                  </div>

                  {resetErr && (
                    <div className="p-3 bg-red-50 border border-red-200 rounded-xl">
                      <p className="text-sm text-red-600">{resetErr}</p>
                    </div>
                  )}

                  <button
                    type="submit" disabled={resetLoading}
                    className="btn-primary w-full text-base py-3.5 disabled:opacity-50"
                  >
                    {resetLoading ? <><Loader2 size={18} className="animate-spin" /> Updating Password...</> : 'Save & Update Password ✓'}
                  </button>
                </form>
              ) : (
                <div className="text-center py-4 space-y-4">
                  <div className="w-14 h-14 bg-emerald-50 rounded-full flex items-center justify-center mx-auto text-emerald-500 border border-emerald-100 font-bold text-xl">
                    ✓
                  </div>
                  <h3 className="text-xl font-bold text-content-primary">Password Reset Complete!</h3>
                  <p className="text-sm text-content-secondary">
                    Your password has been successfully updated. You are now logged in!
                  </p>
                  <button
                    type="button"
                    onClick={() => navigate('/profile')}
                    className="btn-primary w-full text-base py-3.5"
                  >
                    Go to Profile →
                  </button>
                </div>
              )}
            </div>
          )}

          <p className="text-center text-sm text-content-secondary mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-accent-500 font-semibold hover:text-accent-600">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
