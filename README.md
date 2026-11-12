# Rich Calls

Pay-per-call partner network site. Home Services is the primary campaign
(9 live trades), Furniture (beds & sofas, UK/USA) is secondary. Laptop / PC is
the preferred partner setup. Contracts and Ringba dashboards are held by the
operating partner; Rich Calls recruits and screens partners.

- Public site: `/` (homepage), `/home-services`, `/trades/[slug]`
  (plumbing, electrical, hvac, roofing, windows, solar, siding, landscaping,
  pest-control) — rendered from `content/site.html` by `app/[[...path]]/route.ts`.
- The application form submits to Supabase `partner_applications`
  (anon INSERT only; see `supabase/schema.sql`).
- Admin: `/login` then `/admin` — lists applications, status can be changed
  (pending / contacted / in training / active / rejected). RLS restricts
  reads/updates to Saad's admin emails.

## Env vars (Vercel)

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_SITE_URL`

## Regenerating content/site.html

`content/site.html` is generated from the partner-landing-page prototype by
`transform.py` (branding, Supabase form submission, extra fields, mobile
safety CSS). Re-run `python3 transform.py` after prototype changes.
