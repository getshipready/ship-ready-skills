#!/usr/bin/env python3
"""Fixture tests for quickscan.py (stdlib only). Run: python3 tests/run_tests.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
QS = os.path.join(HERE, "..", "scripts", "quickscan.py")
# fixture: (expected verdict prefix, strings that must appear, strings that must NOT appear)
CASES = {
    "route-perhandler-bad": ("DO NOT SHIP", ["AUTH-002", "[FAIL] 7."], []),
    "route-perhandler-good": ("NO DAY-ONE BLOCKERS", ["[PASS] 7."], ["[FAIL]"]),
    "route-preamble-auth": ("NO DAY-ONE BLOCKERS", ["[PASS] 7."], ["[FAIL]"]),
    "secrets-py-toml-yml": ("DO NOT SHIP", ["SEC-001", "b.py", "config.toml", "ci.yml"], []),
    "secrets-lockfile-clean": ("NO DAY-ONE BLOCKERS", ["[PASS] 1."], ["[FAIL]"]),
    "key002-pgnet-bearer-vault": ("NO DAY-ONE BLOCKERS", ["KEY-002", "switch to an sb_secret_ key", "001_hook.sql:8"], ["[FAIL]"]),
    "key002-pgnet-bearer-secret": ("NO DAY-ONE BLOCKERS", ["KEY-002", "switch to an sb_secret_ key"], ["[FAIL]"]),
    "key002-pgnet-apikey-header": ("NO DAY-ONE BLOCKERS", [], ["KEY-002", "[FAIL]"]),
    "e257-fail-headline": ("1 CHECK FAILED", ["[FAIL] 10.", "RLS-011", "1 failed, all rated below high"], ["NO DAY-ONE BLOCKERS", "0 critical, 0 high"]),
    "e257-public-revoked": ("NO DAY-ONE BLOCKERS", ["[PASS] 10."], ["[FAIL]"]),
    "key002-bad": ("FIX BEFORE LAUNCH", ["SEC-001", "Resend API key"], []),
    "key002-good": ("NO DAY-ONE BLOCKERS", [], ["[FAIL]"]),
    "key002-newkeys": ("DO NOT SHIP", ["SEC-001", "sb_secret_", "GitHub fine-grained token", "Groq API key"], []),
    "key002-goodnew": ("NO DAY-ONE BLOCKERS", [], ["[FAIL]"]),
    "auth010-f1-open-ai-fn":        ("FIX BEFORE LAUNCH", ["AUTH-010", "[FAIL] 7."], ["Pause AI"]),
    "auth010-f2-stripe-webhook":    ("NO DAY-ONE BLOCKERS", ["[PASS] 7."], []),
    "auth010-f3-checked-fn":        ("NO DAY-ONE BLOCKERS", ["[PASS] 7."], []),
    "auth010-f4-no-config":         ("NO DAY-ONE BLOCKERS", [], ["AUTH-010 ", "[FAIL]"]),
    "auth010-f5-lovable-ai":        ("FIX BEFORE LAUNCH", ["[FAIL] 7.", "Pause AI"], []),
    "key001-f1-vite-anon-var":      ("NO DAY-ONE BLOCKERS", ["KEY-001", "VITE_SUPABASE_ANON_KEY"], []),
    "key001-f2-hardcoded-anon-jwt": ("NO DAY-ONE BLOCKERS", ["KEY-001", "legacy `anon` key"], []),
    "key001-f3-migrated":           ("NO DAY-ONE BLOCKERS", [], ["KEY-001, not scored"]),
    "key001-f4-half-migrated-server": ("NO DAY-ONE BLOCKERS", ["KEY-001", "SUPABASE_SERVICE_ROLE_KEY"], []),
    "auth010-f6-withsupabase-user":   ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "auth010-f7-withsupabase-secret": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "auth010-f8-withsupabase-none":   ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "auth: 'none'"], ["[FAIL]", "anyone can call it"]),
    "auth010-f9-plain-deno":          ("FIX BEFORE LAUNCH", ["AUTH-010", "[FAIL] 7.", "anyone can call it"], ["withSupabase"]),
    "auth010-f10-withsupabase-named": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "auth010-f11-withsupabase-publishable": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "publishable", "rate limit"], ["[FAIL]"]),
    "auth010-f12-withsupabase-array": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "auth010-f13-withsupabase-wildcard": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "auth010-f14-withsupabase-publishable-named": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "publishable", "rate limit"], ["[FAIL]"]),
    "auth010-f15-withsupabase-array-named": ("NO DAY-ONE BLOCKERS", ["[PASS] 7.", "withSupabase"], ["[FAIL]"]),
    "rls002-to-1": ("DO NOT SHIP", ["RLS-002", "[FAIL] 5."], []),
    "rls002-to-2": ("DO NOT SHIP", ["RLS-002", "[FAIL] 5."], []),
    "rls002-to-3": ("DO NOT SHIP", ["RLS-002", "[FAIL] 5."], []),
    "rls002-to-4": ("NO DAY-ONE BLOCKERS", ["[PASS] 5."], ["[FAIL]"]),
    "auth012-f1-clerk-uid": ("NO DAY-ONE BLOCKERS", ["AUTH-012", "(clerk)", "auth.jwt()->>'sub'"], ["[FAIL]"]),
    "auth012-f2-clerk-sub": ("NO DAY-ONE BLOCKERS", [], ["AUTH-012"]),
    "auth012-f3-disabled": ("NO DAY-ONE BLOCKERS", [], ["AUTH-012"]),
    "auth012-f4-no-thirdparty": ("NO DAY-ONE BLOCKERS", [], ["AUTH-012"]),
    "auth012-f5-auth0-then-section": ("NO DAY-ONE BLOCKERS", ["AUTH-012", "(auth0)"], ["[FAIL]"]),
    "auth012-f6-cognito": ("NO DAY-ONE BLOCKERS", [], ["AUTH-012"]),
    "sql001-f1": ("DO NOT SHIP", ["SQL-001", "[FAIL] 9.", "exec_sql"], []),
    "sql001-f2": ("NO DAY-ONE BLOCKERS", ["[PASS] 9."], ["SQL-001 "]),
    "sql001-f3": ("FIX BEFORE LAUNCH", ["SQL-001", "[FAIL] 9."], []),
    "sql001-f4": ("NO DAY-ONE BLOCKERS", ["[PASS] 9."], ["[FAIL]"]),
    "sql001-f5": ("FIX BEFORE LAUNCH", ["SQL-001", "[FAIL] 9."], []),
    "sql001-f6": ("NO DAY-ONE BLOCKERS", ["[PASS] 9."], ["[FAIL]"]),
    "sql001-f7": ("DO NOT SHIP", ["SQL-001", "[FAIL] 9."], []),
    "sql001-f8": ("DO NOT SHIP", ["SQL-001", "[FAIL] 9."], []),
    "sql001-f9": ("NO DAY-ONE BLOCKERS", ["[PASS] 9."], ["SQL-001 "]),
    "rls011-f1": ("FIX BEFORE LAUNCH", ["RLS-011", "[FAIL] 10.", "dash_push"], []),
    "rls011-f2": ("FIX BEFORE LAUNCH", ["RLS-011", "[FAIL] 10.", "EXECUTE not revoked from public"], []),
    "rls011-f3": ("NO DAY-ONE BLOCKERS", ["[PASS] 10."], ["RLS-011 ", "[FAIL]"]),
    "rls011-f4": ("NO DAY-ONE BLOCKERS", ["[PASS] 10."], ["[FAIL]"]),
    "rls011-f5": ("NO DAY-ONE BLOCKERS", ["[PASS] 10."], ["[FAIL]"]),
    "rls011-f6": ("NO DAY-ONE BLOCKERS", ["[PASS] 10."], ["[FAIL]"]),
    "rls011-f7": ("1 CHECK FAILED", ["RLS-011", "[FAIL] 10.", "MEDIUM"], []),
    "rls011-f8": ("DO NOT SHIP", ["SQL-001", "[FAIL] 9.", "[PASS] 10."], ["`exec_sql()` is security definer (runs as the owner, RLS skipped)"]),
    "rls011-f9": ("FIX BEFORE LAUNCH", ["RLS-011", "[FAIL] 10.", "granted to anon/public"], []),
    "rls011-f10": ("FIX BEFORE LAUNCH", ["RLS-011", "[FAIL] 10.", "EXECUTE not revoked from public"], []),
    "rls014-f1": ("FIX BEFORE LAUNCH", ["RLS-014", "[FAIL] 11.", "anon, authenticated"], []),
    "rls014-f2": ("1 CHECK FAILED", ["RLS-014", "[FAIL] 11.", "MEDIUM"], []),
    "rls014-f3": ("NO DAY-ONE BLOCKERS", ["[PASS] 11."], ["RLS-014 ", "[FAIL]"]),
    "rls014-f4": ("NO DAY-ONE BLOCKERS", ["[PASS] 11."], ["[FAIL]"]),
    "rls014-f5": ("NO DAY-ONE BLOCKERS", ["[PASS] 11."], ["[FAIL]"]),
    "rls014-f6": ("FIX BEFORE LAUNCH", ["RLS-014", "[FAIL] 11.", "Bulk grant"], []),
    "rls014-f7": ("NO DAY-ONE BLOCKERS", ["[PASS] 11."], ["[FAIL]"]),
    "rls014-f8": ("FIX BEFORE LAUNCH", ["RLS-014", "[FAIL] 11."], []),
    "rls014-f9": ("NO DAY-ONE BLOCKERS", ["[PASS] 11."], ["[FAIL]"]),
    "usermeta-f1": ("DO NOT SHIP", ["AUTH-013", "[FAIL] 12.", "admins read all"], []),
    "usermeta-f2": ("FIX BEFORE LAUNCH", ["AUTH-013", "[FAIL] 12.", "HIGH"], []),
    "usermeta-f3": ("NO DAY-ONE BLOCKERS", ["[PASS] 12."], ["AUTH-013 ", "[FAIL]"]),
    "usermeta-f4": ("NO DAY-ONE BLOCKERS", ["[PASS] 12."], ["[FAIL]"]),
    "usermeta-f5": ("DO NOT SHIP", ["AUTH-013", "[FAIL] 12."], []),
    "usermeta-f6": ("FIX BEFORE LAUNCH", ["AUTH-013", "[FAIL] 12."], []),
    "usermeta-f7": ("DO NOT SHIP", ["AUTH-013", "[FAIL] 12."], []),
    "usermeta-f8": ("NO DAY-ONE BLOCKERS", ["[PASS] 12."], ["[FAIL]"]),
    "e234-f1-commented-enable": ("DO NOT SHIP", ["RLS-001", "[FAIL] 4."], []),
    "e234-f2-unquoted-policy": ("DO NOT SHIP", ["RLS-002", "[FAIL] 5."], []),
    "e234-f3-quoted-schema": ("DO NOT SHIP", ["RLS-001", "[FAIL] 4."], []),
    "e234-f4-jwt-wrapper": ("DO NOT SHIP", ["AUTH-013", "[FAIL] 12."], []),
    "e234-f5-rls-reenabled": ("NO DAY-ONE BLOCKERS", [], ["[FAIL]"]),
    "e234-f6-sk-in-identifier": ("NO DAY-ONE BLOCKERS", [], ["[FAIL]", "OpenAI/Anthropic"]),
}
# key002-newkeys holds fake keys in real formats. It is written at test time so GitHub
# push protection doesn't treat the fixture as a leaked secret.
_nk = os.path.join(HERE, "fixtures", "key002-newkeys", "src")
os.makedirs(_nk, exist_ok=True)
with open(os.path.join(_nk, "admin.ts"), "w") as _f:
    _f.write('const admin = createClient(url, "' + "sb_" + "secret_" + "FAKEfake0000Test1111xyz_TEST" + '");\n')
    _f.write('const gh = "' + "github" + "_pat_" + "11FAKE0000TEST" + "x" * 30 + "_" + "y" * 40 + '";\n')
    _f.write('const groq = "' + "gsk" + "_" + "FakeTestKey0" * 4 + '";\n')
fails = 0
for name, (verdict, must, mustnot) in CASES.items():
    out = subprocess.run([sys.executable, QS, os.path.join(HERE, "fixtures", name)], capture_output=True, text=True).stdout
    res = next((l for l in out.splitlines() if l.startswith("Result: ")), "")
    errs = []
    if not res.startswith("Result: " + verdict):
        errs.append(f"verdict: {res!r}")
    errs += [f"missing {s!r}" for s in must if s not in out]
    errs += [f"unexpected {s!r}" for s in mustnot if s in out]
    print(("ok   " if not errs else "FAIL ") + name + ("" if not errs else "  " + "; ".join(errs)))
    fails += bool(errs)
import tempfile
FX = lambda n: os.path.join(HERE, "fixtures", n)
def run(*a): return subprocess.run([sys.executable, QS, *a], capture_output=True, text=True)
with tempfile.TemporaryDirectory() as empty:
    EXIT = [  # (name, args, expected exit code, text that must appear)
        ("exit-default-critical-is-0", [FX("sql001-f1")], 0, "DO NOT SHIP"),
        ("exit-fail-on-critical-critical", [FX("sql001-f1"), "--fail-on=critical"], 1, "DO NOT SHIP"),
        ("exit-fail-on-critical-high-only", [FX("rls011-f1"), "--fail-on=critical"], 0, "FIX BEFORE LAUNCH"),
        ("exit-fail-on-high-high", [FX("rls011-f1"), "--fail-on=high"], 1, "FIX BEFORE LAUNCH"),
        ("exit-fail-on-high-clean", [FX("rls011-f3"), "--fail-on=high"], 0, "NO DAY-ONE BLOCKERS"),
        ("exit-fail-on-bad-value", [FX("rls011-f3"), "--fail-on=low"], 1, "Usage"),
        ("empty-folder", [empty, "--fail-on=high"], 0, "no Supabase or app files were found"),
    ]
    for name, a, code, text in EXIT:
        r = run(*a); out = r.stdout + r.stderr
        errs = ([f"exit {r.returncode} != {code}"] if r.returncode != code else []) + ([f"missing {text!r}"] if text not in out else [])
        if name == "empty-folder" and "NO DAY-ONE BLOCKERS" in out: errs.append("empty folder reported no blockers")
        print(("ok   " if not errs else "FAIL ") + name + ("" if not errs else "  " + "; ".join(errs)))
        fails += bool(errs)

# SEC-003 / Mapbox fixtures: written to a temp dir at test time. Token-shaped values are
# assembled here so no secret-looking literal is committed (GitHub push protection).
def _pubenv_cases():
    tok = "sk." + "eyJ" + "1IjoiZXhhbXBsZSIsImEiOiJ0ZXN0In0" + ".AbCdEfGhIjKlMnOpQrStUv"
    fx = {
        "a": {".env": "VITE_SUPABASE_URL=https://x.supabase.co\nVITE_RESEND_API_KEY=placeholder\nVITE_STRIPE_KEY=placeholder\nVITE_GEMINI_API_KEY=placeholder\nVITE_OPENAI_API_KEY=placeholder\nNEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_placeholder\n"},
        "b": {".env": "EXPO_PUBLIC_OPENAI_API_KEY=placeholder\nEXPO_PUBLIC_REVENUECAT_SECRET=placeholder\nREACT_APP_SENDGRID_API_KEY=placeholder\nNEXT_PUBLIC_GROQ_API_KEY=placeholder\n"},
        "c": {".env": "NEXT_PUBLIC_MAPBOX_TOKEN=" + tok + "\n", ".gitignore": "node_modules\n"},
        "safe": {".env": "VITE_STRIPE_PUBLISHABLE_KEY=pk_test_x\nNEXT_PUBLIC_STRIPE_PRICE_ID=price_x\nVITE_SUPABASE_ANON_KEY=x\nVITE_SUPABASE_PUBLISHABLE_KEY=x\nNEXT_PUBLIC_STRIPE_PAYMENT_LINK=https://buy.stripe.com/x\nVITE_SUPABASE_URL=https://x.supabase.co\n"},
        "safe2": {".env": "NEXT_PUBLIC_MAPBOX_TOKEN=pk.placeholder\nNEXT_PUBLIC_POSTHOG_KEY=phc_placeholder\nNEXT_PUBLIC_SENTRY_DSN=https://x@o1.ingest.sentry.io/1\nVITE_TURNSTILE_SITE_KEY=0x4AAA\nEXPO_PUBLIC_SUPABASE_ANON_KEY=x\n"},
    }
    return fx, [
        ("pubenv-a-providers", "a", "DO NOT SHIP", ["SEC-003", "VITE_RESEND_API_KEY", "VITE_STRIPE_KEY", "VITE_GEMINI_API_KEY", "VITE_OPENAI_API_KEY"], ["VITE_SUPABASE_URL ", "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY"]),
        ("pubenv-b-providers", "b", "DO NOT SHIP", ["SEC-003", "EXPO_PUBLIC_OPENAI_API_KEY", "EXPO_PUBLIC_REVENUECAT_SECRET", "REACT_APP_SENDGRID_API_KEY", "NEXT_PUBLIC_GROQ_API_KEY"], []),
        ("pubenv-c-mapbox-secret", "c", "FIX BEFORE LAUNCH", ["SEC-001", "Mapbox secret token"], ["Secrets behind a public env prefix (NEXT_PUBLIC_, VITE_, EXPO_PUBLIC_)  (SEC-003)\n1."]),
        ("pubenv-safe", "safe", "1 CHECK FAILED", ["[PASS] 3."], ["exposed to the browser"]),
        ("pubenv-safe2", "safe2", "1 CHECK FAILED", ["[PASS] 3."], ["exposed to the browser", "Mapbox secret token"]),
    ]
_files, _pcases = _pubenv_cases()
with tempfile.TemporaryDirectory() as _root:
    for _d, _fs in _files.items():
        os.makedirs(os.path.join(_root, _d))
        for _n, _c in _fs.items():
            open(os.path.join(_root, _d, _n), "w").write(_c)
    for name, d, verdict, must, mustnot in _pcases:
        r = run(os.path.join(_root, d)); out = r.stdout + r.stderr
        res = next((l for l in out.splitlines() if l.startswith("Result: ")), "")
        errs = ([] if res.startswith("Result: " + verdict) else [f"verdict: {res!r}"])
        errs += [f"missing {x!r}" for x in must if x not in out] + [f"unexpected {x!r}" for x in mustnot if x in out]
        print(("ok   " if not errs else "FAIL ") + name + ("" if not errs else "  " + "; ".join(errs)))
        fails += bool(errs)
# RLS-004 (own-row update policy on a table with role/plan/credits): fixtures are written at test time
_T = "create table public.profiles (id uuid primary key references auth.users(id), display_name text, {extra});\nalter table public.profiles enable row level security;\n"
_P = 'create policy "own row" on public.profiles for update using (auth.uid() = id);\n'
_R4 = {
    "bad": _T.format(extra="role text default 'user'") + _P,
    "bad-plan-all": _T.format(extra="plan text, credits int") + 'create policy "own" on public.profiles for all using (auth.uid() = id);\n',
    "good-grant": _T.format(extra="role text default 'user'") + _P + "revoke update on table public.profiles from anon, authenticated;\ngrant update (display_name) on table public.profiles to authenticated;\n",
    "good-nopriv": _T.format(extra="bio text") + _P,
}
with tempfile.TemporaryDirectory() as _r4:
    for _n, _sql in _R4.items():
        os.makedirs(os.path.join(_r4, _n, "supabase", "migrations"))
        open(os.path.join(_r4, _n, "supabase", "migrations", "001.sql"), "w").write(_sql)
    for name, d, bad in [("rls004-bad-role", "bad", True), ("rls004-bad-plan-all", "bad-plan-all", True), ("rls004-good-column-grant", "good-grant", False), ("rls004-good-no-priv-column", "good-nopriv", False)]:
        out = run(os.path.join(_r4, d)).stdout
        errs = []
        if bad and not ("RLS-004" in out and "[FAIL] 13." in out and "CRITICAL" in out): errs.append("RLS-004 critical not reported")
        if not bad and ("RLS-004 " in out or "[FAIL] 13." in out or "[PASS] 13." not in out): errs.append("unexpected RLS-004 result")
        print(("ok   " if not errs else "FAIL ") + name + ("" if not errs else "  " + "; ".join(errs)))
        fails += bool(errs)
    out = run(os.path.join(_r4, "bad")).stdout
    errs = [x for x in ["self-promotion to admin/Pro"] if x in out] + (["not 44"] if "44 more checks" not in out else [])
    print(("ok   " if not errs else "FAIL ") + "rls004-promo-text-44-more" + ("" if not errs else "  " + "; ".join(errs)))
    fails += bool(errs)
# --no-promo / SHIPREADY_NO_PROMO
PROMO = [("promo-default-shows-crew", [], {}, True), ("promo-flag-hides", ["--no-promo"], {}, False),
         ("promo-env-hides", [], {"SHIPREADY_NO_PROMO": "1"}, False), ("promo-env-zero-shows", [], {"SHIPREADY_NO_PROMO": "0"}, True),
         ("promo-flag-with-fail-on", ["--no-promo", "--fail-on=critical"], {}, False)]
for name, extra, env, shows in PROMO:
    r = subprocess.run([sys.executable, QS, FX("sql001-f1"), *extra], capture_output=True, text=True, env={**os.environ, "SHIPREADY_NO_PROMO": "", **env})
    out = r.stdout; has = "Get the Crew" in out or "$39" in out
    errs = []
    if has != shows: errs.append(f"promo present={has}, expected {shows}")
    if "Result: " not in out or "Static heuristics" not in out: errs.append("scan output incomplete")
    if not shows and "Full rule list: https://github.com/getshipready/ship-ready-skills" not in out: errs.append("neutral line missing")
    print(("ok   " if not errs else "FAIL ") + name + ("" if not errs else "  " + "; ".join(errs)))
    fails += bool(errs)
# writes nothing: no __pycache__/.pyc after a run from a clean copy
import shutil, tempfile
_tmp = tempfile.mkdtemp()
_sc = os.path.join(_tmp, "scripts"); shutil.copytree(os.path.join(HERE, "..", "scripts"), _sc, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
subprocess.run([sys.executable, os.path.join(_sc, "quickscan.py"), FX("key002-good"), "--no-promo"], capture_output=True, text=True, env={k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"})
_pyc = [os.path.join(d, f) for d, _, fs in os.walk(_tmp) for f in fs if f.endswith(".pyc")]
print(("ok   " if not _pyc else "FAIL ") + "writes-no-bytecode" + ("" if not _pyc else "  " + ", ".join(_pyc)))
fails += bool(_pyc)
shutil.rmtree(_tmp, ignore_errors=True)
PUBENV_N = 5
total = len(CASES) + len(EXIT) + PUBENV_N + len(PROMO) + 5 + 1  # +5 RLS-004 checks, +1 bytecode
print(f"\n{total - fails}/{total} passed")
sys.exit(1 if fails else 0)
