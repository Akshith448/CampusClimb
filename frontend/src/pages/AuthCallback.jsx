import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'motion/react';
import { Terminal, RefreshCw } from 'lucide-react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';
import { useAuth } from '../context/AuthContext';
import WelcomeToast from '../components/WelcomeToast';

/**
 * Determine if this is the user's first sign-in.
 *
 * Strategy: compare created_at vs last_sign_in_at.
 * Supabase sets both timestamps on account creation.
 * If they differ by ≤ 15 seconds the user was literally just created.
 *
 * Fallback: check app_metadata.provider_token presence isn't reliable,
 * so we use the time delta approach as the primary signal.
 */
function isNewUser(user) {
  if (!user) return false;
  try {
    const created   = new Date(user.created_at).getTime();
    const lastSignIn = new Date(user.last_sign_in_at).getTime();
    return Math.abs(lastSignIn - created) <= 15_000; // 15-second window
  } catch {
    return false;
  }
}

/** Extract a friendly first name from the Supabase user object */
function getDisplayName(user) {
  if (!user) return '';
  // Google OAuth populates user_metadata.full_name or .name
  const full = user.user_metadata?.full_name || user.user_metadata?.name || '';
  if (full) return full.split(' ')[0]; // first name only
  // Fallback: email prefix
  return user.email?.split('@')[0] || '';
}

/* ─── Status messages shown while the callback resolves ─────────────────── */
const STATUS = {
  loading: 'Verifying session…',
  new:     'Account created! Just a moment…',
  returning: 'Welcome back! Redirecting…',
  error:   'Something went wrong. Redirecting to login…',
};

export default function AuthCallback() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [status, setStatus] = useState('loading');
  const [displayName, setDisplayName] = useState('');
  const [showToast, setShowToast] = useState(false);

  useEffect(() => {
    if (!isSupabaseConfigured || !supabase) {
      // Supabase not configured — shouldn't reach here normally
      navigate('/login', { replace: true });
      return;
    }

    let cancelled = false;

    const run = async () => {
      try {
        // getSession() exchanges the PKCE/implicit token from the URL hash automatically
        const { data: { session }, error } = await supabase.auth.getSession();

        if (cancelled) return;

        if (error || !session) {
          console.error('[AuthCallback] Session exchange failed.');
          setStatus('error');
          setTimeout(() => navigate('/login', { replace: true }), 2000);
          return;
        }

        const { user, access_token } = session;

        // Feed the Supabase JWT into AuthContext so the rest of the app
        // (including the backend, which validates via SUPABASE_JWT_SECRET) treats
        // this user as authenticated identically to email/password users.
        login(access_token, {
          id:    user.id,
          email: user.email,
          name:  user.user_metadata?.full_name || user.user_metadata?.name || user.email,
        });

        const firstTime = isNewUser(user);
        const name      = getDisplayName(user);

        setDisplayName(name);

        if (firstTime) {
          setStatus('new');
          setShowToast(true);
          // Toast auto-dismisses after 3.2 s (WelcomeToast handles this)
          // onDone callback does the navigation
        } else {
          setStatus('returning');
          // Small visual delay so the status message is visible, then navigate
          setTimeout(() => {
            if (!cancelled) navigate('/query', { replace: true });
          }, 600);
        }
      } catch (err) {
        console.error('[AuthCallback] Unexpected error during OAuth callback handling.');
        if (!cancelled) {
          setStatus('error');
          setTimeout(() => navigate('/login', { replace: true }), 2000);
        }
      }
    };

    run();
    return () => { cancelled = true; };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleToastDone = () => {
    navigate('/query', { replace: true });
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex flex-col items-center justify-center font-mono text-neutral-100">
      {/* Brand mark */}
      <motion.div
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        className="flex flex-col items-center gap-6"
      >
        <div className="w-12 h-12 rounded-xl bg-neutral-900 border border-neutral-800 flex items-center justify-center shadow-lg">
          <Terminal className="w-6 h-6 text-teal-400" />
        </div>

        <div className="text-center space-y-2">
          <p className="text-sm font-semibold text-neutral-300">
            {status === 'loading' || status === 'returning'
              ? STATUS[status]
              : status === 'new'
              ? STATUS.new
              : STATUS.error}
          </p>
          {(status === 'loading' || status === 'returning') && (
            <RefreshCw className="w-4 h-4 text-teal-400 animate-spin mx-auto mt-1" />
          )}
        </div>

        {/* Subtle animated progress dots */}
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-1.5 h-1.5 rounded-full bg-teal-500/60"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
            />
          ))}
        </div>
      </motion.div>

      {/* Welcome toast for new users — rendered at page level so it's above everything */}
      <WelcomeToast
        visible={showToast}
        name={displayName}
        onDone={handleToastDone}
      />
    </div>
  );
}
