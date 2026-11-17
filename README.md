# Ship-Ready Lite · 53 free skills for vibe-coded apps

**Your app works. Now make it safe to launch.**
53 Agent Skills (+ a router and a free quick scan) for Claude Code, Cursor, Codex and Claude.ai that fix what AI builders leave behind: open Supabase tables, leaked keys, unsigned Stripe webhooks, client-only auth, broken deploys, slow queries, missing launch basics.

Built for apps made with **Lovable, Bolt, v0, Replit, Cursor and Claude Code** on Next.js / Vite + Supabase + Stripe + Vercel.

Home: [https://getshipready.github.io](https://getshipready.github.io)

### Guides (free, no signup)
- [Is my Lovable app's Supabase database exposed? A 10-minute self-check](https://getshipready.github.io/guides/lovable-supabase-self-check.html)
- ["RLS enabled" isn't a green light: test your Supabase app as a second user](https://getshipready.github.io/guides/rls-second-user-test.html)
- [Stripe webhook not verified in a Lovable or Bolt app: how to check and fix](https://getshipready.github.io/guides/stripe-webhook-not-verified.html)
- [Supabase anon key exposed in my frontend: is that a problem?](https://getshipready.github.io/guides/supabase-anon-key-exposed.html)
- [Supabase insert "works" but no row appears: the silent RLS failure (and the wrong fix)](https://getshipready.github.io/guides/supabase-insert-success-no-row.html)
- [Supabase view bypasses RLS? Fix it with security_invoker](https://getshipready.github.io/guides/supabase-view-bypasses-rls.html)
- [Login isn't access control: the second-account test for vibe-coded apps](https://getshipready.github.io/guides/login-is-not-access-control.html)
- [URL scan, two-account test or repo check: what each one can see in a vibe-coded app](https://getshipready.github.io/guides/url-scan-vs-two-account-test.html)

The skills walk your agent through a two-account test (can a second logged-in user read the first user's rows). The automated CI version of that test is in the Crew.

## Install in one line (Claude Code)
```bash
claude plugin install ship-ready-lite --marketplace getshipready/ship-ready-skills
```

That's it: all 53 skills + the router. Now open your app folder and run:
```bash
claude "Use ship-ready-start-here and check if this app is safe to launch"
```
Want a first answer in seconds? Run the free quick scan (8 day-one checks, offline, no network calls):
```bash
claude "Use ship-ready-quick-scan on this app"
# or, without an agent (Python 3, standard library only):
python3 skills/ship-ready-quick-scan/scripts/quickscan.py path/to/app
```
What the 8 checks look for:
1. **Leaked keys in your code**: Stripe keys, API keys or the Supabase `service_role` key committed to the repo.
2. **`.env` not ignored**: `.env` isn't in `.gitignore`, so it can end up on GitHub.
3. **Secrets in public env vars**: keys behind `NEXT_PUBLIC_`, `VITE_` or `EXPO_PUBLIC_` ship to every visitor's browser.
4. **Row Level Security off**: Supabase tables where RLS was never turned on, or a later migration turned it off.
5. **Read policies open to everyone**: `using (true)` policies let any visitor read every row.
6. **Views that skip RLS**: views without `security_invoker` run as their owner and ignore your policies.
7. **API routes with no caller check**: server routes that act without confirming who is calling.
8. **Stripe webhooks not verified**: handlers that don't check Stripe's signature accept fake "paid" events.

Each failed check names the free skill that fixes it. [See what it prints](skills/ship-ready-quick-scan/SKILL.md).

- Already inside a Claude Code session? Type `/plugin install ship-ready-lite --marketplace getshipready/ship-ready-skills`
- Claude Code older than 2.1.275: `claude plugin marketplace add getshipready/ship-ready-skills`, then `claude plugin install ship-ready-lite@ship-ready`

Only want one area? Install a category plugin instead:

| Plugin | Area | Skills | Install |
|---|---|---|---|
| `ship-ready-security` | Security | 8 | `/plugin install ship-ready-security --marketplace getshipready/ship-ready-skills` |
| `ship-ready-supabase` | Supabase & data | 9 | `/plugin install ship-ready-supabase --marketplace getshipready/ship-ready-skills` |
| `ship-ready-auth` | Auth | 6 | `/plugin install ship-ready-auth --marketplace getshipready/ship-ready-skills` |
| `ship-ready-payments` | Payments | 6 | `/plugin install ship-ready-payments --marketplace getshipready/ship-ready-skills` |
| `ship-ready-deploy` | Deploy & ops | 7 | `/plugin install ship-ready-deploy --marketplace getshipready/ship-ready-skills` |
| `ship-ready-performance` | Performance | 5 | `/plugin install ship-ready-performance --marketplace getshipready/ship-ready-skills` |
| `ship-ready-debugging` | Debugging & code health | 7 | `/plugin install ship-ready-debugging --marketplace getshipready/ship-ready-skills` |
| `ship-ready-launch` | Launch | 5 | `/plugin install ship-ready-launch --marketplace getshipready/ship-ready-skills` |

**Cursor:** copy `skills/*` into `.cursor/skills/` (Cursor also reads `.claude/skills/`).
**Claude.ai:** zip any skill folder and upload it under Settings → Capabilities → Skills.
**Codex / other agents:** copy into `.agents/skills/` and mention it in `AGENTS.md`.

## Catalogue
| Area | Skill | What it does |
|---|---|---|
| Security | [`secret-leak-check`](skills/secret-leak-check/SKILL.md) | Find API keys, service-role keys and tokens committed to an AI-built repo or shipped in the frontend bundle, and produce a rotation list |
| Security | [`leaked-key-rotation`](skills/leaked-key-rotation/SKILL.md) | Rotate leaked API keys fast without breaking production: triage every secret that sat in the leaked place, cap spend with no deploy, revoke and reissue at each provider (OpenAI, Anthropic, OpenRouter, Stripe, Supabase, GitHub), update host env vars, redeploy, prove the old key is dead and check usage and billing since the leak |
| Security | [`public-env-audit`](skills/public-env-audit/SKILL.md) | Audit NEXT_PUBLIC_, VITE_, EXPO_PUBLIC_ and REACT_APP_ variables to make sure no secret is compiled into the browser bundle |
| Security | [`xss-sanitize`](skills/xss-sanitize/SKILL.md) | Find and fix places where user-generated content is rendered as HTML (dangerouslySetInnerHTML, v-html, innerHTML, markdown with raw HTML) |
| Security | [`security-headers`](skills/security-headers/SKILL.md) | Add Content-Security-Policy, HSTS, frame-ancestors, nosniff and Referrer-Policy to a Next.js, Vite or static app on Vercel or Netlify without breaking Supabase, Stripe or analytics |
| Security | [`api-rate-limit`](skills/api-rate-limit/SKILL.md) | Protect login, signup, AI/LLM, email/SMS and other costly endpoints with per-user or per-IP rate limits and input caps so nobody can burn your credits or spam your users |
| Security | [`dependency-audit`](skills/dependency-audit/SKILL.md) | Find and fix vulnerable or abandoned npm packages in production dependencies without breaking the app, including Next.js security patches |
| Security | [`ssrf-url-fetch-guard`](skills/ssrf-url-fetch-guard/SKILL.md) | Secure features that fetch a user-supplied URL (link previews, import from URL, webhooks you call, AI browsing) against SSRF and internal network access |
| Supabase & data | [`rls-quick-check`](skills/rls-quick-check/SKILL.md) | Five-minute check of a Supabase project's Row Level Security: which tables have RLS off, which policies are 'using (true)', which updates lack WITH CHECK, and which buckets are public |
| Supabase & data | [`rls-policy-writer`](skills/rls-policy-writer/SKILL.md) | Write correct Supabase RLS policies for common access models: owner-only, public-read/owner-write, admin, team/multi-tenant, and server-only tables, with WITH CHECK, explicit Data API grants (required for new tables from Oct 30, 2026), indexes and a rollback |
| Supabase & data | [`mass-delete-guard`](skills/mass-delete-guard/SKILL.md) | Stop one user, bug or leaked key from wiping a Supabase/Postgres table, and recover fast if it already happened: incident steps, delete audit log, soft delete, owner-only delete policies and a delete rate limit |
| Supabase & data | [`storage-bucket-lockdown`](skills/storage-bucket-lockdown/SKILL.md) | Make Supabase Storage buckets private where needed, add per-user folder policies, and switch the app to signed URLs |
| Supabase & data | [`service-role-split`](skills/service-role-split/SKILL.md) | Remove the Supabase service_role key from browser code and split into a browser client (anon key + session) and a server-only admin client |
| Supabase & data | [`schema-to-migrations`](skills/schema-to-migrations/SKILL.md) | Turn a Supabase project built through Lovable, Bolt or the dashboard into versioned SQL migrations so changes are reviewable, reproducible and testable on a branch |
| Supabase & data | [`backups-and-restore`](skills/backups-and-restore/SKILL.md) | Make sure a Supabase/Postgres app can recover from deleted data or a bad migration: check the backup plan, add a logical export, and run a restore drill |
| Supabase & data | [`edge-function-auth`](skills/edge-function-auth/SKILL.md) | Make Supabase Edge Functions verify the caller's JWT, check roles, use secrets correctly and handle CORS, especially in Lovable/Bolt SPAs where Edge Functions are the only server code |
| Supabase & data | [`teams-multitenant-rls`](skills/teams-multitenant-rls/SKILL.md) | Add organizations or teams to a Supabase app with membership-based RLS, roles per team, invitations and safe switching between workspaces |
| Auth | [`protect-routes-nextjs`](skills/protect-routes-nextjs/SKILL.md) | Add real server-side protection to pages and API routes in a Next.js App Router app using @supabase/ssr middleware and getUser(), replacing client-only redirects |
| Auth | [`auth-redirect-urls`](skills/auth-redirect-urls/SKILL.md) | Fix Supabase/Clerk/Auth.js login, magic-link, OAuth and password-reset redirects that point at localhost or the wrong domain after deploying |
| Auth | [`oauth-callback-fix`](skills/oauth-callback-fix/SKILL.md) | Implement or repair the /auth/callback route that exchanges the code for a session with Supabase PKCE in Next.js, fixing 'auth session missing', loops and blank pages after Google/GitHub login |
| Auth | [`email-deliverability-smtp`](skills/email-deliverability-smtp/SKILL.md) | Move Supabase auth emails off the default rate-limited sender to custom SMTP (Resend, Postmark, SES) with SPF, DKIM and DMARC, and brand the templates |
| Auth | [`admin-role-setup`](skills/admin-role-setup/SKILL.md) | Implement admin/staff roles safely: role stored server-side, users unable to promote themselves, admin checks on the server and in RLS |
| Auth | [`session-bugs`](skills/session-bugs/SKILL.md) | Diagnose 'logged out randomly', 'user is null on first load', hydration mismatches and stale sessions in Supabase/Next.js or SPA apps with a structured checklist |
| Payments | [`stripe-webhook-verify`](skills/stripe-webhook-verify/SKILL.md) | Make a Stripe webhook endpoint verify signatures with the raw body, handle retries idempotently and return fast |
| Payments | [`stripe-checkout-server`](skills/stripe-checkout-server/SKILL.md) | Create Stripe Checkout sessions on the server with fixed Price IDs, the logged-in user's id and correct success/cancel URLs, never trusting prices or user ids from the browser |
| Payments | [`entitlements-table`](skills/entitlements-table/SKILL.md) | Model paid access with an entitlements/subscriptions table written only by the Stripe webhook and read by the app and RLS, replacing client-set is_pro flags |
| Payments | [`stripe-subscription-lifecycle`](skills/stripe-subscription-lifecycle/SKILL.md) | Handle the full subscription lifecycle: trials, upgrades/downgrades, failed payments, cancellations and the Stripe Customer Portal |
| Payments | [`stripe-go-live`](skills/stripe-go-live/SKILL.md) | Switch a Stripe integration from test to live mode safely: live keys, live webhook endpoint and secret, live Price IDs, tax, receipts and a real-card test |
| Payments | [`usage-credits-billing`](skills/usage-credits-billing/SKILL.md) | Implement prepaid credits or usage limits for AI features with an atomic ledger, so users can't overspend or race the counter |
| Deploy & ops | [`env-var-inventory`](skills/env-var-inventory/SKILL.md) | Build a complete inventory of environment variables across local, preview and production (Vercel, Netlify, Supabase secrets), fix missing ones and write .env.example |
| Deploy & ops | [`vercel-build-fix`](skills/vercel-build-fix/SKILL.md) | Diagnose and fix Vercel/Netlify build failures in AI-generated Next.js or Vite apps: type errors, ESLint, missing env vars, Node version, case-sensitive imports, lockfile mismatches |
| Deploy & ops | [`spa-hosting-rewrites`](skills/spa-hosting-rewrites/SKILL.md) | Fix 404s on refresh and deep links for Vite/React SPAs (Lovable, Bolt exports) on Vercel, Netlify, Cloudflare Pages or S3 by adding the right rewrites, plus caching headers |
| Deploy & ops | [`custom-domain-setup`](skills/custom-domain-setup/SKILL.md) | Connect a custom domain to Vercel/Netlify with correct DNS, HTTPS, www/apex redirect and update every place that stores the old URL (auth, Stripe, OAuth, emails) |
| Deploy & ops | [`preview-vs-prod`](skills/preview-vs-prod/SKILL.md) | Stop preview deployments from touching production data and money: separate Supabase projects or branches, Stripe test keys in preview, and protected previews |
| Deploy & ops | [`rollback-plan`](skills/rollback-plan/SKILL.md) | Write and rehearse how to undo a bad deploy or migration in minutes: instant rollback on the host, reversible migrations, feature flags |
| Deploy & ops | [`error-and-uptime-alerts`](skills/error-and-uptime-alerts/SKILL.md) | Add error tracking (Sentry), uptime monitoring and a health endpoint so you hear about outages before users tweet |
| Performance | [`n-plus-one-fix`](skills/n-plus-one-fix/SKILL.md) | Find and fix N+1 query patterns (a query inside a loop or per list item) in Supabase/Prisma apps using joins, embedded selects or batched IN queries |
| Performance | [`index-advisor`](skills/index-advisor/SKILL.md) | Find slow Postgres/Supabase queries and add the right indexes (foreign keys, RLS owner columns, sort columns) with EXPLAIN evidence |
| Performance | [`bundle-diet`](skills/bundle-diet/SKILL.md) | Shrink the JavaScript bundle of a Next.js or Vite app: find heavy dependencies (moment, lodash, icon packs, charts), lazy-load below-the-fold components and remove dead code |
| Performance | [`image-optimization`](skills/image-optimization/SKILL.md) | Fix slow images: next/image or responsive srcset, modern formats, correct sizes, lazy loading and priority for the hero, plus Supabase image transforms |
| Performance | [`lighthouse-triage`](skills/lighthouse-triage/SKILL.md) | Run Lighthouse or PageSpeed Insights on key pages and turn the report into a short prioritized fix list for LCP, INP and CLS |
| Debugging & code health | [`bug-repro-first`](skills/bug-repro-first/SKILL.md) | Turn a vague bug report ('it doesn't work') into exact reproduction steps, expected vs actual, logs and the smallest failing case before any code change |
| Debugging & code health | [`ai-loop-breaker`](skills/ai-loop-breaker/SKILL.md) | Get out of the loop where an AI builder keeps 'fixing' the same bug and breaking other things: freeze, diff, isolate, write a precise prompt with evidence, and checkpoint |
| Debugging & code health | [`agent-delete-guard`](skills/agent-delete-guard/SKILL.md) | Stop your own AI coding agent (Claude Code, Cursor, Codex) from deleting files, code or databases, and get things back when it already has: checkpoint before every session, deny rules, a read-only database role for the agent, and a recovery order |
| Debugging & code health | [`typescript-errors-fix`](skills/typescript-errors-fix/SKILL.md) | Fix accumulated TypeScript errors in AI-generated code without `any` spam or ts-ignore: generate Supabase types, fix nullability, and re-enable type checking in builds |
| Debugging & code health | [`add-regression-tests`](skills/add-regression-tests/SKILL.md) | Add a minimal, high-value test suite to a vibe-coded app: smoke E2E for signup/login/pay, API auth tests and RLS tests, running in CI |
| Debugging & code health | [`refactor-giant-component`](skills/refactor-giant-component/SKILL.md) | Safely split giant AI-generated components or route files into smaller pieces (data hooks, presentational components, utils) without changing behaviour |
| Debugging & code health | [`export-and-run-locally`](skills/export-and-run-locally/SKILL.md) | Export a Lovable, Bolt, v0 or Replit project to GitHub and run it locally with Cursor/Claude Code: env vars, Supabase connection, scripts, and a sanity build |
| Launch | [`seo-metadata`](skills/seo-metadata/SKILL.md) | Add titles, descriptions, Open Graph/Twitter images, sitemap.xml, robots.txt and canonical URLs to a Next.js or Vite app, and keep private app pages out of search |
| Launch | [`legal-pages-draft`](skills/legal-pages-draft/SKILL.md) | Draft a privacy policy, terms of service and cookie notice that match what the app actually collects and which processors it uses (Supabase, Stripe, analytics, AI APIs) |
| Launch | [`analytics-and-funnel`](skills/analytics-and-funnel/SKILL.md) | Set up privacy-friendly analytics and define 5–7 key events (visit, signup, activation, checkout start, paid) so you know where launch traffic drops |
| Launch | [`launch-post-drafts`](skills/launch-post-drafts/SKILL.md) | Draft launch posts for X, Reddit, Product Hunt, Hacker News and Indie Hackers that follow each community's rules: hook, concrete proof, honest limits, one CTA |
| Launch | [`transactional-email-setup`](skills/transactional-email-setup/SKILL.md) | Send product emails (welcome, receipts, notifications) from your own domain with Resend/Postmark, verified DNS, templates and unsubscribe handling |

## How every skill is written
When to use → numbered steps → copy-paste commands/code → output format → pitfalls → "done when" checklist → what only a human should do. Each skill asks your agent to show evidence (file:line, command output) and never echo secrets.

## Lite vs Crew vs Audit
| | **Lite** (this repo) | **Ship-Ready Crew** | **Agent-run audit** |
|---|---|---|---|
| Price | Free, MIT | $39 one-time | $129 per app |
| What | 53 single-task skills | 10 named agents: Harbor (lead) + Sentinel, Warden, Keymaster, Tally, Pilot, Torque, Medic, Beacon, Proof | We run the Crew on your repo; a human reviews the result |
| Scanner | free quick scan: 8 checks (10 of the 59 rules) | 59-check offline scanner (59 rules) with file:line evidence, CI exit code | included |
| Output | your agent's notes | Ship score /100, verdict, findings JSON/MD, Excel scorecard, fix plan, patches | PDF + Markdown report, fix plan + patches, one re-scan |
| Worked example | none | PromptPad: 0/100 → 99/100, 49 findings, full patch | your app |

→ Home: https://getshipready.github.io · Crew: https://getshipready.github.io/crew · Audit: https://getshipready.github.io/audit

## Is it safe to install?
Check before you trust any skills pack, this one included. Lite is 53 skills plus a router, each a folder of plain Markdown (`SKILL.md`) plus JSON plugin manifests. There is no npm package, no `postinstall` or setup script, no binaries and no network calls, so nothing runs when you install it; your agent only reads the instructions. Confirm it yourself: `find . -type f ! -name "*.md" ! -name "*.json"` lists only `LICENSE`, `.gitignore` and `skills/ship-ready-quick-scan/scripts/quickscan.py`, a standard-library Python script that runs only when you call it (no network calls). No file is executable. (Some skills show commands like `curl` for you to run on purpose; your agent asks before running anything.) Why it matters: on 22 Oct 2026 GitHub published critical malware advisories for npm packages of two popular skills collections ([GHSA-rgwm-3jj9-h563](https://github.com/advisories/GHSA-rgwm-3jj9-h563), [GHSA-9855-prwc-mfp2](https://github.com/advisories/GHSA-9855-prwc-mfp2)).

## Honest limits
These skills guide your agent; they don't replace a penetration test or legal advice. Keys, dashboards, production migrations and deploys stay in your hands.

Already ran a static code scanner? Good, keep it. It reads your code; the two-account test logs in as a second user and checks what that user can actually read. These skills walk your agent through that test; the Crew runs it in CI. Run both.

## License
MIT. Use them, fork them, ship them.
