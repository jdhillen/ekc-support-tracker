-- Founder Support Tracker schema (Supabase / Postgres)
-- Run once in the Supabase SQL editor.

create table if not exists partners (
  id          serial primary key,
  name        text not null unique,
  focus       text not null
);

create table if not exists requests (
  id               serial primary key,
  title            text not null check (char_length(title) between 3 and 200),
  description      text not null default '',
  requester_name   text not null,
  requester_email  text not null,
  business_name    text not null default '',
  category         text not null check (category in ('capital','legal','talent','mentorship','marketing','other')),
  priority         text not null default 'medium' check (priority in ('low','medium','high')),
  status           text not null default 'new' check (status in ('new','referred','in_progress','resolved')),
  partner_id       integer references partners(id) on delete set null,
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now()
);

create index if not exists requests_status_idx  on requests (status);
create index if not exists requests_partner_idx on requests (partner_id);

-- The app connects as the table owner (which bypasses RLS). Enabling RLS with
-- no policies keeps these tables closed to Supabase's public REST API.
alter table partners enable row level security;
alter table requests enable row level security;
