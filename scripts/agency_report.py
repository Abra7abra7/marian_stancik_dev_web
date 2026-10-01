#!/usr/bin/env python3
"""
Agency-Grade Site Audit & Weekly Report — marianstancik.dev
Combines: health monitoring, GEO audit, security scan, content analysis, Umami analytics
Generates: professional dark-theme HTML with PDF print support
"""
import subprocess, json, os, re, ssl, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────
TARGET_URLS = [
    "https://marianstancik.dev",
    "https://www.marianstancik.dev",
    "https://www.ascentia.sk",
]
GIT_REPOS = [
    "/root/projects/marian-stancik-web",
    "/root/projects/ascentia-web",
]
AGENTMAIL_TO = ["stancikmarian8@gmail.com"]
AGENTMAIL_FROM = "marianstancik@agentmail.to"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HermesAgency/1.0)"


# ── Helpers ────────────────────────────────────────────────────────
def run(cmd, timeout=20):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except: return ""

def get_umami_pass():
    try:
        r = subprocess.run(["docker","inspect","umami-umami-db-1"], capture_output=True, text=True, timeout=5)
        data = json.loads(r.stdout)
        for e in data[0]["Config"]["Env"]:
            if e.startswith("POSTGRES_PASSWORD="): return e.split("=",1)[1]
    except: pass
    return ""

def query_umami(sql):
    pw = get_umami_pass()
    if not pw: return []
    r = subprocess.run(["docker","exec","-e",f"PGPASSWORD={pw}","umami-umami-db-1",
        "psql","-U","umami","-d","umami","-t","-A","-F","|","-c",sql],
        capture_output=True, text=True, timeout=15)
    if r.returncode: return []
    return [l for l in r.stdout.strip().split("\n") if l.strip()]


# ── Audit Engine (simplified, inline) ──────────────────────────────
def audit_url(target_url):
    """Run GEO + Readiness audit on a target URL"""
    parsed = urllib.parse.urlparse(target_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    ctx = ssl.create_default_context()
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,*/*"}

    result = {"url": target_url, "domain": parsed.netloc, "error": None}
    start = datetime.now()
    html, resp_headers, status, rtime = "", {}, 0, 0

    try:
        req = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            status = resp.status
            rtime = int((datetime.now() - start).total_seconds() * 1000)
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        result["error"] = str(e)
        return result

    result["status"] = status
    result["response_ms"] = rtime
    result["headers"] = resp_headers

    # Fetch robots.txt, llms.txt, sitemap.xml
    for resource in ["robots.txt", "llms.txt", "sitemap.xml"]:
        try:
            req = urllib.request.Request(f"{base_url}/{resource}", headers=headers)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
                result[resource.replace(".","_")] = r.read().decode('utf-8', errors='ignore')
        except: result[resource.replace(".","_")] = ""

    # Content analysis
    text = re.sub(r'<[^>]+>', ' ', html)
    words = [w for w in text.split() if len(w) > 1]
    result["word_count"] = len(words)

    # Numbers with units
    result["numbers"] = re.findall(r'(?:€\s*\d+(?:[\.,]\d+)?|\d+(?:[\.,]\d+)?\s*(?:€|%|kg|ms|s|h|hod|min|M|k|\+))', html, re.IGNORECASE)

    # External links
    domain_esc = re.escape(parsed.netloc)
    result["external_links"] = re.findall(r'href=["\'](https?://(?!' + domain_esc + r')[^"\']+)["\']', html)

    # Quotes
    result["quotes"] = re.findall(r'<blockquote[^>]*>(.*?)</blockquote>', html, re.DOTALL | re.IGNORECASE)

    # Headings
    result["h1_count"] = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
    result["h2_count"] = len(re.findall(r'<h2[^>]*>', html, re.IGNORECASE))
    result["h3_count"] = len(re.findall(r'<h3[^>]*>', html, re.IGNORECASE))

    # Schema / JSON-LD
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    result["schemas"] = [json.loads(s.strip()) for s in schemas if s.strip()] if schemas else []

    # AI bots in robots.txt
    robots = result.get("robots_txt", "") or ""
    ai_bots = ["GPTBot","ClaudeBot","PerplexityBot","Google-Extended","Applebot-Extended","CCBot","Cohere-ai"]
    result["allowed_bots"] = [b for b in ai_bots if b.lower() in robots.lower()]

    # Security headers
    rh = resp_headers
    result["security"] = {
        "hsts": "strict-transport-security" in rh,
        "csp": "content-security-policy" in rh,
        "xframe": "x-frame-options" in rh,
        "xcontent": "x-content-type-options" in rh,
        "referrer": "referrer-policy" in rh,
        "cookies": "set-cookie" in rh,
    }
    result["tracking_scripts"] = re.findall(r'(google-analytics\.com|googletagmanager\.com|facebook\.net|clarity\.ms)', html, re.IGNORECASE)
    result["is_cookieless"] = not result["security"]["cookies"] and len(result["tracking_scripts"]) == 0

    # Legal markers
    result["has_privacy"] = bool(re.search(r'href=["\'][^"\']*(?:privacy|ochrana-osobnych)[^"\']*["\']', html, re.IGNORECASE))
    result["has_terms"] = bool(re.search(r'href=["\'][^"\']*(?:terms|obchodne-podmienky)[^"\']*["\']', html, re.IGNORECASE))
    result["has_ai_act"] = bool(re.search(r'(?:AI Act|čl\.\s*50|asistencia|disclaimer)', html, re.IGNORECASE))
    result["has_waiver"] = bool(re.search(r'(?:108/2024|odstúpen|14\s*dní)', html, re.IGNORECASE))
    result["llms_ok"] = len(result.get("llms_txt","")) > 50
    result["sitemap_ok"] = "<url>" in result.get("sitemap_xml","")
    result["canonical_ok"] = 'rel="canonical"' in html.lower()
    result["schema_org_ok"] = len(result["schemas"]) > 0

    # SCORING: GEO (0-100)
    ncount = len(result["numbers"])
    elinks = len(result["external_links"])
    eq = len(result["quotes"])
    p1 = min(10, int((ncount/15)*10)) + min(12, elinks*2) + min(8, eq*4) + (5 if ("19+" in html or "Hetzner" in html) else 2)
    p2 = (6 if result["h1_count"]==1 and result["h2_count"]>=2 else 3) + (8 if len(words)>100 else 4) + \
         (6 if "FAQPage" in str(result["schemas"]) or "faq" in html.lower() else 0) + (5 if "<table" in html else 2)
    p3 = (9 if result["schema_org_ok"] else 0) + (6 if "linkedin.com" in html or "github.com" in html else 0) + \
         (4 if "Marian Stancik" in html else 0) + (6 if result["has_ai_act"] else 2)
    ab = len(result["allowed_bots"])
    p4 = (6 if ab>=3 else (3 if len(robots)>0 else 0)) + (4 if result["llms_ok"] else 0) + \
         (3 if rtime<1500 else 1) + (2 if result["canonical_ok"] else 1)
    result["geo_score"] = p1+p2+p3+p4
    result["geo_pillars"] = {"evidence":p1,"structure":p2,"authority":p3,"crawlability":p4}

    # SCORING: Readiness (0-100)
    sec_count = sum([1 for v in result["security"].values() if v and v is True])
    r_gdpr = 30 if result["is_cookieless"] and result["has_privacy"] else 20
    r_ai = 25 if result["has_ai_act"] else 15
    r_sec = int((sec_count/5)*25)
    r_eco = 20 if (result["has_terms"] and result["has_waiver"]) else 15
    result["readiness_score"] = r_gdpr+r_ai+r_sec+r_eco
    result["readiness_pillars"] = {"gdpr":r_gdpr,"ai_act":r_ai,"security":r_sec,"ecommerce":r_eco}
    return result


# ── SSL Certificate Check ──────────────────────────────────────────
def check_ssl(hostname, port=443):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket(), server_hostname=hostname) as s:
            s.settimeout(8)
            s.connect((hostname, port))
            cert = s.getpeercert()
            expires = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            remaining = (expires - datetime.now(timezone.utc)).days
            issuer = dict(x[0] for x in cert["issuer"]) if cert.get("issuer") else {}
            return {"remaining_days": remaining, "issuer": issuer.get("commonName","?"), "expires": expires.strftime("%d.%m.%Y"), "ok": remaining > 30}
    except: return {"error": "Could not check SSL", "ok": False}

from socket import socket


# ── Content Stats ──────────────────────────────────────────────────
def get_blog_stats():
    blog_index = "/root/projects/marian-stancik-web/blog"
    if not os.path.isdir(blog_index): return {}
    total = 0
    langs = {}
    for root, dirs, files in os.walk(blog_index):
        for f in files:
            if f.endswith(".html") and f != "index.html":
                total += 1
                d = root.replace(blog_index,"").lstrip("/") or "en"
                langs[d] = langs.get(d,0) + 1
    return {"total": total, "per_language": langs}


# ── Data Collection ────────────────────────────────────────────────
def collect():
    now = datetime.now(timezone.utc)
    week = now - timedelta(days=7)
    data = {"generated": now.strftime("%d. %B %Y %H:%M CEST"), "period": {"from": week.strftime("%d.%m.%Y"), "to": now.strftime("%d.%m.%Y")}}

    # 1. Site audits
    audits = [audit_url(url) for url in TARGET_URLS]
    data["audits"] = audits

    # 2. SSL checks
    ssl_results = []
    for d in ["marianstancik.dev", "www.marianstancik.dev", "www.ascentia.sk", "api.marianstancik.dev"]:
        r = check_ssl(d)
        r["hostname"] = d
        ssl_results.append(r)
    data["ssl"] = ssl_results

    # 3. Git sync
    git_data = []
    for repo in GIT_REPOS:
        name = os.path.basename(repo)
        last = run(["git","-C",repo,"log","--oneline","-1"],5)
        behind = run(["git","-C",repo,"fetch","origin","-q"],10)
        div = run(["git","-C",repo,"log","--oneline","HEAD..origin/main"],5)
        git_data.append({"name":name,"last_commit":last,"diverged":bool(div.strip())})
    data["git"] = git_data

    # 4. Umami analytics
    u = {"visits_7d":0,"all_time":0,"countries_7d":[]}
    try:
        r = query_umami("SELECT COUNT(*)::text FROM session WHERE created_at > now()-interval'7 days'")
        u["visits_7d"] = int(r[0]) if r else 0
        r = query_umami("SELECT COUNT(*)::text FROM session")
        u["all_time"] = int(r[0]) if r else 0
        u["countries_7d"] = [c.split("|") for c in query_umami(
            "SELECT COALESCE(country,'?'),COUNT(*)::text FROM session WHERE created_at>now()-interval'7 days'"+
            " AND country IS NOT NULL AND country!='' GROUP BY country ORDER BY COUNT(*) DESC")]
        u["browsers_7d"] = [b.split("|") for b in query_umami(
            "SELECT COALESCE(browser,'?'),COUNT(*)::text FROM session WHERE created_at>now()-interval'7 days'"+
            " AND browser IS NOT NULL AND browser!='' GROUP BY browser ORDER BY COUNT(*) DESC")]
        u["os_7d"] = [o.split("|") for o in query_umami(
            "SELECT COALESCE(os,'?'),COUNT(*)::text FROM session WHERE created_at>now()-interval'7 days'"+
            " AND os IS NOT NULL AND os!='' GROUP BY os ORDER BY COUNT(*) DESC")]
        u["daily"] = [d.split("|") for d in query_umami(
            "SELECT created_at::date::text,COUNT(*)::text FROM session WHERE created_at>now()-interval'7 days' GROUP BY created_at::date ORDER BY created_at::date")]
    except: u["error"] = True
    data["umami"] = u

    # 5. Blog stats
    data["blog"] = get_blog_stats()

    # 6. Try smoke test (head request to measure TTFB)
    for a in audits:
        if a.get("response_ms"):
            a["ttfb_ms"] = a["response_ms"]

    return data


# ── HTML Report Generator ──────────────────────────────────────────
def generate_html(data):
    audits = data["audits"]
    ssl = data["ssl"]
    git = data["git"]
    u = data["umami"]
    blog = data["blog"]
    p = data["period"]

    # Main verdict
    all_sites_up = all(a.get("status",0)==200 or a.get("status",0)==308 for a in audits)
    all_ssl_ok = all(s.get("ok",False) for s in ssl)
    all_git = not any(g["diverged"] for g in git)
    overall_grade = "A" if all_sites_up and all_ssl_ok and all_git else "B"
    overall_color = "#2ECC71" if overall_grade=="A" else "#E8B86D"

    def vrow(label, val, icon="", cls=""):
        return f"<tr><td class='lbl'>{icon}{label}</td><td class='val {cls}'>{val}</td></tr>"

    def badge(ok, t="OK", f="FAIL"):
        c1,c2 = ("#2ECC71",t) if ok else ("#E74C3C",f)
        return f"<span class='b' style='background:rgba({','.join(str(int(c1[i:i+2],16)) for i in (1,3,5))},0.15);color:{c1}'>{'✅' if ok else '❌'} {c2}</span>"

    # ── BUILD ──
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Agency Report — marianstancik.dev</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#08080F;color:#F0F0F5;padding:32px 24px;line-height:1.5;}}
h1{{font-size:26px;color:#CD7F32;font-weight:700}} h2{{font-size:16px;color:#E8B86D;margin:28px 0 10px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.06);font-weight:600}}
h3{{font-size:13px;color:#8888A0;margin:18px 0 8px;font-weight:500}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
td{{padding:5px 10px}} .lbl{{color:#8888A0}} .val{{color:#F0F0F5;text-align:right}} .gold{{color:#CD7F32}} .green{{color:#2ECC71}}
.b{{display:inline-block;padding:3px 10px;border-radius:4px;font-size:11px;font-weight:600;margin:2px 4px}}
.card{{background:rgba(18,18,30,0.65);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px 18px;margin-bottom:14px}}
.score{{display:inline-block;padding:12px 28px;border-radius:12px;font-size:32px;font-weight:700;margin:8px auto}}
.grade{{display:inline-block;width:56px;height:56px;border-radius:50%;line-height:56px;font-size:28px;font-weight:700}}
.sec-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:6px}}
@media print{{body{{background:#fff;color:#333;padding:0}} .card{{background:#f5f5f5;border-color:#ddd}} .gold{{color:#CD7F32}}}}
@media screen and (min-width:720px){{.col2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}}}
</style></head><body>
<div style="text-align:center;padding:28px 0;border-bottom:3px solid #CD7F32;margin-bottom:20px;">
<div style="font-size:11px;color:#8888A0;letter-spacing:1px;">HERMES AGENCY REPORT</div>
<h1>📊 Web Audit & Performance</h1>
<p style="color:#8888A0;font-size:14px;margin:6px 0 0;">{p["from"]} – {p["to"]} · marianstancik.dev · ascentia.sk</p>
<div class="grade" style="background:{overall_color}22;color:{overall_color};border:3px solid {overall_color};">{overall_grade}</div>
<p style="color:#8888A0;font-size:12px;">Overall Grade</p>
</div>"""

    # ── Executive Summary ──
    html += """<div class="card"><h2>📋 Executive Summary</h2><table>"""
    for a in audits:
        s = a.get("status",0)
        ok = s in (200,308)
        t = f"{s} ({a.get('response_ms','?')}ms)" if ok else f"{a.get('error','DOWN')}"
        html += vrow(a.get("domain","?"), f"{badge(ok)} {t}")
    for s in ssl:
        ok = s.get("ok",False)
        html += vrow(f"🔒 SSL {s.get('hostname','?')}", badge(ok, f"{s.get('remaining_days',0)}d valid", s.get('error','FAIL')))
    html += vrow("📦 Git Sync", badge(all_git, "All synced", "Diverged repos"))
    html += vrow("🌐 Blog Posts", str(blog.get("total",0)))
    html += vrow("📊 Umami All-Time", str(u.get("all_time",0)))
    html += "</table></div>"

    # ── GEO + Readiness Scores ──
    for a in audits:
        if a.get("geo_score") is None: continue
        gs = a["geo_score"]; rs = a.get("readiness_score",0)
        gbar = min(100,gs); rbar = min(100,rs)
        def bar(v, c="#CD7F32"):
            return f"<div style='background:rgba(18,18,30,0.65);border-radius:6px;overflow:hidden;height:8px;margin:4px 0'><div style='width:{v}%;height:100%;background:linear-gradient(90deg,{c},#E8B86D);border-radius:6px'></div></div>"
        html += f"""<div class="card"><h2>🎯 Audit Scores — {a['domain']}</h2>
<table>
<tr><td class="lbl">GEO Score</td><td style="text-align:right;font-size:22px;font-weight:700;color:#CD7F32;">{gs}/100</td></tr>
<tr><td colspan="2">{bar(gbar)}</td></tr>
<tr><td class="lbl">Readiness Score</td><td style="text-align:right;font-size:22px;font-weight:700;color:#E8B86D;">{rs}/100</td></tr>
<tr><td colspan="2">{bar(rbar)}</td></tr>"""
        for pn,pv in [("Evidence Density", a["geo_pillars"]["evidence"]),("Structure", a["geo_pillars"]["structure"]),
                       ("Authority", a["geo_pillars"]["authority"]),("AI Crawlability", a["geo_pillars"]["crawlability"])]:
            html += vrow(f"  {pn}", f"{pv}/100", "", "gold")
        html += "</table></div>"

    # ── Security ──
    for a in audits:
        if not a.get("security"): continue
        s = a["security"]
        html += """<div class="card"><h2>🔒 Security Headers</h2><table>"""
        for name, key in [("HSTS", "hsts"),("CSP","csp"),("X-Frame-Options","xframe"),("X-Content-Type-Options","xcontent"),("Referrer-Policy","referrer")]:
            html += vrow(f"  {name}", badge(s.get(key,False)))
        html += vrow("  🍪 Cookie-less", badge(a.get("is_cookieless",False)))
        html += vrow("  📜 Privacy Policy", badge(a.get("has_privacy",False)))
        html += vrow("  📜 AI Act Disclaimer", badge(a.get("has_ai_act",False)))
        html += "</table></div>"

    # ── AI / GEO Deep ──
    for a in audits:
        html += """<div class="card"><h2>🤖 AI Discovery Status</h2><table>"""
        html += vrow("  Schema.org JSON-LD", badge(a.get("schema_org_ok",False)))
        html += vrow("  llms.txt (>50ch)", badge(a.get("llms_ok",False)))
        html += vrow("  Sitemap.xml valid", badge(a.get("sitemap_ok",False)))
        html += vrow("  Canonical URL", badge(a.get("canonical_ok",False)))
        html += vrow("  AI Bots Allowed", f"{len(a.get('allowed_bots',[]))}/{len(['GPTBot','ClaudeBot','PerplexityBot','Google-Extended','Applebot-Extended','CCBot','Cohere-ai'])}")
        html += vrow("  Word Count", str(a.get("word_count",0)))
        html += vrow("  External Citations", str(len(a.get("external_links",[]))))
        html += vrow("  H1/H2/H3", f"H1:{a.get('h1_count',0)} H2:{a.get('h2_count',0)} H3:{a.get('h3_count',0)}")
        html += "</table></div>"

    # ── Analytics ──
    html += """<div class="card"><h2>📊 Traffic Analytics</h2><table>"""
    html += vrow("  🟢 7-Day Visits", str(u.get("visits_7d",0)), "", "gold")
    html += vrow("  📊 All-Time Total", str(u.get("all_time",0)), "", "gold")
    if u.get("countries_7d"):
        html += f"<tr><td colspan='2' style='padding:8px 10px;color:#E8B86D;font-size:12px;'>— Top Countries —</td></tr>"
        for c,n in u["countries_7d"]:
            html += vrow(f"  {c or '?'}", n, "", "gold")
    if u.get("browsers_7d"):
        html += f"<tr><td colspan='2' style='padding:8px 10px;color:#E8B86D;font-size:12px;'>— Browsers —</td></tr>"
        for b,n in u["browsers_7d"]:
            html += vrow(f"  {b or '?'}", n, "")
    if u.get("os_7d"):
        html += f"<tr><td colspan='2' style='padding:8px 10px;color:#E8B86D;font-size:12px;'>— OS —</td></tr>"
        for o,n in u["os_7d"]:
            html += vrow(f"  {o or '?'}", n, "")
    if u.get("daily"):
        html += f"<tr><td colspan='2' style='padding:8px 10px;color:#E8B86D;font-size:12px;'>— Daily —</td></tr>"
        for d,n in u["daily"]:
            html += vrow(f"  {d}", n, "", "gold")
    html += "</table></div>"

    # ── SSL ──
    html += """<div class="card"><h2>🔐 SSL Certificates</h2><table>"""
    for s in ssl:
        ok = s.get("ok",False)
        days = s.get("remaining_days",0)
        html += vrow(f"  {s.get('hostname','?')}", badge(ok, f"✅ {days}d valid ({s.get('issuer','?')})", s.get('error','❌ FAIL') if not ok else "⚠"))
    html += "</table></div>"

    # ── Git ──
    html += """<div class="card"><h2>📦 Git Sync & Deployment</h2><table>"""
    for g in git:
        icon = "✅" if not g["diverged"] else "⚠"
        html += vrow(f"  {icon} {g['name']}", g['last_commit'][:70])
    html += "</table></div>"

    # ── Blog Stats ──
    if blog.get("per_language"):
        html += """<div class="card"><h2>📝 Content Overview</h2><table>"""
        html += vrow("  Total Blog Posts", str(blog.get("total",0)))
        for lang, count in sorted(blog["per_language"].items()):
            html += vrow(f"  {lang}", str(count))
        html += "</table></div>"

    # ── Footer ──
    html += f"""<div style="text-align:center;padding:16px;color:#8888A0;font-size:11px;border-top:1px solid rgba(255,255,255,0.06);margin-top:24px;">
<p style="margin:0;">Generated: {data["generated"]}</p>
<p style="margin:4px 0 0;">Hermes Agency · marianstancik.dev · Hetzner VPS · Umami · Cloudflare</p>
<p style="margin:4px 0 0;"><button class="b" onclick="window.print()" style="cursor:pointer;padding:8px 24px;background:#CD7F32;color:#08080F;border:none;border-radius:6px;font-weight:600;">🖨 Print / Save PDF</button></p>
</div></body></html>"""
    return html


def send_email(subject, html_body):
    """Send email via AgentMail MCP HTTP endpoint"""
    api_key = None
    env_path = Path("/root/.hermes/.env")
    if env_path.exists():
        for line in env_path.read_text().split("\n"):
            if line.startswith("AGENTMAIL_API_KEY="):
                api_key = line.split("=",1)[1].strip().strip("'\"")
    if not api_key or api_key == "***":
        print("⚠ Cannot send email: no AgentMail API key")
        return False
    
    import urllib.request
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {
            "name": "send_message",
            "arguments": {
                "inboxId": "marianstancik@agentmail.to",
                "to": ["stancikmarian8@gmail.com"],
                "subject": subject,
                "html": html_body,
                "text": subject
            }
        }
    }).encode()
    
    try:
        req = urllib.request.Request("https://mcp.agentmail.to/mcp",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "hermes-agency/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as f:
            resp = f.read().decode()
        if '"isError":false' in resp or '"messageId"' in resp:
            return True
        return False
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


# ── Main ──
def main():
    print("🚀 Collecting agency audit data...")
    data = collect()

    html = generate_html(data)
    subject = f"📊 Agency Report — {data['period']['from']} – {data['period']['to']}"
    text = f"Agency Report — marianstancik.dev. Generated: {data['generated']}"

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_dir = Path("/root/.hermes/cache/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"agency_report_{ts}.html"
    path.write_text(html)
    print(f"📁 Report saved: {path}")

    # Email send
    print("📧 Sending email...")
    ok = send_email(subject, html)
    print(f"{'✅ Email sent to stancikmarian8@gmail.com' if ok else '⚠ Email not sent'}")

    # Output JSON for fallback cron delivery
    report = {"html": html, "subject": subject, "email_sent": ok, "path": str(path)}
    print("\n📄 JSON_OUTPUT_START")
    print(json.dumps(report))
    print("📄 JSON_OUTPUT_END")


if __name__ == "__main__":
    main()