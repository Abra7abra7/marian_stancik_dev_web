#!/usr/bin/env python3
"""One-shot CSP refactor: replace inline onclick/onsubmit handlers with data attributes,
extract inline <script> blocks to external files, drop redundant meta CSP.
Run once, then verify + build. Part of the audit Phase 2 (script-src without 'unsafe-inline')."""
import re, sys, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
errors = []

def edit(path, transforms, must=True):
    p = BASE / path
    if not p.exists():
        errors.append(f"MISSING: {path}")
        return
    s = p.read_text(encoding="utf-8")
    orig = s
    for label, pattern, repl in transforms:
        s2, n = re.subn(pattern, repl, s, flags=re.M | re.S)
        if n == 0 and must:
            errors.append(f"{path}: pattern '{label}' matched 0×")
        s = s2
    if s != orig:
        p.write_text(s, encoding="utf-8")
        print(f"edited: {path}")

# 1) switchLanguage buttons -> data-lang-switch (root templates + blog index)
ROOT_TPL = ["index.html", "about.html", "contact.html", "services.html", "services-sk.html",
            "expertise.html", "skills.html", "drones.html", "blog/index.html"]
for f in ROOT_TPL:
    edit(f, [("switchLanguage", r'onclick="switchLanguage\(\'(\w+)\'\)"', r'data-lang-switch="\1"')])

# 2) meta CSP removal (redundant with _headers; locale copies regenerate from these)
for f in ["about.html", "contact.html", "drones.html", "expertise.html", "skills.html"]:
    edit(f, [("metaCSP", r'[ \t]*<meta http-equiv="Content-Security-Policy"[^>]*>\n', '')], must=False)

# 3) Stripe buttons -> data attributes (canonical keys fix the PRODUCTS mismatch)
KEYMAP = {
    "AI GEO Audit": "geo-audit",
    "AI Web Readiness Scan": "readiness",
    "Full Web Audit (GEO + Readiness)": "full-audit",
    "GEO Monitoring (Monthly)": "geo-monitoring",
    "GEO Monitoring": "geo-monitoring",
    "Compliance Watch (Monthly)": "compliance-watch",
    "Compliance Watch": "compliance-watch",
    "Full Monitoring Suite (Monthly)": "full-suite",
    "Full Monitoring Suite": "full-suite",
    "Custom AI Agent Architecture": "custom-agent",
    "Záloha za Vlastného Agenta": "agent-deposit",
    "Custom Agent Deposit": "agent-deposit",
}
def stripe_repl(m):
    title, price, key = m.group(1), m.group(2), m.group(3)
    canonical = KEYMAP.get(title, key)
    return f'data-checkout-key="{canonical}" data-price="{price}" data-title="{title}"'
STRIPE_RE = r'onclick="openStripeCheckout\(\'([^\']+)\', (\d+), \'([^\']+)\'\)"'

for f in ["services.html", "services-sk.html"]:
    edit(f, [
        ("stripe", STRIPE_RE, stripe_repl),
        ("modal-overlay", r'<div id="stripeModal" class="stripe-modal-overlay" onclick="closeStripeModal\(event\)">', '<div id="stripeModal" class="stripe-modal-overlay">'),
        ("modal-inner", r'<div class="stripe-modal" onclick="event\.stopPropagation\(\)">', '<div class="stripe-modal">'),
        ("modal-close", r'(<button class="stripe-modal-close") onclick="closeStripeModal\(event\)">', r'\1>'),
        ("modal-done", r'<button onclick="closeStripeModal\(event\)" class="btn-stripe"', '<button class="btn-stripe" data-close-stripe'),
        ("form-submit", r'(<form id="stripeCheckoutForm") onsubmit="handleStripeRedirect\(event\)"', r'\1>'),
    ])

# 4) remove plain inline <script> blocks + wire external scripts (services pages)
for f, script in [("services.html", "/js/stripe-checkout.js?v=1"), ("services-sk.html", "/js/stripe-checkout.js?v=1")]:
    edit(f, [
        ("inline-script", r'\n<script>\n// (?:Product configs|Centralizované smerovanie).*?\n</script>\n', '\n'),
        ("wire", r'(\n</body>)', rf'  <script src="{script}"></script>\1'),
    ])

# 5) contact.html: order-confirm inline block -> external file
edit("contact.html", [
    ("inline-script", r'\n<script>\ndocument\.addEventListener\(\'DOMContentLoaded\'.*?\n</script>\n', '\n'),
    ("wire", r'(\n</body>)', '  <script src="/js/order-confirm.js?v=1"></script>\\1'),
])

# 6) blog posts + blog index: onsubmit -> data-subscribe-lang, wire subscribe.js
POSTS = [str(p.relative_to(BASE)) for p in sorted((BASE / "blog" / "posts").rglob("*.html"))]
for f in POSTS + ["blog/index.html"]:
    edit(f, [
        ("subscribe", r'onsubmit="handleBlogSubscribe\(event, this, \'(\w+)\'\)"', r'data-subscribe-lang="\1"'),
        ("wire", r'(\n</body>)', '  <script src="/js/subscribe.js?v=1"></script>\\1'),
    ], must=False)

# 7) verify no inline handlers remain anywhere
left = []
for p in BASE.rglob("*.html"):
    if "node_modules" in str(p):
        continue
    t = p.read_text(encoding="utf-8")
    if re.search(r'on(click|submit)="', t):
        left.append(str(p.relative_to(BASE)))
if left:
    errors.append("REMAINING inline handlers: " + ", ".join(left))

print("\n=== RESULT ===")
print("\n".join(errors) if errors else "ALL CLEAN — no inline onclick/onsubmit handlers remain.")
sys.exit(1 if errors else 0)
