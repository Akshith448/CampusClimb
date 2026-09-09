import React from 'react';
import { motion } from 'motion/react';
import { Layers, BarChart3, Languages, Sparkles, Terminal } from 'lucide-react';

export default function ProblemSolution() {
  const features = [
    {
      id: 'dedup',
      title: 'CAPT-M Semantic Deduplication',
      subtitle: 'Zero Duplicate Studying',
      description: 'Our custom fine-tuned MPNet transformer evaluates semantic intent instead of exact keyword matching. Multiple question variations get merged into 1 master concept.',
      badge: '83.0% Top-3 Recall (Clean-97)',
      icon: Layers,
      accentColor: 'text-teal-400',
      detailVisual: (
        <div className="mt-4 p-3 bg-neutral-950 rounded-lg border border-neutral-800 font-mono text-[11px]">
          <div className="flex justify-between items-center text-neutral-400 mb-1.5">
            <span>Query 1: "What is B-Tree height?"</span>
            <span className="text-teal-400 font-bold">Cosine Dist: 0.88</span>
          </div>
          <div className="flex justify-between items-center text-neutral-400">
            <span>Query 2: "Calculate depth of B-Tree"</span>
            <span className="text-teal-300">Vector Clustered</span>
          </div>
        </div>
      )
    },
    {
      id: 'frequency',
      title: 'PYQ Weightage & Frequency Analysis',
      subtitle: 'Smart Exam Prioritization',
      description: 'Stop guessing what to revise. CampusClimb ranks every topic by historical frequency and weightage across past semester exams.',
      badge: 'Frequency & Recency Matrix',
      icon: BarChart3,
      accentColor: 'text-teal-400',
      detailVisual: (
        <div className="mt-4 grid grid-cols-3 gap-2 text-center font-mono">
          <div className="bg-neutral-900 p-2 rounded-lg border border-neutral-800">
            <span className="text-[10px] text-neutral-400 block">Unit 1</span>
            <span className="text-xs font-bold text-teal-400">High Yield</span>
          </div>
          <div className="bg-neutral-900 p-2 rounded-lg border border-neutral-800">
            <span className="text-[10px] text-neutral-400 block">Unit 2</span>
            <span className="text-xs font-bold text-amber-400">Med Yield</span>
          </div>
          <div className="bg-neutral-900 p-2 rounded-lg border border-neutral-800">
            <span className="text-[10px] text-neutral-400 block">Unit 3</span>
            <span className="text-xs font-bold text-teal-400">Priority Topic</span>
          </div>
        </div>
      )
    },
    {
      id: 'bilingual',
      title: 'Bilingual AI Doubt & Answer Engine',
      subtitle: 'English + Hinglish Explanations',
      description: 'Get instant, step-by-step explanations tailored to university exam marking schemes. Ask doubts in simple English or Hinglish.',
      badge: 'Gemini LLM Layer',
      icon: Languages,
      accentColor: 'text-teal-400',
      detailVisual: (
        <div className="mt-4 p-3 bg-neutral-950 rounded-lg border border-neutral-800 flex items-center justify-between text-xs font-mono">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-400 text-[10px] border border-teal-500/20">
              Hindi + English
            </span>
            <span className="text-neutral-300">Exam-ready bullet points</span>
          </div>
          <Sparkles className="w-4 h-4 text-teal-400" />
        </div>
      )
    }
  ];

  return (
    <section id="features" className="py-20 bg-[#0a0a0a] dark:bg-[#0a0a0a] light:bg-neutral-100 relative border-t border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-3xl sm:text-4xl font-extrabold text-neutral-100 dark:text-neutral-100 light:text-neutral-900 tracking-tight"
          >
            Built Specifically for University Exam Blueprinting
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-neutral-400 text-base sm:text-lg"
          >
            Standard AI chatbots hallucinate vague answers. CampusClimb combines fine-tuned vector embeddings with past paper frequency analysis.
          </motion.p>
        </div>

        {/* Bento Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={feature.id}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                whileHover={{ y: -5, scale: 1.01 }}
                className="glass-card glass-card-hover rounded-xl p-6 relative overflow-hidden flex flex-col justify-between border border-neutral-800"
              >
                <div>
                  {/* Top Badge & Icon */}
                  <div className="flex items-center justify-between mb-6 relative z-10 font-mono">
                    <div className="w-10 h-10 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center">
                      <Icon className={`w-5 h-5 ${feature.accentColor}`} />
                    </div>
                    <span className="text-[10px] font-semibold text-neutral-300 px-2.5 py-1 rounded-md bg-neutral-900 border border-neutral-800">
                      {feature.badge}
                    </span>
                  </div>

                  {/* Title & Subtitle */}
                  <span className="text-[11px] font-mono font-semibold uppercase tracking-wider text-neutral-400 block mb-1">
                    {feature.subtitle}
                  </span>
                  <h3 className="text-xl font-bold text-neutral-100 dark:text-neutral-100 light:text-neutral-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-neutral-400 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>

                {/* Detail Visual Footer */}
                <div className="relative z-10 pt-4">
                  {feature.detailVisual}
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
