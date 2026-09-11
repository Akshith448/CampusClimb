import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sun, Moon, Menu, X, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function Navbar({ theme, toggleTheme }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-200 ${
        scrolled
          ? 'bg-[#0a0a0a]/90 dark:bg-[#0a0a0a]/90 light:bg-white/90 backdrop-blur-md border-b border-neutral-800 dark:border-neutral-800 light:border-neutral-200 py-3 shadow-xl'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center group-hover:border-teal-500/50 transition-all duration-200">
            <Terminal className="w-4 h-4 text-teal-400 group-hover:scale-110 transition-transform duration-200" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-neutral-100 dark:text-neutral-100 light:text-neutral-900 font-mono">
              CampusClimb
            </span>
            <span className="text-[10px] text-neutral-400 font-mono tracking-wider -mt-0.5">
              Semantic PYQ Engine
            </span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8 text-xs font-mono tracking-wide text-neutral-400 dark:text-neutral-400 light:text-neutral-600">
          <Link to="/dashboard" className="hover:text-teal-400 transition-colors duration-200 text-teal-300 font-semibold">
            [Dashboard]
          </Link>
          <a href="#features" className="hover:text-teal-400 transition-colors duration-200">
            [Features]
          </a>
          <a href="#how-it-works" className="hover:text-teal-400 transition-colors duration-200">
            [Pipeline]
          </a>
          <a href="#benchmarks" className="hover:text-teal-400 transition-colors duration-200 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
            [Metrics]
          </a>
          <a href="#credibility" className="hover:text-teal-400 transition-colors duration-200">
            [NLP Spec]
          </a>
        </nav>

        {/* Right Actions */}
        <div className="hidden md:flex items-center gap-4">
          {/* Light/Dark Toggle */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle Theme"
            className="p-2 rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 hover:text-teal-400 transition-all duration-200"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-teal-600" />}
          </button>

          <Link
            to="/login"
            className="text-xs font-mono text-neutral-400 hover:text-white transition-colors duration-200 px-2 py-1"
          >
            Sign In
          </Link>

          <Link
            to="/login"
            className="px-4 py-2 text-xs font-mono font-semibold rounded-lg bg-teal-600 hover:bg-teal-500 text-white shadow-md transition-all duration-200 flex items-center gap-1.5"
          >
            <span>Launch Engine</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Mobile Hamburger Toggle */}
        <div className="flex items-center gap-2 md:hidden">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-teal-600" />}
          </button>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 hover:text-white"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-[#0a0a0a] border-b border-neutral-800 px-4 py-6 space-y-4 font-mono text-xs"
          >
            <a
              href="#features"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-neutral-300 hover:text-teal-400 py-1"
            >
              [Features]
            </a>
            <a
              href="#how-it-works"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-neutral-300 hover:text-teal-400 py-1"
            >
              [Pipeline]
            </a>
            <a
              href="#benchmarks"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-neutral-300 hover:text-teal-400 py-1"
            >
              [Metrics]
            </a>
            <a
              href="#credibility"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-neutral-300 hover:text-teal-400 py-1"
            >
              [NLP Spec]
            </a>
            <div className="pt-4 border-t border-neutral-800 flex flex-col gap-3">
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full text-center py-2.5 rounded-lg border border-neutral-800 text-neutral-200 font-medium"
              >
                Sign In
              </Link>
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full text-center py-2.5 rounded-lg bg-teal-600 text-white font-semibold"
              >
                Launch Engine
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
