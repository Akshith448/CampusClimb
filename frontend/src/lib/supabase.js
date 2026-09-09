import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Guard: createClient will throw if URL is empty/placeholder
const isConfigured =
  supabaseUrl &&
  supabaseUrl !== 'YOUR_SUPABASE_URL_HERE' &&
  supabaseAnonKey &&
  supabaseAnonKey !== 'YOUR_SUPABASE_ANON_KEY_HERE';

export const supabase = isConfigured
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export const isSupabaseConfigured = isConfigured;
