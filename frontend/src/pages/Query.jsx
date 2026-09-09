import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { Terminal, LogOut, Search, Send, Sparkles, CheckCircle2, RefreshCw } from 'lucide-react';
import { motion } from 'motion/react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Query() {
  const { user, token, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [query, setQuery] = useState('');
  const [subject, setSubject] = useState('Operating Systems');
  const [language, setLanguage] = useState('English');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await axios.post(`${API_BASE_URL}/api/v1/agent/query`, {
        query,
        subject,
        language,
      });
      setResult(res.data);
    } catch (err) {
      console.error('Query error:', err);
      const apiErr = err.response?.data?.detail || 'Failed to map query to topic space.';
      setError(typeof apiErr === 'string' ? apiErr : JSON.stringify(apiErr));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-neutral-100 font-mono flex flex-col">
      {/* Header */}
      <header className="border-b border-neutral-800 bg-[#0a0a0a]/90 backdrop-blur-md px-6 py-4 flex items-center justify-between sticky top-0 z-50">
        <Link to="/" className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center">
            <Terminal className="w-4 h-4 text-teal-400" />
          </div>
          <span className="text-base font-bold tracking-tight text-white font-mono">
            CampusClimb <span className="text-xs text-teal-400 font-normal">/ Query Engine</span>
          </span>
        </Link>

        <div className="flex items-center gap-4 text-xs">
          <span className="text-neutral-400 hidden sm:inline">
            Auth: <span className="text-teal-400 font-semibold">{user?.email || 'Authenticated Student'}</span>
          </span>
          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 transition-colors"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Sign Out</span>
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8 space-y-8">
        
        {/* Search Panel */}
        <div className="glass-card rounded-xl p-6 border border-neutral-800 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-teal-400">
              <Sparkles className="w-4 h-4" />
              <span>CAPT-M Vector Matching & Bilingual Query Mode</span>
            </div>
            <span className="text-[10px] text-neutral-500 bg-neutral-900 px-2 py-0.5 rounded border border-neutral-800">
              Token Active
            </span>
          </div>

          <form onSubmit={handleSearch} className="space-y-4">
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask any question (e.g. Differentiate process vs thread with time complexity)..."
                  className="w-full bg-neutral-950 border border-neutral-800 focus:border-teal-500 text-neutral-200 text-sm rounded-lg px-4 py-3 outline-none transition-colors"
                />
                <Search className="w-4 h-4 text-neutral-500 absolute right-3.5 top-1/2 -translate-y-1/2" />
              </div>

              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="bg-neutral-950 border border-neutral-800 text-neutral-300 text-xs rounded-lg px-3 py-3 outline-none"
              >
                <option value="Operating Systems">Operating Systems</option>
                <option value="DBMS">DBMS</option>
                <option value="Computer Networks">Computer Networks</option>
              </select>

              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-neutral-950 border border-neutral-800 text-neutral-300 text-xs rounded-lg px-3 py-3 outline-none"
              >
                <option value="English">English</option>
                <option value="Hindi">Hindi / Hinglish</option>
              </select>

              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-teal-600 hover:bg-teal-500 disabled:opacity-50 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-2 uppercase tracking-wider"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                <span>Submit Query</span>
              </button>
            </div>
          </form>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 p-4 rounded-lg text-xs text-red-400">
            {error}
          </div>
        )}

        {/* Query Result Box */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card rounded-xl p-6 border border-teal-500/30 space-y-6 text-left"
          >
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-neutral-800 pb-4 text-xs">
              <span className="text-neutral-300 font-semibold">
                Matched Topic: <span className="text-teal-400">{result.matched_topic}</span>
              </span>
              <span className="text-teal-400 bg-teal-500/10 px-2.5 py-1 rounded border border-teal-500/20 font-bold">
                Confidence: {(result.confidence_score * 100).toFixed(1)}% ({result.confidence_label})
              </span>
            </div>

            <div>
              <h4 className="text-[11px] uppercase tracking-wider text-neutral-400 mb-1.5">
                Answer Output ({result.language})
              </h4>
              <p className="text-sm text-neutral-200 leading-relaxed bg-neutral-950 p-4 rounded-lg border border-neutral-800 font-sans">
                {result.answer}
              </p>
            </div>

            <div>
              <h4 className="text-[11px] uppercase tracking-wider text-neutral-400 mb-1.5">
                Concept Explanation
              </h4>
              <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed bg-neutral-950 p-4 rounded-lg border border-neutral-800">
                {result.explanation}
              </p>
            </div>

            {result.sources && result.sources.length > 0 && (
              <div>
                <h4 className="text-[11px] uppercase tracking-wider text-neutral-400 mb-2">
                  Retrieved Vector Note Sources ({result.sources.length})
                </h4>
                <div className="space-y-2">
                  {result.sources.map((src, i) => (
                    <div key={i} className="bg-neutral-950 p-3 rounded-lg border border-neutral-800 text-xs text-neutral-400 font-sans">
                      {src.text}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}

      </main>
    </div>
  );
}
