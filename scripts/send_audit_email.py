#!/usr/bin/env python3
"""
Direct Audit Report Dispatcher via AgentMail MCP.
Sends the newly generated 2-page AI GEO Audit PDF as an attachment + rich HTML email
to stancikmarian8@gmail.com.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure PDF is freshly generated
from generate_geo_audit_pdf import build_geo_audit_pdf

PDF_PATH = "assets/sample-geo-audit.pdf"
build_geo_audit_pdf(PDF_PATH, client_name="Marian Stancik", client_url="https://www.marianstancik.dev")

if not os.path.exists(PDF_PATH):
    print(f"❌ Error: {PDF_PATH} does not exist!")
    sys.exit(1)

with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
print(f"📦 Encoded PDF attachment: {len(pdf_bytes)} bytes ({len(pdf_base64)} b64 chars)")

# AgentMail MCP configuration
AGENTMAIL_API_KEY = os.getenv("AGENTMAIL_API_KEY", "")
if not AGENTMAIL_API_KEY:
    hermes_env = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(hermes_env):
        with open(hermes_env) as f:
            for line in f:
                if line.startswith("AGENTMAIL_API_KEY="):
                    AGENTMAIL_API_KEY = line.split("=", 1)[1].strip().strip('"\'')

SENDER_INBOX = "ascentia@agentmail.to"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "x-api-key": AGENTMAIL_API_KEY
}

# 1. Initialize MCP session
init_payload = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "geo-audit-delivery", "version": "1.0"}
    }
}

req_init = urllib.request.Request(AGENTMAIL_URL, data=json.dumps(init_payload).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req_init) as resp:
    sess_id = resp.headers.get("Mcp-Session-Id")
    init_data = resp.read().decode('utf-8')
    if not sess_id:
        for line in init_data.split('\n'):
            if line.startswith('data:'):
                try:
                    d = json.loads(line[5:].strip())
                    sess_id = d.get('result', {}).get('sessionId')
                except Exception:
                    pass

if sess_id:
    headers["Mcp-Session-Id"] = sess_id
    print(f"🔑 MCP Session initialized: {sess_id}")

# 2. Rich HTML Body with Bronze Neural Styling (Zero broken images, pure email-safe CSS)
html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI GEO Audit Report</title>
</head>
<body style="margin:0; padding:0; background-color:#08080F; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif; color:#F0F0F5;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#08080F; padding:24px 12px;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px; width:100%; background-color:#0D0D18; border:1px solid rgba(255,255,255,0.08); border-radius:12px; overflow:hidden; box-shadow:0 12px 40px rgba(0,0,0,0.6);">
          
          <!-- Header Bar -->
          <tr>
            <td style="background-color:#12121E; padding:26px 36px 22px; border-bottom:2px solid #CD7F32; text-align:left;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td>
                    <div style="font-size:22px; font-weight:700; letter-spacing:4px; color:#E8B86D; text-transform:uppercase; margin-bottom:4px;">ASCENTIA</div>
                    <div style="color:#CD7F32; font-size:11px; font-weight:600; letter-spacing:2px; text-transform:uppercase;">✦ AI AGENT SYSTEMS · TECHNICAL AUDITS</div>
                  </td>
                  <td align="right">
                    <span style="display:inline-block; padding:5px 12px; background:rgba(205,127,50,0.15); border:1px solid rgba(205,127,50,0.4); border-radius:6px; font-size:11px; font-weight:600; color:#E8B86D;">
                      AUDIT DELIVERED
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Main Content -->
          <tr>
            <td style="padding:32px 36px 20px;">
              <h1 style="margin:0 0 8px; font-size:22px; font-weight:700; color:#FFFFFF; line-height:1.3;">
                ✦ Váš AI GEO Audit je pripravený
              </h1>
              <p style="margin:0 0 20px; color:#94A3B8; font-size:14px; line-height:1.6;">
                Analyzovaná doména: <strong style="color:#F0F0F5;">https://www.marianstancik.dev</strong><br>
                Dátum vyhotovenia: <strong style="color:#F0F0F5;">17. septembra 2026</strong> · Klient: <strong style="color:#F0F0F5;">Marian Stancik</strong>
              </p>

              <!-- Score Card Box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:linear-gradient(135deg, rgba(26,26,42,0.9), rgba(18,18,30,0.95)); border:1px solid #CD7F32; border-radius:10px; margin-bottom:24px;">
                <tr>
                  <td style="padding:20px 24px; text-align:center; width:140px; border-right:1px solid rgba(205,127,50,0.25);">
                    <div style="font-size:36px; font-weight:800; color:#CD7F32; line-height:1;">66</div>
                    <div style="font-size:13px; font-weight:600; color:#64748B; margin-top:2px;">/ 100</div>
                    <div style="font-size:11px; font-weight:700; color:#16A34A; margin-top:8px;">● Pevný základ</div>
                  </td>
                  <td style="padding:18px 24px;">
                    <div style="font-size:14px; font-weight:700; color:#E8B86D; margin-bottom:6px;">Zhrnutie auditu viditeľnosti v AI modeloch:</div>
                    <div style="font-size:13px; color:#CBD5E1; line-height:1.6;">
                      Web má perfektnú technickú infraštruktúru, rýchly server-side kód a otvorené pravidlá pre AI botov v robots.txt. Hlavný priestor na rast spočíva v <strong>hustote overiteľných dát (Evidence Density)</strong> a expertných citáciách. Potenciál po optimalizácii: <strong style="color:#16A34A;">82+ bodov</strong>.
                    </div>
                  </td>
                </tr>
              </table>

              <!-- 4 Pillars Table -->
              <h2 style="margin:0 0 12px; font-size:15px; font-weight:600; color:#E8B86D; text-transform:uppercase; letter-spacing:1px;">
                Rozpad skóre podľa 4 kľúčových pilierov
              </h2>
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse; margin-bottom:26px; font-size:13px;">
                <tr style="background-color:#12121E; border-bottom:2px solid #CD7F32;">
                  <th align="left" style="padding:10px 12px; color:#E8B86D; font-weight:600;">Pilier hodnotenia</th>
                  <th align="center" style="padding:10px 8px; color:#E8B86D; font-weight:600;">Body</th>
                  <th align="center" style="padding:10px 8px; color:#E8B86D; font-weight:600;">Váha</th>
                  <th align="right" style="padding:10px 12px; color:#E8B86D; font-weight:600;">Stav</th>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.06); background-color:rgba(255,255,255,0.01);">
                  <td style="padding:10px 12px; color:#F0F0F5;"><strong>1. Evidence Density</strong> (štatistiky, čísla, štúdie)</td>
                  <td align="center" style="padding:10px 8px; color:#F0F0F5;">14 / 35</td>
                  <td align="center" style="padding:10px 8px; color:#94A3B8;">35%</td>
                  <td align="right" style="padding:10px 12px; color:#D97706; font-weight:600;">Zlepšiť</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.06); background-color:rgba(255,255,255,0.03);">
                  <td style="padding:10px 12px; color:#F0F0F5;"><strong>2. Structure &amp; Position</strong> (FAQ, sémantika, 150w)</td>
                  <td align="center" style="padding:10px 8px; color:#F0F0F5;">20 / 25</td>
                  <td align="center" style="padding:10px 8px; color:#94A3B8;">25%</td>
                  <td align="right" style="padding:10px 12px; color:#16A34A; font-weight:600;">Veľmi dobré</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.06); background-color:rgba(255,255,255,0.01);">
                  <td style="padding:10px 12px; color:#F0F0F5;"><strong>3. Authority Signals</strong> (entity, disclaimery, sameAs)</td>
                  <td align="center" style="padding:10px 8px; color:#F0F0F5;">19 / 25</td>
                  <td align="center" style="padding:10px 8px; color:#94A3B8;">25%</td>
                  <td align="right" style="padding:10px 12px; color:#16A34A; font-weight:600;">Dobrý základ</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.06); background-color:rgba(255,255,255,0.03);">
                  <td style="padding:10px 12px; color:#F0F0F5;"><strong>4. AI Crawlability</strong> (llms.txt, SSR, robots.txt)</td>
                  <td align="center" style="padding:10px 8px; color:#F0F0F5;">13 / 15</td>
                  <td align="center" style="padding:10px 8px; color:#94A3B8;">15%</td>
                  <td align="right" style="padding:10px 12px; color:#16A34A; font-weight:600;">Excelentné</td>
                </tr>
              </table>

              <!-- TOP 5 Recommendations -->
              <h2 style="margin:0 0 12px; font-size:15px; font-weight:600; color:#E8B86D; text-transform:uppercase; letter-spacing:1px;">
                TOP 5 Prioritných opráv (Roadmap k 82+ bodom)
              </h2>
              <div style="background-color:#12121E; border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:16px 20px; margin-bottom:24px;">
                <ol style="margin:0; padding-left:20px; color:#CBD5E1; font-size:13px; line-height:1.7;">
                  <li style="margin-bottom:8px;">
                    <strong style="color:#FFFFFF;">Doplniť externé citácie a trhové štatistiky</strong> <span style="color:#CD7F32; font-weight:600;">[+8 bodov]</span><br>
                    <span style="color:#94A3B8; font-size:12px;">Pridať 1–2 citácie z relevantných štúdií (napr. Gartner o AI agentoch) s hypertextovými odkazmi.</span>
                  </li>
                  <li style="margin-bottom:8px;">
                    <strong style="color:#FFFFFF;">Pridať citácie expertov (Quotation Addition)</strong> <span style="color:#CD7F32; font-weight:600;">[+6 bodov]</span><br>
                    <span style="color:#94A3B8; font-size:12px;">Priame citovanie autorít (Karpathy, Brown) prináša podľa GEO výskumov až +41% nárast citovanosti.</span>
                  </li>
                  <li style="margin-bottom:8px;">
                    <strong style="color:#FFFFFF;">Front-loadovať odpovede v prvých 150 slovách</strong> <span style="color:#CD7F32; font-weight:600;">[+5 bodov]</span><br>
                    <span style="color:#94A3B8; font-size:12px;">AI vyhľadávače indexujú úvody stránok. Odpoveď na hlavnú tému musí odznieť priamo v prvom odseku.</span>
                  </li>
                  <li style="margin-bottom:8px;">
                    <strong style="color:#FFFFFF;">Pridať dateModified priamo do HTML</strong> <span style="color:#CD7F32; font-weight:600;">[+3 body]</span><br>
                    <span style="color:#94A3B8; font-size:12px;">Doplniť meta property="article:modified_time" a JSON-LD atribút pre signál čerstvosti obsahu.</span>
                  </li>
                  <li>
                    <strong style="color:#FFFFFF;">Posilniť externé validačné signály (Wikipedia / Zmienky)</strong> <span style="color:#CD7F32; font-weight:600;">[+4 body]</span><br>
                    <span style="color:#94A3B8; font-size:12px;">Registrácia v autoritatívnych odborných adresároch pre posilnenie bázy pre ChatGPT Search a Perplexity.</span>
                  </li>
                </ol>
              </div>

              <!-- Action Callout Box with Attachment Info -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:rgba(205,127,50,0.08); border:1px solid #CD7F32; border-radius:8px; margin-bottom:28px;">
                <tr>
                  <td style="padding:16px 20px;">
                    <div style="font-size:14px; font-weight:700; color:#E8B86D; margin-bottom:4px;">
                      📎 Kompletný 2-stranový PDF Report je priložený v prílohe
                    </div>
                    <div style="font-size:12.5px; color:#CBD5E1; line-height:1.5;">
                      Súbor <strong>AI-GEO-Audit-marianstancik-dev.pdf</strong> obsahuje kompletnú 20-bodovú technickú maticu, VETO previerky, rozpad váh a strategické odporúčania.
                    </div>
                  </td>
                </tr>
              </table>

              <!-- Strategic Consultation Note -->
              <p style="margin:0 0 16px; color:#94A3B8; font-size:13px; line-height:1.6;">
                V prípade otázok k realizácii prioritných bodov alebo záujmu o implementáciu na kľúč mi stačí odpovedať priamo na tento email.
              </p>
            </td>
          </tr>

          <!-- Signature Block -->
          <tr>
            <td style="padding:16px 36px 24px; border-top:1px solid rgba(255,255,255,0.08); background-color:#12121E;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td>
                    <div style="font-size:14px; font-weight:700; color:#FFFFFF;">Marian Stancik</div>
                    <div style="font-size:12px; color:#CD7F32; margin-top:2px;">✦ Hermes Agent — ASCENTIA s.r.o.</div>
                    <div style="font-size:11px; color:#64748B; margin-top:4px;">Building autonomous systems that run without you.</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Corporate Footer -->
          <tr>
            <td style="padding:14px 36px; background-color:#08080F; border-top:1px solid rgba(255,255,255,0.05); font-size:11px; color:#64748B; line-height:1.5;">
              <strong>ASCENTIA s.r.o.</strong> · Klincová 37/B, 821 08 Bratislava, Slovakia · IČO: 51858959 · DIČ: 2120816071<br>
              Tento report bol vypracovaný systémom umelej inteligencie (ASCENTIA Hermes Agent) a nepredstavuje právne poradenstvo.
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

plain_text = """ASCENTIA s.r.o. — AI GEO AUDIT REPORT
==================================================

Ahoj Marian,

V prílohe tohto emailu nájdeš kompletný technický AI GEO Audit Report pre doménu https://www.marianstancik.dev.

ZHRNUTIE VÝSLEDKOV:
-------------------
• Celkové GEO Skóre: 66 / 100 (Pevný základ, potenciál 82+)
• Analyzovaná doména: https://www.marianstancik.dev
• Dátum vyhotovenia: 17. septembra 2026

4 KĽÚČOVÉ PILIERE:
-------------------
1. Evidence Density: 14 / 35 bodov (35% váha) — Zlepšiť
2. Structure & Position: 20 / 25 bodov (25% váha) — Veľmi dobré
3. Authority Signals: 19 / 25 bodov (25% váha) — Dobrý základ
4. AI Crawlability: 13 / 15 bodov (15% váha) — Excelentné

TOP 5 PRIORITNÝCH OPRÁV (NÁRAST +16 AŽ +18 BODOV):
--------------------------------------------------
1. Doplniť externé citácie a trhové štatistiky (+8 bodov)
2. Pridať citácie expertov (Quotation Addition, +6 bodov)
3. Front-loadovať odpovede v prvých 150 slovách (+5 bodov)
4. Pridať dateModified priamo do HTML (+3 body)
5. Posilniť externé validačné signály (+4 body)

Kompletnú 20-bodovú technickú maticu nájdeš v priloženom PDF súbore:
AI-GEO-Audit-marianstancik-dev.pdf

S pozdravom,
Marian Stancik
ASCENTIA s.r.o.
Klincová 37/B, 821 08 Bratislava
"""

# 3. Construct send_message payload with PDF attachment
send_args = {
    "inboxId": SENDER_INBOX,
    "to": [RECIPIENT],
    "subject": "✦ Výsledky AI GEO Auditu: marianstancik.dev (Skóre 66/100) — Marian Stancik",
    "text": plain_text,
    "html": html_content,
    "attachments": [
        {
            "filename": "AI-GEO-Audit-marianstancik-dev.pdf",
            "contentType": "application/pdf",
            "contentDisposition": "attachment",
            "content": pdf_base64
        }
    ]
}

send_payload = {
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/call",
    "params": {
        "name": "send_message",
        "arguments": send_args
    }
}

print(f"🚀 Sending email with PDF attachment from {SENDER_INBOX} to {RECIPIENT}...")
req_send = urllib.request.Request(AGENTMAIL_URL, data=json.dumps(send_payload).encode('utf-8'), headers=headers)

try:
    with urllib.request.urlopen(req_send, timeout=30) as resp:
        res_text = resp.read().decode('utf-8')
        print("📥 AgentMail response:")
        print(res_text[:500])
        if '"isError":true' in res_text:
            print("❌ Error from AgentMail tool call!")
            sys.exit(1)
        else:
            print(f"✅ EMAIL SUCCESSFULLY SENT WITH PDF ATTACHMENT TO {RECIPIENT}!")
except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error {e.code}: {e.read().decode('utf-8')}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error sending email: {e}")
    sys.exit(1)
