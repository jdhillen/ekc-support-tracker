-- Demo data. Partner names are fictional placeholders.
insert into partners (name, focus) values
  ('Regional Small Business Development Center', 'Business planning, financials, SBA loan prep'),
  ('Community Legal Clinic',                     'Entity formation, contracts, IP basics'),
  ('Heartland Angel Network',                    'Pre-seed and seed investment'),
  ('Main Street Microloan Fund',                 'Microloans up to $50k'),
  ('Tech Talent Collective',                     'Recruiting, apprenticeships, internships'),
  ('Founder Mentor Network',                     'One-on-one mentorship with operators')
on conflict (name) do nothing;

insert into requests (title, description, requester_name, requester_email, business_name, category, priority, status, partner_id, created_at, updated_at) values
  ('Need seed funding for hardware pilot', 'Raising $250k to fund a 3-site pilot of our sensor kit.', 'Maya Ortiz', 'maya@example.com', 'FieldSense', 'capital', 'high', 'referred',
     (select id from partners where name = 'Heartland Angel Network'), now() - interval '9 days', now() - interval '7 days'),
  ('Help choosing LLC vs C-corp', 'Planning to raise outside money next year; unsure which entity to form.', 'Darnell Brooks', 'darnell@example.com', 'Brooks Logistics', 'legal', 'medium', 'resolved',
     (select id from partners where name = 'Community Legal Clinic'), now() - interval '14 days', now() - interval '3 days'),
  ('Hiring first two developers', 'Looking for junior devs; open to apprenticeship model.', 'Priya Shah', 'priya@example.com', 'ClinicFlow', 'talent', 'medium', 'in_progress',
     (select id from partners where name = 'Tech Talent Collective'), now() - interval '6 days', now() - interval '1 day'),
  ('Working capital for bakery expansion', 'Need ~$30k for a second oven and storefront buildout.', 'Luis Hernandez', 'luis@example.com', 'Panadería Sol', 'capital', 'high', 'new',
     null, now() - interval '1 day', now() - interval '1 day'),
  ('Go-to-market advice for B2B SaaS', 'First 10 customers came from network; need a repeatable channel.', 'Emily Chen', 'emily@example.com', 'Ledgerly', 'mentorship', 'low', 'referred',
     (select id from partners where name = 'Founder Mentor Network'), now() - interval '4 days', now() - interval '2 days'),
  ('Financial projections review', 'Bank asked for 3-year projections before considering a loan.', 'Sam Whitfield', 'sam@example.com', 'Whitfield Woodworks', 'capital', 'medium', 'in_progress',
     (select id from partners where name = 'Regional Small Business Development Center'), now() - interval '5 days', now() - interval '2 days'),
  ('Brand and website refresh', 'Rebranding ahead of a regional retail launch.', 'Aisha Johnson', 'aisha@example.com', 'Kindred Candles', 'marketing', 'low', 'new',
     null, now() - interval '2 hours', now() - interval '2 hours'),
  ('Trademark for product name', 'Want to protect our product name before launch.', 'Tom Nguyen', 'tom@example.com', 'Prairie Pet Co.', 'legal', 'medium', 'new',
     null, now() - interval '3 hours', now() - interval '3 hours');
