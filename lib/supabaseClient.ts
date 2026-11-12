import { createClient, type SupabaseClient } from "@supabase/supabase-js";

export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
export const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "";

export const isSupabaseConfigured = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);

/** Browser Supabase client (anon/publishable key only — never a service key). */
export const supabase: SupabaseClient | null = isSupabaseConfigured
  ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
  : null;

export type ApplicationStatus =
  | "pending"
  | "contacted"
  | "in training"
  | "active"
  | "rejected";

export interface PartnerApplication {
  id: string;
  reference_code: string;
  full_name: string;
  country: string;
  city: string | null;
  whatsapp: string;
  email: string;
  languages: string | null;
  english_level: string | null;
  device: string | null;
  hours: string | null;
  shift_availability: string | null;
  experience: string | null;
  campaign: string | null;
  screening_reply: string | null;
  referral: string | null;
  about: string | null;
  status: ApplicationStatus;
  created_at: string;
}
