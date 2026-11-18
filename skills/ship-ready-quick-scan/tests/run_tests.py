#!/usr/bin/env python3
"""Fixture tests for quickscan.py (stdlib only). Run: python3 tests/run_tests.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
QS = os.path.join(HERE, "..", "scripts", "quickscan.py")
# fixture: (expected verdict prefix, strings that must appear, strings that must NOT appear)
CASES = {
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
}
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
print(f"\n{len(CASES) - fails}/{len(CASES)} passed")
sys.exit(1 if fails else 0)
