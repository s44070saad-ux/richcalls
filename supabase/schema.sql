-- Rich Calls — partner_applications schema
-- Run in the Supabase SQL Editor of the NEW "richcalls" project only.
-- Never run this in the PharmaHub (hkigldiypjninnnvxlnb) or Velora/menuqr
-- (owrbvnjptzbbufghoilt) projects.

create extension if not exists pgcrypto;

create table if not exists public.partner_applications (
  id uuid primary key default gen_random_uuid(),
  reference_code text not null unique,
  full_name text not null,
  country text not null,
  city text,
  whatsapp text not null,
  email text not null,
  languages text,
  english_level text,
  device text,
  hours text,
  shift_availability text,
  experience text,
  campaign text,
  screening_reply text,
  referral text,
  about text,
  status text not null default 'pending'
    check (status in ('pending','contacted','in training','active','rejected')),
  created_at timestamptz not null default now()
);

alter table public.partner_applications enable row level security;

-- Anyone (anon) may submit an application. Inserts always start as 'pending'.
drop policy if exists "anyone can submit an application" on public.partner_applications;
create policy "anyone can submit an application"
  on public.partner_applications
  for insert
  to anon, authenticated
  with check (status = 'pending');

-- Only Saad's admin accounts may read applications.
drop policy if exists "admin can read applications" on public.partner_applications;
create policy "admin can read applications"
  on public.partner_applications
  for select
  to authenticated
  using ((auth.jwt() ->> 'email') in ('s44070saad@gmail.com', 'saadxj8@gmail.com'));

-- Only Saad's admin accounts may change application status / rows.
drop policy if exists "admin can update applications" on public.partner_applications;
create policy "admin can update applications"
  on public.partner_applications
  for update
  to authenticated
  using ((auth.jwt() ->> 'email') in ('s44070saad@gmail.com', 'saadxj8@gmail.com'))
  with check ((auth.jwt() ->> 'email') in ('s44070saad@gmail.com', 'saadxj8@gmail.com'));

drop policy if exists "admin can delete applications" on public.partner_applications;
create policy "admin can delete applications"
  on public.partner_applications
  for delete
  to authenticated
  using ((auth.jwt() ->> 'email') in ('s44070saad@gmail.com', 'saadxj8@gmail.com'));
