#!/usr/bin/env python3
"""
Weekly Analytics & Site Health Report for marianstancik.dev
Queries Umami DB directly + checks sites + git sync → email via AgentMail
"""
import subprocess, json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────
SITES = [
    {"name": "marianstancik.dev", "url": "https://marianstancik.dev"},
    {"name": "www.marianstancik.dev", "url": "https://www.marianstancik.dev"},
    {"name": "ascentia.sk", "url": "https://www.ascentia.sk"},
    {"name": "API", "url": "https://api.marianstancik.dev/api/health"},
]
GIT_REPOS = [
    {"path": "/root/projects/marian-stancik-web", "name": "marian-stancik-web"},
    {"path": "/root/projects/ascentia-web", "name": "ascentia-web"},
]
AGENTMAIL_FROM = "marianstancik@agentmail.to"
AGENTMAIL_TO = ["marianstancik@agentmail.to"]
WEBSITE_ID = "ec1c0df8-e51f-4236-9ad0-e3992f0b1637"

# Get Umami DB password from Docker container
def get_umami_db_pass():
    try:
        r = subprocess.run(
            ["docker", "inspect", "umami-umami-db-1"],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(r.stdout)
        for env in data[0]["Config"]["Env"]:
            if env.startswith("POSTGRES_PASSWORD="):
                return env.split("=", 1)[1]
    except: pass
    return "umami_pass_change_me"


# ── Helpers ────────────────────────────────────────────────────────
def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def check_site(url):
    r = run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}|%{time_total}s", url], timeout=10)
    if "ERROR" in r:
        return {"status": "ERROR", "code": 0, "time": 0, "ok": False}
    parts = r.split("|")
    code = parts[0] if parts else "000"
    t = parts[1] if len(parts) > 1 else "0s"
    ok = code.startswith("2") or code == "308"  # 308 is redirect (expected for apex)
    return {"status": code, "time": t, "ok": ok}

def check_git(repo):
    git_cmd = ["git", "-C", repo["path"]]
    fetch = run(git_cmd + ["fetch", "origin", "-q"], timeout=10)
    behind = run(git_cmd + ["log", "--oneline", "HEAD..origin/main"], timeout=5)
    ahead = run(git_cmd + ["log", "--oneline", "origin/main..HEAD"], timeout=5)
    last_commit = run(git_cmd + ["log", "--oneline", "-1"], timeout=5)
    diverged = bool(behind and behind != "ERROR" and behind.strip()) or bool(ahead and ahead != "ERROR" and ahead.strip())
    return {
        "name": repo["name"],
        "last_commit": last_commit,
        "behind": behind.strip() if behind and behind != "ERROR" else "",
        "ahead": ahead.strip() if ahead and ahead != "ERROR" else "",
        "diverged": diverged
    }

def query_umami(sql):
    """Query Umami DB via docker exec (only way to reach it)"""
    pw = get_umami_db_pass()
    r = subprocess.run(
        ["docker", "exec", "-e", f"PGPASSWORD={pw}",
         "umami-umami-db-1", "psql", "-U", "umami", "-d", "umami",
         "-t", "-A", "-F", "|", "-c", sql],
        capture_output=True, text=True, timeout=15
    )
    if r.returncode != 0:
        return []
    return [l for l in r.stdout.strip().split("\n") if l.strip() and not l.strip().startswith("(")]


# ── Data Collection ────────────────────────────────────────────────
def collect():
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=7)

    # Site health
    site_results = [{"name": s["name"], **check_site(s["url"])} for s in SITES]

    # Git status
    git_results = [check_git(r) for r in GIT_REPOS]

    # Umami weekly stats
    u = {}
    try:
        r = query_umami(
            "SELECT COUNT(*)::text FROM session "
            "WHERE created_at > now() - interval '7 days'"
        )
        u["visits"] = int(r[0]) if r else 0

        r = query_umami(
            "SELECT COUNT(DISTINCT country)::text FROM session "
            "WHERE created_at > now() - interval '7 days'"
        )
        u["countries"] = int(r[0]) if r else 0

        u["country_list"] = query_umami(
            "SELECT COALESCE(country,'?'), COUNT(*)::text as cnt FROM session "
            "WHERE created_at > now() - interval '7 days' AND country IS NOT NULL AND country != '' "
            "GROUP BY country ORDER BY COUNT(*) DESC"
        )
        u["country_list"] = [c.split("|") for c in u["country_list"]]

        u["browser_list"] = query_umami(
            "SELECT COALESCE(browser,'?'), COUNT(*)::text FROM session "
            "WHERE created_at > now() - interval '7 days' AND browser IS NOT NULL AND browser != '' "
            "GROUP BY browser ORDER BY COUNT(*) DESC"
        )
        u["browser_list"] = [b.split("|") for b in u["browser_list"]]

        u["os_list"] = query_umami(
            "SELECT COALESCE(os,'?'), COUNT(*)::text FROM session "
            "WHERE created_at > now() - interval '7 days' AND os IS NOT NULL AND os != '' "
            "GROUP BY os ORDER BY COUNT(*) DESC"
        )
        u["os_list"] = [o.split("|") for o in u["os_list"]]

        u["lang_list"] = query_umami(
            "SELECT COALESCE(language,'?'), COUNT(*)::text FROM session "
            "WHERE created_at > now() - interval '7 days' AND language IS NOT NULL AND language != '' "
            "GROUP BY language ORDER BY COUNT(*) DESC"
        )
        u["lang_list"] = [l.split("|") for l in u["lang_list"]]

        u["daily"] = query_umami(
            "SELECT created_at::date::text, COUNT(*)::text FROM session "
            "WHERE created_at > now() - interval '7 days' "
            "GROUP BY created_at::date ORDER BY created_at::date"
        )
        u["daily"] = [d.split("|") for d in u["daily"]]

        r = query_umami("SELECT COUNT(*)::text FROM session")
        u["all_time"] = int(r[0]) if r else 0

        r = query_umami(
            "SELECT created_at::date::text FROM session "
            "ORDER BY created_at ASC LIMIT 1"
        )
        u["first_date"] = r[0] if r else "?"
    except Exception as e:
        u["error"] = str(e)

    return {
        "sites": site_results,
        "git": git_results,
        "umami": u,
        "period": {"from": week_start.strftime("%d.%m.%Y"), "to": now.strftime("%d.%m.%Y")},
        "generated": now.strftime("%d. %B %Y %H:%M CEST")
    }


# ── Report Generation ──────────────────────────────────────────────
def generate(data):
    s = data["sites"]
    g = data["git"]
    u = data["umami"]
    p = data["period"]

    def td(v, c="#F0F0F5"):
        return f'<td style="padding:5px 8px;color:{c};">{v}</td>'

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,sans-serif;background:#0D0D18;color:#F0F0F5;padding:24px;line-height:1.5}}
h1{{font-size:22px;color:#CD7F32;margin:0 0 4px}}
h2{{font-size:14px;color:#E8B86D;margin:18px 0 8px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.06)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
.bx{{background:rgba(18,18,30,0.65);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px 14px;margin-bottom:12px}}
.ok{{color:#2ECC71}} .fail{{color:#E74C3C}} .muted{{color:#8888A0}} .gold{{color:#CD7F32}}
.badge{{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:600}}
.badge-ok{{background:rgba(46,204,113,0.15);color:#2ECC71}} .badge-fail{{background:rgba(231,76,60,0.15);color:#E74C3C}}
</style></head><body>
<div style="text-align:center;padding:20px 0;border-bottom:2px solid #CD7F32;margin-bottom:16px;">
<h1>📊 Týždenný Report</h1>
<p class="muted" style="font-size:13px;margin:4px 0;">marianstancik.dev · {p["from"]} – {p["to"]}</p>
</div>

<div class="bx">
<h2>🟢 Health Check</h2>
<table>"""
    for site in s:
        badge = '<span class="badge badge-ok">✅ OK</span>' if site["ok"] else '<span class="badge badge-fail">❌ DOWN</span>'
        html += f"<tr>{td(site['name'])}{td(badge)}{td(site['time'],'#8888A0')}</tr>"
    html += "</table></div>"

    html += """<div class="bx"><h2>📦 Git Sync</h2><table>"""
    for git in g:
        g_badge = '<span class="badge badge-ok">✓ V SYNC</span>' if not git["diverged"] else '<span class="badge badge-fail">⚠ DIVERGED</span>'
        html += f"<tr>{td(git['name'])}{td(g_badge)}{td(git['last_commit'][:60],'#8888A0')}</tr>"
    html += "</table></div>"

    html += """<div class="bx"><h2>📈 Analytics</h2><table>"""
    html += f"<tr>{td('Návštevy (7d)')}{td(str(u.get('visits','?')),'#E8B86D')}</tr>"
    html += f"<tr>{td('All-time total')}{td(str(u.get('all_time','?')),'#E8B86D')}</tr>"
    html += f"<tr>{td('Krajiny (7d)')}{td(str(u.get('countries','?')),'#E8B86D')}</tr>"
    if u.get("first_date"):
        html += f"<tr>{td('Tracking od')}{td(u['first_date'],'#8888A0')}</tr>"
    html += "</table></div>"

    if u.get("country_list"):
        html += """<div class="bx"><h2>🌍 Krajiny</h2><table>"""
        for c in u["country_list"]:
            html += f"<tr>{td(c[0])}{td(c[1],'#CD7F32')}</tr>"
        html += "</table></div>"

    if u.get("browser_list"):
        html += """<div class="bx"><h2>🌐 Prehliadače</h2><table>"""
        for b in u["browser_list"]:
            html += f"<tr>{td(b[0])}{td(b[1],'#CD7F32')}</tr>"
        html += "</table></div>"

    if u.get("os_list"):
        html += """<div class="bx"><h2>💻 OS</h2><table>"""
        for o in u["os_list"]:
            html += f"<tr>{td(o[0])}{td(o[1],'#CD7F32')}</tr>"
        html += "</table></div>"

    if u.get("daily"):
        html += """<div class="bx"><h2>📅 Dnevn</h2><table>"""
        for d in u["daily"]:
            html += f"<tr>{td(d[0])}{td(d[1],'#E8B86D')}</tr>"
        html += "</table></div>"

    if u.get("error"):
        html += f'<div class="bx"><p class="fail">⚠ DB chyba: {u["error"]}</p></div>'

    html += f"""<div style="text-align:center;padding:12px;color:#8888A0;font-size:11px;margin-top:16px;">
<p style="margin:0;">{data["generated"]}</p>
<p style="margin:4px 0 0;">Hermes Agent · VPS Hetzner · Umami DB</p>
</div></body></html>"""

    # Plain text
    text = f"""📊 TÝŽDENNÝ REPORT — marianstancik.dev
{p["from"]} – {p["to"]}
{'='*50}

🟢 HEALTH CHECK:
"""
    for site in s:
        icon = "✅" if site["ok"] else "❌"
        text += f"  {icon} {site['name']}: {site['status']} ({site['time']})\n"

    text += f"""
📦 GIT SYNC:
"""
    for git in g:
        icon = "✓" if not git["diverged"] else "⚠"
        text += f"  {icon} {git['name']}: {git['last_commit'][:70]}\n"

    text += f"""
📈 ANALYTICS (7 dní):
  Návštevy: {u.get("visits", "?")}
  All-time: {u.get("all_time", "?")}
  Krajiny:  {u.get("countries", "?")}
"""
    if u.get("country_list"):
        text += "\nKRAJINY:\n" + "\n".join(f"  {c[0]}: {c[1]}" for c in u["country_list"]) + "\n"
    if u.get("daily"):
        text += "\nDNEVNÉ:\n" + "\n".join(f"  {d[0]}: {d[1]}" for d in u["daily"]) + "\n"
    if u.get("browser_list"):
        text += "\nPREHLIADAČE:\n" + "\n".join(f"  {b[0]}: {b[1]}" for b in u["browser_list"]) + "\n"

    text += f"""
---
Hermes Agent · {data["generated"]}
"""
    return html, text


# ── Main ───────────────────────────────────────────────────────────
def main():
    print("📊 Zbieram data...")
    data = collect()

    html, text = generate(data)
    print(text)

    # Save HTML
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_dir = Path("/root/.hermes/cache/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / f"weekly_report_{ts}.html"
    html_path.write_text(html)

    # Output JSON for cron consumer
    report = {
        "html": html,
        "text": text,
        "subject": f"📊 Týždenný Report — {data['period']['from']} – {data['period']['to']}",
        "period": data["period"],
        "all_ok": all(s["ok"] for s in data["sites"]),
        "all_synced": not any(g["diverged"] for g in data["git"]),
    }
    print("\n📄 JSON_OUTPUT_START")
    print(json.dumps(report))
    print("📄 JSON_OUTPUT_END")
    print(f"\n📁 HTML report: {html_path}")


if __name__ == "__main__":
    main()