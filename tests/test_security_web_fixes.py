"""Regression tests for web findings (0sec-labs deep review)."""
from pathlib import Path
import re
import pytest

REPO = Path(__file__).resolve().parent.parent
MW = REPO / "cloudflare" / "functions" / "_middleware.js"
REPORT = REPO / "scripts" / "agency_report.py"


# --- CRITICAL A: no hardcoded AgentMail key ---
def test_middleware_no_hardcoded_key():
    src = MW.read_text()
    assert "am_us_" not in src, "hardcoded AgentMail key still present"
    assert "env.AGENTMAIL_API_KEY ||" not in src
    assert "env.AGENTMAIL_API_KEY" in src          # env reference kept
    assert "Internal error" in src                 # generic 500 path


# --- HIGH B: SSRF — whitelist + search sanitization (mirror of JS regex) ---
ALLOWED_PREFIXES = ['/tools', '/blog', '/success', '/api/report/', '/api/contact', '/api/login']
SEARCH_RE = re.compile(r'^[A-Za-z0-9=&?._~\-/]*$')

def safe_worker_url(pathname, search):
    if pathname == '/':
        return 'https://worker/'
    if not SEARCH_RE.match(search):
        return None
    if '..' in pathname or '//' in pathname:
        return None
    for p in ALLOWED_PREFIXES:
        if pathname.startswith(p):
            return f"https://worker{pathname}{search}"
    return None

@pytest.mark.parametrize("path,search,ok", [
    ("/tools?x=1", "", True), ("/blog?page=2", "", True),
    ("/../admin", "", False), ("/api/report//evil", "", False),
    ("/internal/debug", "", False), ("/tools/x", "", True),
])
def test_worker_url_traversal(path, search, ok):
    assert bool(safe_worker_url(path, search)) is ok

def test_middleware_search_regex_rejects_bad_chars():
    src = MW.read_text()
    js_re = re.search(r"SEARCH_RE = /(.*?)/;", src).group(1)
    assert js_re == r"^[A-Za-z0-9=&?._~\/-]*$"


# --- CRITICAL C: SQL/Command injection in agency_report.py ---
def test_agency_report_sql_whitelist_rejects_payload():
    ns = {}
    exec(compile(REPORT.read_text(), 'report', 'exec'), ns)
    with pytest.raises(ValueError):
        ns["query_umami"]("SELECT 1; DROP TABLE session")
    assert "SELECT COUNT(*)::text FROM session" in ns["_SQL_WHITELIST"]

def test_agency_report_no_shell_true():
    src = REPORT.read_text()
    assert "shell=True" not in src
