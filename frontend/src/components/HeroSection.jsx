import React, { useState } from 'react';
import { motion } from 'motion/react';
import { ArrowRight, CheckCircle2, Search, Play, Terminal } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HeroSection() {
  const [activeTab, setActiveTab] = useState('english');
  const demoQuery = "Differentiate B-Trees and B+ Trees with time complexity.";

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.08,
        delayChildren: 0.1,
      },
    },
  };

  const wordVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
  };

  return (
    <section className="relative pt-24 pb-16 lg:pt-32 lg:pb-28 overflow-hidden bg-grid-pattern">
      {/* Background Subtle Lab Glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[350px] bg-teal-600/10 blur-[140px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          
          {/* Left Hero Content */}
          <div className="lg:col-span-7 text-left space-y-6">
            
            {/* Tech Badge */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-neutral-900 border border-neutral-800 text-xs text-teal-400 font-mono font-medium"
            >
              <Terminal className="w-3.5 h-3.5 text-teal-400" />
              <span>CAPT-M Vector Transformer Pipeline</span>
              <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
            </motion.div>

            {/* Headline */}
            <motion.h1
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-neutral-100 dark:text-neutral-100 light:text-neutral-900 leading-[1.1]"
            >
              <motion.span variants={wordVariants} className="inline-block mr-2">
                Master
              </motion.span>
              <motion.span variants={wordVariants} className="inline-block mr-2">
                University
              </motion.span>
              <motion.span variants={wordVariants} className="inline-block mr-2">
                Exams
              </motion.span>
              <motion.span variants={wordVariants} className="inline-block mr-2">
                with
              </motion.span>
              <br className="hidden sm:inline" />
              <motion.span variants={wordVariants} className="inline-block text-gradient-teal">
                Semantic Intelligence
              </motion.span>
            </motion.h1>

            {/* Subtext */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="text-base sm:text-lg text-neutral-400 dark:text-neutral-400 light:text-neutral-600 max-w-[54ch] leading-relaxed"
            >
              Eliminate duplicate study time. CampusClimb clusters previous year questions by concept frequency and delivers confidence-ranked bilingual solutions.
            </motion.p>

            {/* Dual CTAs */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex flex-wrap items-center gap-4 pt-2 font-mono"
            >
              <Link
                to="/login"
                className="px-6 py-3.5 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs uppercase tracking-wider shadow-lg transition-all duration-200 flex items-center gap-2 group"
              >
                <span>Launch Engine</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
              </Link>
              <a
                href="#how-it-works"
                className="px-6 py-3.5 rounded-lg bg-neutral-900 hover:bg-neutral-800 text-neutral-300 hover:text-white font-semibold text-xs uppercase tracking-wider border border-neutral-800 transition-all duration-200 flex items-center gap-2"
              >
                <Play className="w-3.5 h-3.5 text-teal-400 fill-teal-400" />
                <span>View Pipeline</span>
              </a>
            </motion.div>

            {/* Validated Research Metrics Strip */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="pt-6 border-t border-neutral-800 grid grid-cols-3 gap-4 font-mono"
            >
              <div>
                <p className="text-2xl font-bold text-teal-400">83.0%</p>
                <p className="text-[11px] text-neutral-400 font-medium">Top-3 Recall (Clean-97)</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-neutral-200">768-dim</p>
                <p className="text-[11px] text-neutral-400 font-medium">MPNet Embeddings</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-teal-400">Hindi + Eng</p>
                <p className="text-[11px] text-neutral-400 font-medium">Bilingual Layer</p>
              </div>
            </motion.div>
          </div>

          {/* Right Hero Demo Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.94 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            whileHover={{ y: -4, transition: { duration: 0.2 } }}
            className="lg:col-span-5"
          >
            <div className="glass-card rounded-xl p-5 border border-neutral-800 shadow-2xl relative font-mono">
              
              {/* Header Badge */}
              <div className="flex items-center justify-between pb-4 border-b border-neutral-800 mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-teal-400 animate-ping" />
                  <span className="text-xs text-neutral-300 font-semibold uppercase tracking-wider">
                    CAPT-M Match Engine
                  </span>
                </div>
                <span className="text-[10px] text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20 font-bold">
                  Demo Sample Format
                </span>
              </div>

              {/* Sample Query Input Mock */}
              <div className="mb-4">
                <label className="text-[10px] font-semibold text-neutral-400 block mb-1.5 uppercase tracking-wider">
                  Sample PYQ Query
                </label>
                <div className="relative">
                  <input
                    type="text"
                    readOnly
                    value={demoQuery}
                    className="w-full bg-neutral-950 border border-neutral-800 text-neutral-200 text-xs rounded-lg px-3.5 py-2.5 pr-8 outline-none"
                  />
                  <Search className="w-4 h-4 text-neutral-400 absolute right-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>

              {/* Frequency Stats Placeholder */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="bg-neutral-900 p-2.5 rounded-lg border border-neutral-800">
                  <span className="text-[10px] text-neutral-400 block">Exam Frequency</span>
                  <span className="text-xs font-bold text-neutral-200 flex items-center gap-1 mt-0.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
                    — (Sample Match)
                  </span>
                </div>
                <div className="bg-neutral-900 p-2.5 rounded-lg border border-neutral-800">
                  <span className="text-[10px] text-neutral-400 block">Weightage Rank</span>
                  <span className="text-xs font-bold text-teal-400 mt-0.5 block">
                    High Yield Topic
                  </span>
                </div>
              </div>

              {/* Language Switcher Tabs */}
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-semibold text-neutral-400 uppercase tracking-wider">
                  Bilingual Output Preview
                </span>
                <div className="flex items-center bg-neutral-900 rounded-lg p-0.5 border border-neutral-800">
                  <button
                    onClick={() => setActiveTab('english')}
                    className={`px-2.5 py-1 text-[10px] font-medium rounded-md transition-all ${
                      activeTab === 'english'
                        ? 'bg-teal-600 text-white shadow'
                        : 'text-neutral-400 hover:text-neutral-200'
                    }`}
                  >
                    English
                  </button>
                  <button
                    onClick={() => setActiveTab('hindi')}
                    className={`px-2.5 py-1 text-[10px] font-medium rounded-md transition-all ${
                      activeTab === 'hindi'
                        ? 'bg-teal-600 text-white shadow'
                        : 'text-neutral-400 hover:text-neutral-200'
                    }`}
                  >
                    Hinglish
                  </button>
                </div>
              </div>

              {/* Solution Output Box */}
              <div className="bg-neutral-950 rounded-lg p-3.5 border border-neutral-800 text-left min-h-[110px]">
                {activeTab === 'english' ? (
                  <p className="text-xs text-neutral-300 leading-relaxed font-mono">
                    <span className="text-teal-400 font-semibold">Key Difference:</span> B-Trees store data in both internal and leaf nodes (Search O(log N)). B+ Trees store all actual record pointers in leaf nodes linked sequentially, making range queries significantly faster for database indexing.
                  </p>
                ) : (
                  <p className="text-xs text-neutral-300 leading-relaxed font-mono">
                    <span className="text-teal-400 font-semibold">मुख्य अंतर (Key Difference):</span> B-Tree mein data internal aur leaf dono nodes me hota hai. Jabki B+ Tree me saare data pointers sirf leaf nodes par hote hain aur ye sequentially linked hote hain, jisse database index me range queries fast ho jaati hain.
                  </p>
                )}
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
