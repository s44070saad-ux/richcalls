"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  supabase,
  isSupabaseConfigured,
  type PartnerApplication,
  type ApplicationStatus,
} from "@/lib/supabaseClient";

const STATUSES: ApplicationStatus[] = [
  "pending",
  "contacted",
  "in training",
  "active",
  "rejected",
];

export default function AdminPage() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [rows, setRows] = useState<PartnerApplication[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!supabase) return;
    const { data, error } = await supabase
      .from("partner_applications")
      .select("*")
      .order("created_at", { ascending: false });
    if (error) setError(error.message);
    else setRows((data as PartnerApplication[]) ?? []);
    setLoading(false);
  }, []);

  useEffect(() => {
    if (!supabase) {
      setLoading(false);
      return;
    }
    supabase.auth.getUser().then(({ data }) => {
      if (!data.user) {
        router.replace("/login");
        return;
      }
      setUserEmail(data.user.email ?? "");
      load();
    });
  }, [load, router]);

  async function setStatus(id: string, status: ApplicationStatus) {
    if (!supabase) return;
    const { error } = await supabase
      .from("partner_applications")
      .update({ status })
      .eq("id", id);
    if (error) setError(error.message);
    else
      setRows((r) => r.map((x) => (x.id === id ? { ...x, status } : x)));
  }

  async function signOut() {
    await supabase?.auth.signOut();
    router.replace("/login");
  }

  return (
    <main className="admin-wrap">
      <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <h1 style={{ fontSize: "1.7rem", margin: "6px 0 2px" }}>Partner applications</h1>
          <p className="muted" style={{ margin: 0 }}>
            {userEmail ? `Signed in as ${userEmail}` : "Rich Calls admin"}
          </p>
        </div>
        <button className="btn btn-ghost" onClick={signOut}>Sign out</button>
      </div>

      <div className="admin-card">
        {!isSupabaseConfigured ? (
          <p className="err">Supabase is not connected yet — environment variables are missing.</p>
        ) : loading ? (
          <p>Loading applications…</p>
        ) : error ? (
          <p className="err" role="alert">{error}</p>
        ) : rows.length === 0 ? (
          <p>No applications yet. Submitted applications will appear here.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Ref</th>
                <th>Applicant</th>
                <th>Contact</th>
                <th>Campaign</th>
                <th>Device / Hours</th>
                <th>Screening reply</th>
                <th>Received</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td><b>{r.reference_code}</b></td>
                  <td>
                    {r.full_name}
                    <br />
                    <span style={{ color: "#5b6b82" }}>
                      {r.city ? `${r.city}, ` : ""}{r.country}
                      {r.languages ? ` · ${r.languages}` : ""}
                      {r.english_level ? ` · ${r.english_level}` : ""}
                    </span>
                    {r.referral && <><br /><span style={{ color: "#5b6b82" }}>Ref: {r.referral}</span></>}
                  </td>
                  <td>
                    {r.whatsapp}
                    <br />
                    <span style={{ color: "#5b6b82" }}>{r.email}</span>
                  </td>
                  <td>{r.campaign ?? "—"}</td>
                  <td>
                    {r.device ?? "—"}
                    <br />
                    <span style={{ color: "#5b6b82" }}>
                      {r.hours ?? ""}{r.shift_availability ? ` · ${r.shift_availability}` : ""}
                    </span>
                  </td>
                  <td style={{ maxWidth: 260, whiteSpace: "pre-wrap" }}>{r.screening_reply ?? "—"}</td>
                  <td>{new Date(r.created_at).toLocaleString()}</td>
                  <td>
                    <select
                      className="status-select"
                      value={r.status}
                      onChange={(e) => setStatus(r.id, e.target.value as ApplicationStatus)}
                      aria-label={`Status for ${r.reference_code}`}
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <p style={{ marginTop: 18 }}>
        <a href="/">← Back to Rich Calls home</a>
      </p>
    </main>
  );
}
