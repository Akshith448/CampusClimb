import React from 'react';
import { motion } from 'motion/react';
import { ArrowRight, Terminal } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function CtaBanner() {
  return (
    <section className="py-20 relative overflow-hidden bg-grid-pattern border-t border-neutral-800">
      {/* Background Lab Mesh */}
      <div className="absolute inset-0 bg-gradient-to-r from-teal-950/20 via-neutral-950 to-teal-950/20 pointer-events-none" />
      <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-[550px] h-[250px] bg-teal-500/10 blur-[130px] rounded-full pointer-events-none" />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center space-y-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-neutral-900 border border-neutral-800 text-teal-400 text-xs font-mono"
        >
          <Terminal className="w-3.5 h-3.5" />
          <span>Ready for Semester Exam Blueprinting?</span>
        </motion.div>

        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-3xl sm:text-5xl font-extrabold text-neutral-100 tracking-tight"
        >
          Climb the Semester Leaderboard with <br className="hidden sm:inline" />
          <span className="text-gradient-teal">Semantic PYQ Intelligence</span>
        </motion.h2>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-neutral-400 text-base sm:text-lg max-w-2xl mx-auto"
        >
          Upload your course syllabus or past question papers to get instant deduplicated concept maps and bilingual explanations.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="pt-4 flex justify-center font-mono"
        >
          <Link
            to="/login"
            className="px-8 py-4 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs uppercase tracking-wider shadow-xl transition-all duration-200 flex items-center gap-2.5 group"
          >
            <span>Launch Engine</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
