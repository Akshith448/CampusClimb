import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { CheckCircle2, Sparkles } from 'lucide-react';

/**
 * WelcomeToast
 * Slide-up toast anchored to the bottom-right.
 * Props:
 *   visible  — boolean
 *   name     — string (user's display name or email prefix)
 *   onDone   — callback fired after auto-dismiss
 */
export default function WelcomeToast({ visible, name, onDone }) {
  React.useEffect(() => {
    if (!visible) return;
    const t = setTimeout(() => {
      onDone?.();
    }, 3200);
    return () => clearTimeout(t);
  }, [visible, onDone]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="welcome-toast"
          initial={{ opacity: 0, y: 32, scale: 0.94 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 24, scale: 0.94 }}
          transition={{ type: 'spring', stiffness: 340, damping: 26 }}
          className="fixed bottom-6 right-6 z-[9999] max-w-sm"
          role="status"
          aria-live="polite"
        >
          <div className="flex items-start gap-3 bg-[#141414] border border-teal-500/30 rounded-2xl px-5 py-4 shadow-[0_8px_32px_rgba(20,184,166,0.18)] backdrop-blur-md">
            {/* Icon with ping ring */}
            <div className="relative mt-0.5 shrink-0">
              <div className="w-8 h-8 rounded-full bg-teal-500/10 border border-teal-500/30 flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4 text-teal-400" />
              </div>
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-teal-400 rounded-full">
                <span className="absolute inset-0 rounded-full bg-teal-400 animate-ping opacity-75" />
              </span>
            </div>

            {/* Text */}
            <div className="min-w-0">
              <p className="text-sm font-bold text-neutral-100 font-sans flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                Welcome to CampusClimb!
              </p>
              <p className="text-xs text-neutral-400 font-sans mt-0.5 leading-relaxed">
                {name
                  ? `Great to have you, ${name}. Your account is ready.`
                  : 'Your account has been created. Redirecting…'}
              </p>
            </div>

            {/* Progress bar */}
            <motion.div
              className="absolute bottom-0 left-0 h-[2px] bg-teal-500/60 rounded-b-2xl"
              initial={{ width: '100%' }}
              animate={{ width: '0%' }}
              transition={{ duration: 3.2, ease: 'linear' }}
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
