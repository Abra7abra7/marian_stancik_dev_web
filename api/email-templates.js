// Branded HTML email templates — uniform design with profile photo (report style)
// Design: navy gradient header + round profile photo + bronze accents

const PROFILE_IMG = 'https://www.marianstancik.dev/profile.webp';

module.exports = {

  // ── Generate unified email shell ──
  _shell(title, contentHtml) {
    return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif; }
body { background: #f0f0f5; }
.email-wrapper { max-width: 600px; margin: 0 auto; background: #ffffff; }
.header { background: linear-gradient(135deg, #002147 0%, #1a3a5c 100%); padding: 32px 40px 24px; text-align: center; }
.header img { width: 64px; height: 64px; border-radius: 50%; border: 3px solid #CD7F32; object-fit: cover; margin-bottom: 8px; }
.header h1 { color: #ffffff; font-size: 20px; font-weight: 600; letter-spacing: 0.3px; }
.header .subtitle { color: #CD7F32; font-size: 13px; font-weight: 400; letter-spacing: 2px; margin-top: 2px; }
.content { padding: 32px 40px; color: #2d2d2d; font-size: 14px; line-height: 1.7; }
.content h2 { color: #002147; font-size: 18px; font-weight: 600; margin: 24px 0 12px; padding-bottom: 6px; border-bottom: 1px solid #e0e0e0; }
.content h2:first-child { margin-top: 0; }
.content h3 { color: #002147; font-size: 15px; font-weight: 600; margin: 16px 0 8px; }
.content p { margin: 0 0 14px; }
.content ul { margin: 0 0 14px; padding-left: 20px; }
.content li { margin-bottom: 6px; }
.divider { height: 3px; background: #CD7F32; margin: 0 40px; }
.signature { padding: 20px 40px 28px; color: #555; font-size: 13px; line-height: 1.6; }
.signature strong { color: #002147; }
.signature img { width: 48px; height: 48px; border-radius: 50%; border: 2px solid #CD7F32; object-fit: cover; float: left; margin-right: 12px; }
.signature .sig-text { overflow: hidden; }
.footer { background: #f8f8f8; padding: 16px 40px; color: #999; font-size: 11px; line-height: 1.5; text-align: left; }
.footer strong { color: #777; }
.data-table { width: 100%; border-collapse: collapse; margin: 12px 0 20px; font-size: 13px; }
.data-table th { background: #002147; color: #fff; padding: 8px 12px; text-align: left; font-weight: 500; }
.data-table td { padding: 8px 12px; border-bottom: 1px solid #eee; }
.data-table tr:nth-child(even) td { background: #fafafe; }
@media (max-width: 480px) {
  .header { padding: 24px 20px 18px; }
  .content { padding: 24px 20px; }
  .divider { margin: 0 20px; }
  .signature { padding: 16px 20px 24px; }
  .footer { padding: 12px 20px; }
}
</style></head>
<body><div class="email-wrapper">
  <div class="header">
    <img src="${PROFILE_IMG}" alt="Marian Stancik">
    <h1>Marian Stancik</h1>
    <div class="subtitle">✦ HERMES AGENT</div>
  </div>
  <div class="content">
    <h2>${title}</h2>
    ${contentHtml}
  </div>
  <div class="divider"></div>
  <div class="signature">
    <img src="${PROFILE_IMG}" alt="">
    <div class="sig-text">
      <strong>Marian Stancik</strong><br>
      ✦ Hermes Agent — ASCENTIA s.r.o.<br>
      Building systems that run without you.<br>
      <span style="color:#999;font-size:11px;">Reply to this email or DM me on Telegram</span>
    </div>
  </div>
  <div class="footer">
    <strong>ASCENTIA s.r.o.</strong> • Klincová 37/B, 821 08 Bratislava, Slovakia<br>
    IČO: 51858959 • DIČ: 2120816071<br>
    marianstancik.dev
  </div>
</div></body></html>`;
  },

  // ── NEWSLETTER WELCOME ──
  welcome(name = '', source = 'web') {
    const content = `<p>Ahoj${name ? ' ' + name : ''},</p>
<p>Ďakujem za prihlásenie k odberu noviniek. Posielam ti pravidelné súhrny z AI sveta bez zbytočného šumu.</p>
<h3>Čo môžeš očakávať</h3>
<ul>
  <li><strong>AI Agent Systems</strong> — multi-agent orchestration, MCP servery a Hermes v praxi</li>
  <li><strong>UAV &amp; Edge AI</strong> — hardvérové stavby, počítačové videnie v reálnom čase</li>
  <li><strong>EU AI Act &amp; Compliance</strong> — praktické zhrnutia regulácií</li>
  <li><strong>Building in Public</strong> — kódové ukážky a architektúry</li>
</ul>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr>
    <td style="padding:12px; text-align:center;"><div style="font-size:22px; font-weight:700; color:#002147;">Blog</div><div style="font-size:11px; color:#8888a0; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">marianstancik.dev</div></td>
    <td style="padding:12px; text-align:center;"><div style="font-size:22px; font-weight:700; color:#002147;">GitHub</div><div style="font-size:11px; color:#8888a0; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">Abra7abra7</div></td>
    <td style="padding:12px; text-align:center;"><div style="font-size:22px; font-weight:700; color:#002147;">Telegram</div><div style="font-size:11px; color:#8888a0; text-transform:uppercase; letter-spacing:1px; margin-top:2px;">DM</div></td>
  </tr>
</table>
<p style="margin-top:16px;">👉 <a href="https://marianstancik.dev/blog" style="color:#CD7F32; font-weight:600;">Pozri najnovšie články</a></p>`;
    return this._shell('Vitaj v newslettri', content);
  },

  // ── ORDER CONFIRMATION ──
  orderConfirmation(name, product, price, website = '') {
    const content = `<p>Ahoj ${name},</p>
<p>ďakujem za tvoju objednávku. Nižšie nájdeš zhrnutie a ďalšie kroky.</p>
<h3>Objednávka</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th>Služba</th><th>Suma</th><th>Stav</th></tr>
  <tr><td>${product}</td><td>${price ? '€' + price : 'Na mieru'}</td><td style="color:#CD7F32;">✓ Prijatá</td></tr>
</table>
<h3>⚡ Čo bude ďalej</h3>
<ol>
  <li>Objednávku a doménu som zaevidoval v systéme</li>
  <li>Spúšťam technickú analýzu do 24 hodín</li>
  <li>Kompletný report doručím do 48 hodín</li>
  <li>Faktúra bude doručená samostatne emailom</li>
</ol>
${website ? `<p>Webstránka na analýzu: <a href="${website}" style="color:#CD7F32;">${website}</a></p>` : ''}`;
    return this._shell(`✧ Potvrdenie objednávky: ${product}`, content);
  },

  // ── CONTACT CONFIRMATION ──
  contactConfirmation(name = '', message = '') {
    const content = `<p>Ahoj${name ? ' ' + name : ''},</p>
<p>ďakujem za tvoju správu. Prijal som ju a zvyčajne odpovedám do 24 hodín.</p>
${message ? `<blockquote style="border-left:3px solid #CD7F32; padding:10px 15px; margin:15px 0; color:#555; font-style:italic;">${message}</blockquote>` : ''}
<p>Ak ide o urgentný projekt, kľudne mi napíš priamo.</p>`;
    return this._shell('✧ Potvrdenie prijatia správy', content);
  },

  // ── INVOICE ──
  invoice(name, product, price, invoiceNum, pdfUrl) {
    const content = `<p>Ahoj ${name},</p>
<p>v prílohe tohto emailu nájdeš faktúru za objednávku <strong>${product}</strong>.</p>
<h3>Faktúra ${invoiceNum}</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th>Položka</th><th>Suma</th></tr>
  <tr><td>${product}</td><td>€${price}</td></tr>
</table>
<h3>💳 Platobné údaje</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th style="width:80px;">IBAN</th><td>SK78 1100 0000 0027 0129 7133</td></tr>
  <tr><th>BIC</th><td>FIOZSKBAXXX</td></tr>
  <tr><th>VS</th><td>${String(invoiceNum).replace(/[^0-9]/g, '').slice(-6) || '000001'}</td></tr>
</table>
<p style="margin-top:16px;">Po pripísaní platby spustíme analýzu do 24 hodín.</p>
<p style="margin:16px 0 0;"><a href="${pdfUrl}" style="display:inline-block; background:#CD7F32; color:#fff; text-decoration:none; padding:12px 28px; border-radius:6px; font-weight:600; font-size:14px;">Stiahnuť faktúru PDF</a></p>`;
    return this._shell(`✧ FAKTÚRA č. ${invoiceNum}`, content);
  },

  // ── FOLLOW-UP ──
  followup() {
    const content = `<p>Ahoj,</p>
<p>odkedy si sa prihlásil k odberu, pribudlo niekoľko nových článkov na blogu:</p>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th style="width:30px;"></th><th>Článok</th></tr>
  <tr><td>→</td><td><a href="https://marianstancik.dev/blog" style="color:#002147; text-decoration:none; font-weight:500;">Hermes Agent — autonómna AI na VPS s MCP servermi</a></td></tr>
  <tr><td>→</td><td><a href="https://marianstancik.dev/blog" style="color:#002147; text-decoration:none; font-weight:500;">EU AI Act — praktický sprievodca compliance</a></td></tr>
  <tr><td>→</td><td><a href="https://marianstancik.dev/blog" style="color:#002147; text-decoration:none; font-weight:500;">Edge AI na drone — počítačové videnie v reálnom čase</a></td></tr>
</table>
<p>👉 <a href="https://marianstancik.dev/blog" style="color:#CD7F32; font-weight:600;">Pozri celý blog</a></p>`;
    return this._shell('✧ Čo sa udialo za posledný týždeň', content);
  },

  // ── PAYMENT REMINDER ──
  paymentReminder(name, product) {
    const content = `<p>Ahoj ${name},</p>
<p>pripomínam, že faktúra za <strong>${product}</strong> čaká na úhradu.</p>
<h3>Platobné údaje</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th style="width:80px;">IBAN</th><td>SK78 1100 0000 0027 0129 7133</td></tr>
  <tr><th>BIC</th><td>FIOZSKBAXXX</td></tr>
</table>
<p>Po pripísaní platby spustíme technickú analýzu do 24 hodín.</p>`;
    return this._shell('✧ Pripomienka úhrady faktúry', content);
  },

  // ── PLAIN TEXT FALLBACKS ──
  welcomeText(name = '') {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

Vitaj v newslettri! 👋

Ďakujem za prihlásenie. Posielam ti pravidelné novinky z AI sveta bez zbytočného šumu.

ČO MÔŽEŠ OČAKÁVAŤ:
• AI Agent Systems — multi-agent orchestration, MCP servery
• UAV & Edge AI — hardvérové stavby, computer vision
• EU AI Act & Compliance — praktické zhrnutia regulácií
• Building in Public — kódové ukážky a architektúry

Blog: https://marianstancik.dev/blog
GitHub: https://github.com/Abra7abra7

S pozdravom,
Marian Stancik — Hermes Agent`;
  },

  orderConfirmationText(name, product, price, website = '', notes = '') {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

Ahoj ${name},

Ďakujem za objednávku: ${product} (${price ? '€' + price : 'Na mieru'}).

ĎALŠIE KROKY:
1. Objednávka zaevidovaná
2. Technická analýza do 24h
3. Report do 48h
4. Faktúra samostatne

Web: ${website || 'Zadaj v odpovedi'}
${notes ? `Poznámka: ${notes}` : ''}

S pozdravom,
Marian Stancik — Hermes Agent`;
  },

  contactConfirmationText(name = '', message = '') {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

Ahoj${name ? ' ' + name : ''},

Správu som prijal. Odpovedám do 24 hodín.
${message ? `\nTvoja správa: "${message}"` : ''}

S pozdravom,
Marian Stancik — Hermes Agent`;
  },

  invoiceText(name, product, price, invoiceNum, pdfUrl) {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

FAKTÚRA č. ${invoiceNum}

Ahoj ${name},

Faktúra za ${product} (€${price}).

Stiahnuť PDF: ${pdfUrl}

Platobné údaje:
IBAN: SK78 1100 0000 0027 0129 7133
BIC: FIOZSKBAXXX
VS: ${String(invoiceNum).replace(/[^0-9]/g, '').slice(-6) || '000001'}

S pozdravom,
Marian Stancik — Hermes Agent`;
  },

  followupText() {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

Ahoj,

odkedy si sa prihlásil, pribudli nové články:

• Hermes Agent — autonómna AI na VPS
• EU AI Act — praktický sprievodca compliance
• Edge AI na drone — počítačové videnie

Blog: https://marianstancik.dev/blog

S pozdravom,
Marian Stancik — Hermes Agent`;
  },

  paymentReminderText(name, product) {
    return `MARIAN STANCIK — HERMES AGENT
─────────────────────────

Ahoj ${name},

Pripomínam úhradu faktúry za ${product}.

IBAN: SK78 1100 0000 0027 0129 7133
BIC: FIOZSKBAXXX

S pozdravom,
Marian Stancik — Hermes Agent`;
  },
};