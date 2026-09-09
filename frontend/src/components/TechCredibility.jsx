import React from 'react';
import { motion } from 'motion/react';
import { Cpu, ShieldCheck, Database, GitMerge } from 'lucide-react';

export default function TechCredibility() {
  const specs = [
    {
      label: 'Model Architecture',
      value: 'Fine-Tuned MPNet-v2 (768-dim)',
      desc: 'Supervised sentence transformer fine-tuned on university exam question pairs.',
      icon: Cpu,
    },
    {
      label: 'Matching Metric',
      value: 'Semantic Cosine Distance',
      desc: 'Evaluates concept intent rather than surface keyword matching to group duplicates.',
      icon: GitMerge,
    },
    {
      label: 'Weighting Algorithm',
      value: 'Frequency & Recency Matrix',
      desc: 'Calculates mark probability by combining past paper frequency with recency weight.',
      icon: Database,
    },
  ];

  return (
    <section id="credibility" className="py-20 bg-[#0a0a0a] text-neutral-100 relative border-t border-neutral-800 font-mono">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mx-auto text-center space-y-3 mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Factual NLP Pipeline Credentials</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-neutral-100 tracking-tight font-sans">
            Engineered on Validated Academic NLP Benchmarks
          </h2>
          <p className="text-neutral-400 text-sm font-sans">
            No hype or fake claims. CampusClimb is powered by standard high-accuracy vector embeddings and structured database mapping.
          </p>
        </div>

        {/* Specs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {specs.map((spec, idx) => {
            const Icon = spec.icon;
            return (
              <motion.div
                key={spec.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="glass-card p-6 rounded-xl border border-neutral-800 text-left space-y-3"
              >
                <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-[10px] text-neutral-400 uppercase tracking-wider block">
                    {spec.label}
                  </span>
                  <h3 className="text-base font-bold text-neutral-100 mt-0.5">
                    {spec.value}
                  </h3>
                </div>
                <p className="text-xs text-neutral-400 leading-relaxed font-sans">
                  {spec.desc}
                </p>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
