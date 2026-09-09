import React from 'react';
import { Terminal, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-[#050505] border-t border-neutral-800 py-12 text-neutral-400 text-xs font-mono">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          
          {/* Brand & Mission */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center">
              <Terminal className="w-4 h-4 text-teal-400" />
            </div>
            <div>
              <p className="text-sm font-bold text-neutral-100 font-sans">CampusClimb</p>
              <p className="text-[11px] text-neutral-400 font-sans">
                Semantic PYQ Deduplication & Academic Study Intelligence
              </p>
            </div>
          </div>

          {/* Nav Links */}
          <div className="flex items-center gap-6 text-neutral-300 font-medium">
            <a href="#features" className="hover:text-teal-400 transition-colors">[Features]</a>
            <a href="#how-it-works" className="hover:text-teal-400 transition-colors">[Pipeline]</a>
            <a href="#benchmarks" className="hover:text-teal-400 transition-colors">[Metrics]</a>
            <Link to="/login" className="hover:text-teal-400 transition-colors">[Sign In]</Link>
          </div>

          {/* System Status */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-neutral-900 border border-neutral-800 text-[11px]">
            <span className="w-2 h-2 rounded-full bg-teal-400" />
            <span className="text-neutral-300">Backend API v1 Active</span>
          </div>

        </div>

        <div className="mt-8 pt-6 border-t border-neutral-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-neutral-500 font-sans">
          <p>© 2026 CampusClimb. All rights reserved. Powered by CAPT-M Transformer & Supabase.</p>
          <div className="flex items-center gap-1 text-neutral-400 font-mono text-[10px]">
            <span>Clean-97 Benchmarked NLP Engine</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
