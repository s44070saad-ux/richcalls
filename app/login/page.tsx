"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase, isSupabaseConfigured } from "@/lib/supabaseClient";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase) return;
    setBusy(true);
    setError("");
    const res =
      mode === "signin"
        ? await supabase.auth.signInWithPassword({ email, password })
        : await supabase.auth.signUp({ email, password });
    setBusy(false);
    if (res.error) {
      setError(res.error.message);
      return;
    }
    router.push("/admin");
    router.refresh();
  }

  return (
    <main className="admin-wrap" style={{ maxWidth: 460 }}>
      <h1 style={{ fontSize: "1.7rem", margin: "10px 0 4px" }}>Rich Calls Admin</h1>
      <p className="muted" style={{ marginTop: 0 }}>
        Sign in to review partner applications.
      </p>
      <div className="admin-card">
        {!isSupabaseConfigured ? (
          <p className="err">Supabase is not connected yet — environment variables are missing.</p>
        ) : (
          <form onSubmit={submit} style={{ display: "grid", gap: 14 }}>
            <label>
              Email
              <input
                className="field-input"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
              />
            </label>
            <label>
              Password
              <input
                className="field-input"
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete={mode === "signin" ? "current-password" : "new-password"}
              />
            </label>
            {error && <p className="err" role="alert">{error}</p>}
            <button className="btn" type="submit" disabled={busy}>
              {busy ? "Please wait…" : mode === "signin" ? "Sign in" : "Create admin account"}
            </button>
            <button
              type="button"
              onClick={() => setMode(mode === "signin" ? "signup" : "signin")}
              style={{ background: "none", border: 0, color: "#2563eb", fontWeight: 600, cursor: "pointer", minHeight: 44 }}
            >
              {mode === "signin"
                ? "First time? Create the admin account"
                : "Already have an account? Sign in"}
            </button>
          </form>
        )}
      </div>
      <p style={{ marginTop: 18 }}>
        <a href="/">← Back to Rich Calls home</a>
      </p>
    </main>
  );
}
