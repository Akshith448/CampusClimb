import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'motion/react';
import axios from 'axios';
import {
  Terminal, ArrowLeft, ArrowRight, Lock, Mail,
  RefreshCw, AlertCircle, CheckCircle2, Eye, EyeOff,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { supabase, isSupabaseConfigured } from '../lib/supabase';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/* ─── Google G SVG (official brand mark) ───────────────────────────────── */
function GoogleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
      <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.35-8.16 2.35-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
      <path fill="none" d="M0 0h48v48H0z"/>
    </svg>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [mode, setMode]         = useState('login'); // 'login' | 'signup'
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const [emailError, setEmailError]       = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [apiError, setApiError]           = useState('');
  const [loading, setLoading]             = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  /* ── Client-side validation ─────────────────────────────────────────── */
  const validateForm = () => {
    let isValid = true;
    setEmailError('');
    setPasswordError('');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) {
      setEmailError('Email address is required.');
      isValid = false;
    } else if (!emailRegex.test(email.trim())) {
      setEmailError('Please enter a valid email address.');
      isValid = false;
    }

    if (!password) {
      setPasswordError('Password is required.');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters.');
      isValid = false;
    }

    return isValid;
  };

  /* ── Email / password submit ─────────────────────────────────────────── */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');

    if (!validateForm()) return;

    setLoading(true);
    try {
      const endpoint = mode === 'signup' ? '/api/v1/auth/signup' : '/api/v1/auth/login';
      const res = await axios.post(`${API_BASE_URL}${endpoint}`, {
        email: email.trim(),
        password,
      });

      if (res.data) {
        const token    = res.data.access_token || 'demo_token';
        const userData = res.data.user || { id: 'user_1', email: email.trim() };
        login(token, userData);
        navigate('/query');
      }
    } catch (err) {
      console.error('Auth Error:', err);
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        setApiError(detail);
      } else if (Array.isArray(detail) && detail[0]?.msg) {
        setApiError(detail[0].msg);
      } else {
        setApiError(
          `Authentication failed (${err.response?.status || 'network error'}). Please check credentials.`
        );
      }
    } finally {
      setLoading(false);
    }
  };

  /* ── Google OAuth ────────────────────────────────────────────────────── */
  const handleGoogleSignIn = async () => {
    if (!isSupabaseConfigured || !supabase) {
      setApiError(
        'Google Sign-In is not configured yet. Please add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY to frontend/.env.'
      );
      return;
    }

    setGoogleLoading(true);
    setApiError('');
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (error) throw error;
      // Supabase will redirect the browser to Google — no further action needed.
    } catch (err) {
      console.error('Google OAuth Error:', err);
      setApiError(err.message || 'Google Sign-In failed. Please try again.');
      setGoogleLoading(false);
    }
  };

  /* ── Animation Variants ──────────────────────────────────────────────── */
  const panelSpring = { type: 'spring', stiffness: 220, damping: 20 };

  const formStagger = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.06, delayChildren: 0.08 } },
  };

  const fieldVariant = {
    hidden: { opacity: 0, x: -14 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] } },
  };

  /* ── Render ──────────────────────────────────────────────────────────── */
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key="login-page"
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.98 }}
        transition={{ duration: 0.2 }}
        className="min-h-screen bg-[#0a0a0a] text-neutral-100 font-mono flex flex-col justify-between selection:bg-teal-600 selection:text-white bg-grid-pattern"
      >
        {/* ── Top Bar ── */}
        <header className="px-6 py-4 flex items-center justify-between border-b border-neutral-800 bg-[#0a0a0a]/90 backdrop-blur-md">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center group-hover:border-teal-500/50 transition-colors">
              <Terminal className="w-4 h-4 text-teal-400" />
            </div>
            <span className="text-sm font-bold tracking-tight text-neutral-100 font-mono">
              CampusClimb
            </span>
          </Link>

          <Link
            to="/"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-xs text-neutral-400 hover:text-white transition-all duration-200"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Home</span>
          </Link>
        </header>

        {/* ── Asymmetric Split Layout ── */}
        <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 flex items-center justify-center">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 w-full items-center">

            {/* ── Left: Form Panel ── */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={panelSpring}
              className="lg:col-span-6 max-w-md w-full mx-auto"
            >
              <div className="glass-card-elevated rounded-2xl p-6 sm:p-8 bg-[#141414] text-left">

                <motion.div variants={formStagger} initial="hidden" animate="visible" className="space-y-6">

                  {/* ── Header (badge REMOVED, replaced with secure lock hint) ── */}
                  <motion.div variants={fieldVariant}>
                    <h1 className="text-2xl sm:text-3xl font-extrabold text-neutral-100 font-sans tracking-tight">
                      {mode === 'login' ? 'Sign In to CampusClimb' : 'Create Student Account'}
                    </h1>
                    <p className="text-xs text-neutral-400 font-sans mt-1.5 leading-relaxed">
                      {mode === 'login'
                        ? 'Enter your credentials to access your semantic PYQ dashboard.'
                        : 'Register a new account to unlock confidence-ranked exam prep.'}
                    </p>
                  </motion.div>

                  {/* ── Mode Switcher ── */}
                  <motion.div
                    variants={fieldVariant}
                    className="relative flex bg-[#0a0a0a] rounded-xl p-1 border border-neutral-800 text-xs font-mono"
                  >
                    {['login', 'signup'].map((m) => (
                      <button
                        key={m}
                        type="button"
                        onClick={() => { setMode(m); setApiError(''); }}
                        className={`relative z-10 flex-1 py-2 rounded-lg font-semibold transition-colors duration-200 ${
                          mode === m ? 'text-white' : 'text-neutral-400 hover:text-neutral-200'
                        }`}
                      >
                        {mode === m && (
                          <motion.div
                            layoutId="activeModePill"
                            className="absolute inset-0 bg-teal-600 rounded-lg -z-10 shadow"
                            transition={{ type: 'spring', stiffness: 350, damping: 25 }}
                          />
                        )}
                        {m === 'login' ? 'Sign In Mode' : 'Sign Up Mode'}
                      </button>
                    ))}
                  </motion.div>

                  {/* ── API Error Banner (muted red) ── */}
                  {apiError && (
                    <motion.div
                      initial={{ opacity: 0, y: -6 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-3 bg-red-900/20 border border-red-800/40 rounded-xl text-xs text-red-300/90 flex items-start gap-2 font-sans"
                    >
                      <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-red-400/70" />
                      <span>{apiError}</span>
                    </motion.div>
                  )}

                  {/* ── Google Sign-In ── */}
                  <motion.div variants={fieldVariant}>
                    <motion.button
                      whileTap={{ scale: 0.97 }}
                      whileHover={{ backgroundColor: '#1c1c1c' }}
                      type="button"
                      onClick={handleGoogleSignIn}
                      disabled={googleLoading || loading}
                      className="w-full py-3 flex items-center justify-center gap-2.5 rounded-xl border border-neutral-700 bg-[#141414] hover:border-neutral-600 text-neutral-200 text-xs font-sans font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {googleLoading ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <GoogleIcon />
                      )}
                      <span>Continue with Google</span>
                    </motion.button>
                  </motion.div>

                  {/* ── Divider ── */}
                  <motion.div variants={fieldVariant} className="flex items-center gap-3">
                    <div className="flex-1 h-px bg-neutral-800" />
                    <span className="text-[10px] text-neutral-500 font-mono uppercase tracking-[0.06em]">or</span>
                    <div className="flex-1 h-px bg-neutral-800" />
                  </motion.div>

                  {/* ── Auth Form ── */}
                  <form onSubmit={handleSubmit} className="space-y-4">

                    {/* Email Field */}
                    <motion.div variants={fieldVariant} className="space-y-1.5">
                      <label className="text-[10px] font-mono font-semibold tracking-[0.07em] uppercase text-neutral-400 block">
                        Student Email Address
                      </label>
                      <div className={`input-well rounded-xl border ${
                        emailError ? 'border-red-500' : 'border-neutral-800'
                      } relative transition-all duration-200`}>
                        <input
                          id="login-email"
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="student@university.edu"
                          className="w-full bg-transparent text-neutral-100 text-xs rounded-xl px-3.5 py-3 pl-9 outline-none font-mono"
                          autoComplete="email"
                        />
                        <Mail className="w-4 h-4 text-neutral-500 absolute left-3 top-1/2 -translate-y-1/2" />
                      </div>
                      {emailError && <p className="text-[10px] text-red-400 font-sans mt-1">{emailError}</p>}
                    </motion.div>

                    {/* Password Field */}
                    <motion.div variants={fieldVariant} className="space-y-1.5">
                      <label className="text-[10px] font-mono font-semibold tracking-[0.07em] uppercase text-neutral-400 block">
                        Account Password
                      </label>
                      <div className={`input-well rounded-xl border ${
                        passwordError ? 'border-red-500' : 'border-neutral-800'
                      } relative transition-all duration-200`}>
                        <input
                          id="login-password"
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="••••••••••••"
                          className="w-full bg-transparent text-neutral-100 text-xs rounded-xl px-3.5 py-3 pl-9 pr-10 outline-none font-mono"
                          autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
                        />
                        <Lock className="w-4 h-4 text-neutral-500 absolute left-3 top-1/2 -translate-y-1/2" />
                        <button
                          type="button"
                          tabIndex={-1}
                          onClick={() => setShowPassword((v) => !v)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-teal-400 transition-colors"
                          aria-label={showPassword ? 'Hide password' : 'Show password'}
                        >
                          {showPassword ? (
                            <EyeOff className="w-4 h-4" />
                          ) : (
                            <Eye className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                      {passwordError && <p className="text-[10px] text-red-400 font-sans mt-1">{passwordError}</p>}
                    </motion.div>

                    {/* Submit Button */}
                    <motion.div variants={fieldVariant} className="pt-2">
                      <motion.button
                        whileTap={{ scale: 0.97 }}
                        type="submit"
                        disabled={loading || googleLoading}
                        className="w-full py-3.5 bg-teal-600 hover:bg-teal-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-mono font-bold text-xs tracking-[0.06em] uppercase rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-[0_4px_16px_rgba(20,184,166,0.3)]"
                      >
                        {loading ? (
                          <>
                            <RefreshCw className="w-4 h-4 animate-spin text-white" />
                            <span>Processing Request...</span>
                          </>
                        ) : (
                          <>
                            <span>{mode === 'login' ? 'Authenticate & Enter' : 'Complete Registration'}</span>
                            <ArrowRight className="w-4 h-4" />
                          </>
                        )}
                      </motion.button>
                    </motion.div>
                  </form>
                </motion.div>
              </div>
            </motion.div>

            {/* ── Right: Engine Preview Panel ── */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ ...panelSpring, delay: 0.1 }}
              className="lg:col-span-6 hidden lg:block text-left"
            >
              <div className="glass-card rounded-2xl p-6 sm:p-8 bg-[#111111] border border-neutral-800/90 shadow-2xl relative space-y-4 font-mono">
                <div className="flex items-center justify-between border-b border-neutral-800 pb-4">
                  <div className="flex items-center gap-2 text-xs text-neutral-300">
                    <div className="w-2 h-2 rounded-full bg-teal-400 animate-ping" />
                    <span>Engine Output Blueprint</span>
                  </div>
                  <span className="text-[10px] text-teal-400 bg-teal-500/10 px-2.5 py-0.5 rounded border border-teal-500/20 font-bold tabular-nums">
                    83.0% Clean-97 Benchmark
                  </span>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="p-4 bg-[#0a0a0a] rounded-xl border border-neutral-800">
                    <span className="text-[10px] text-neutral-400 uppercase tracking-[0.06em] block mb-1">
                      Matched Concept Space
                    </span>
                    <span className="text-neutral-200 font-semibold">
                      Process Synchronization &amp; Deadlocks
                    </span>
                  </div>

                  <div className="p-4 bg-[#0a0a0a] rounded-xl border border-neutral-800 space-y-2">
                    <span className="text-[10px] text-neutral-400 uppercase tracking-[0.06em] block">
                      Bilingual Output Layer
                    </span>
                    <p className="text-neutral-300 text-xs leading-relaxed font-sans">
                      &quot;Deadlock requires 4 Coffman conditions: Mutual Exclusion, Hold &amp; Wait, No Preemption, and Circular Wait.&quot;
                    </p>
                    <p className="text-teal-300 text-[11px] bg-teal-500/10 p-2.5 rounded-lg border border-teal-500/20">
                      <span className="text-teal-400 font-semibold">Hinglish:</span> &quot;Saari 4 conditions satisfy hone par deadlock hota hai.&quot;
                    </p>
                  </div>
                </div>

                <div className="pt-3 flex items-center justify-between text-[11px] text-neutral-400 border-t border-neutral-800">
                  <span className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
                    Secure Session
                  </span>
                  <span className="tabular-nums">FastAPI v1 Active</span>
                </div>
              </div>
            </motion.div>

          </div>
        </main>

        {/* ── Footer ── */}
        <footer className="py-4 text-center text-[11px] text-neutral-500 border-t border-neutral-800/80 font-sans">
          <span>CampusClimb Academic Intelligence Engine</span>
        </footer>
      </motion.div>
    </AnimatePresence>
  );
}
