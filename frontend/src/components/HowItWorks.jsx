import React from 'react';
import { motion } from 'motion/react';
import { UploadCloud, Network, FileCheck, Bot, CheckCircle } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Upload Syllabus & PYQs',
      description: 'Upload past year question papers and course syllabus in PDF or TXT format with instant file validation.',
      icon: UploadCloud,
    },
    {
      number: '02',
      title: 'CAPT-M Vector Clustering',
      description: 'Our 768-dimensional fine-tuned MPNet transformer evaluates question similarity to deduplicate repeat concepts.',
      icon: Network,
    },
    {
      number: '03',
      title: 'Generate Master Blueprint',
      description: 'Receive a prioritized study schedule ranked by mark weightage and past exam repetition frequency.',
      icon: FileCheck,
    },
    {
      number: '04',
      title: 'Bilingual AI Q&A Engine',
      description: 'Query any topic in English or Hinglish to get confidence-ranked, exam-ready answers with step-by-step logic.',
      icon: Bot,
    },
  ];

  return (
    <section id="how-it-works" className="py-20 bg-grid-pattern relative border-t border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl sm:text-4xl font-extrabold text-neutral-100 tracking-tight"
          >
            How CampusClimb Transforms Study Prep
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-neutral-400 text-base sm:text-lg"
          >
            From raw exam PDFs to structured, high-probability topic mastery in 4 automated pipeline steps.
          </motion.p>
        </div>

        {/* Steps Flow */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 font-mono">
          {steps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={step.number}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.1 }}
                className="glass-card rounded-xl p-6 border border-neutral-800 relative group hover:border-teal-500/40 transition-all duration-200 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 group-hover:scale-105 transition-transform duration-200">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-2xl font-extrabold text-neutral-700 group-hover:text-teal-400 transition-colors">
                      {step.number}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-neutral-100 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-neutral-400 text-xs leading-relaxed font-sans">
                    {step.description}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-neutral-800/80 flex items-center gap-1.5 text-[11px] text-teal-400 font-medium">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Pipeline Step {step.number}</span>
                </div>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
