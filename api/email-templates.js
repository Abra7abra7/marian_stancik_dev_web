// Branded HTML email templates — unified luxury Bronze Neural styling
// Cohesive with marianstancik.dev brand identity

const PROFILE_IMG = 'https://www.marianstancik.dev/profile.webp';

module.exports = {

  // Unified luxury shell for all outgoing branded emails
  _shell(title, contentHtml, persona = 'company') {
    const isCompany = false;
    const headerName = 'Marian Stancik';
    const subtitle = '✦ AI AGENT DEVELOPER · AUTONOMOUS SYSTEMS';
    return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title}</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif; }
body { background: #05050A; color: #F0F0F5; padding: 24px 10px; }
.email-wrapper { max-width: 620px; margin: 0 auto; background: #0D0D18; border: 1px solid rgba(205, 127, 50, 0.3); border-radius: 14px; overflow: hidden; box-shadow: 0 16px 48px rgba(0,0,0,0.7); }
.header { background-color: #12121E; padding: 28px 36px 22px; text-align: left; border-bottom: 2px solid #CD7F32; }
.header .brand-title { font-family: 'Times New Roman', Georgia, serif; font-size: 24px; font-weight: 700; letter-spacing: 5px; color: #E8B86D; text-transform: uppercase; margin-bottom: 4px; }
.header h1 { color: #ffffff; font-size: 15px; font-weight: 600; letter-spacing: 0.5px; margin: 0; }
.header .subtitle { color: #CD7F32; font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }
.header img.avatar { width: 54px; height: 54px; border-radius: 50%; border: 2px solid #CD7F32; object-fit: cover; margin-bottom: 8px; display: inline-block; }
.content { padding: 32px 36px 20px; color: #CBD5E1; font-size: 14px; line-height: 1.7; }
.content h2 { color: #FFFFFF; font-size: 18px; font-weight: 700; margin: 0 0 14px; line-height: 1.3; }
.content h3 { color: #E8B86D; font-size: 14.5px; font-weight: 600; margin: 20px 0 10px; text-transform: uppercase; letter-spacing: 0.8px; }
.content p { margin: 0 0 14px; }
.content ul, .content ol { margin: 0 0 16px; padding-left: 20px; color: #CBD5E1; }
.content li { margin-bottom: 6px; }
.data-table { width: 100%; border-collapse: collapse; margin: 14px 0 22px; font-size: 13px; }
.data-table th { background: #12121E; color: #E8B86D; padding: 10px 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #CD7F32; }
.data-table td { padding: 9px 12px; border-bottom: 1px solid rgba(255,255,255,0.06); color: #F0F0F5; }
.data-table tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
.metric-box { background: #090912; border: 1px solid rgba(205,127,50,0.3); border-radius: 8px; padding: 14px 18px; margin: 16px 0; }
.btn-primary { display: inline-block; background: #CD7F32; color: #FFFFFF !important; text-decoration: none; padding: 12px 26px; border-radius: 6px; font-weight: 700; font-size: 13.5px; letter-spacing: 0.5px; }
.divider { height: 1px; background: rgba(255,255,255,0.08); margin: 0 36px; }
.signature { padding: 20px 36px 26px; background-color: #12121E; color: #94A3B8; font-size: 13px; line-height: 1.6; }
.signature strong { color: #FFFFFF; }
.signature img { width: 46px; height: 46px; border-radius: 50%; border: 2px solid #CD7F32; object-fit: cover; float: left; margin-right: 14px; }
.signature .sig-text { overflow: hidden; }
.footer { background: #08080F; padding: 14px 36px; color: #64748B; font-size: 11px; line-height: 1.5; border-top: 1px solid rgba(255,255,255,0.05); }
@media (max-width: 480px) {
  .header { padding: 22px 20px 18px; }
  .content { padding: 24px 20px; }
  .signature { padding: 16px 20px 22px; }
  .footer { padding: 12px 20px; }
}
</style></head>
<body><div class="email-wrapper">
  <div class="header">
    <img src="${PROFILE_IMG}" alt="${headerName}" class="avatar">
    <h1 style="font-size:17px;">${headerName}</h1>
    <div class="subtitle">${subtitle}</div>
  </div>
  <div class="content">
    <h2>${title}</h2>
    ${contentHtml}
  </div>
  <div class="divider"></div>
  <div class="signature">
    <img src="${PROFILE_IMG}" alt="Marian Stancik">
    <div class="sig-text">
      <strong>Marian Stancik</strong><br>
      <span style="color:#CD7F32; font-weight:600;">✦ AI Agent Developer &amp; Autonomous Systems Builder</span><br>
      Building autonomous systems that run without you.<br>
      <span style="color:#64748B; font-size:11.5px;">marianstancik.dev · marianstancik@agentmail.to</span>
    </div>
  </div>
  <div class="footer">
    <strong>Marián Stančík</strong> — fyzická osoba, podnikateľ (živnostník) · Černákova 2046/8, 977 01 Brezno · IČO: 57068917 · DIČ: 1082585075<br>
    Tento systém využíva asistenciu autonómnych AI agentov podľa čl. 50 EU AI Act.
  </div>
</div></body></html>`;
  },

  // ── NEWSLETTER WELCOME ──
  welcome(name = '', source = 'web') {
    const content = `<p>Ahoj${name ? ' ' + name : ''},</p>
<p>ďakujem za prihlásenie k odberu technických AI noviniek a architektonických analýz.</p>
<h3>Čo pravidelne doručujem do schránky:</h3>
<ul>
  <li><strong style="color:#F0F0F5;">Autonomous Agent Engineering</strong> — 24/7 Hermes runtime, MCP servery, C2 integrácie</li>
  <li><strong style="color:#F0F0F5;">EU AI Act &amp; Compliance</strong> — praktický súlad, čl. 50 označovanie, NIS2 a DORA</li>
  <li><strong style="color:#F0F0F5;">GEO &amp; LLM Discovery</strong> — optimalizácia pre Perplexity, Claude, ChatGPT Search</li>
  <li><strong style="color:#F0F0F5;">Edge AI &amp; Robotics</strong> — stavby taktických UAV, ArduPilot autopilot, Raspberry Pi 5</li>
</ul>
<p style="margin-top:18px;"><a href="https://www.marianstancik.dev/blog" class="btn-primary">Preskúmať najnovšie články</a></p>`;
    return this._shell('Vitaj v komunitnom AI newslettri', content, 'personal');
  },

  // ── ORDER CONFIRMATION ──
  orderConfirmation(name, product, price, website = '') {
    const content = `<p>Ahoj ${name},</p>
<p>ďakujem za tvoju objednávku. Nižšie nájdeš potvrdené zhrnutie a ďalšie kroky realizácie.</p>
<h3>Potvrdená objednávka</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th>Objednaná služba</th><th>Cena</th><th>Status</th></tr>
  <tr><td>${product}</td><td>${price ? '€' + price : 'Na mieru'}</td><td style="color:#10B981; font-weight:700;">✓ Prijatá v systéme</td></tr>
</table>
${website ? `<div class="metric-box"><strong style="color:#E8B86D;">Cieľový web na analýzu:</strong> <a href="${website}" style="color:#10B981; text-decoration:none; font-weight:600;">${website}</a></div>` : ''}
<h3>⚡ Čo sa bude diať ďalej</h3>
<ol>
  <li>Objednávku a cieľovú doménu som zaevidoval v CRM daemone.</li>
  <li>Spúšťam hĺbkové auditné skenovanie do 24 hodín.</li>
  <li>Kompletný exekutívny PDF report doručím do 48 hodín priamo na tvoj e-mail.</li>
  <li>Faktúra vystavená Mariánom Stančíkom (FO) bude doručená samostatne.</li>
</ol>`;
    return this._shell(`Potvrdenie objednávky: ${product}`, content, 'company');
  },

  // ── CONTACT CONFIRMATION ──
  contactConfirmation(name = '', message = '') {
    const content = `<p>Ahoj${name ? ' ' + name : ''},</p>
<p>ďakujem za tvoju správu. Prijal som ju v poriadku a odpovedám do 24 hodín.</p>
${message ? `<blockquote style="border-left:3px solid #CD7F32; padding:12px 18px; margin:16px 0; background:#090912; border-radius:4px; color:#CBD5E1; font-style:italic;">${message}</blockquote>` : ''}
<p>V prípade urgentných požiadaviek ma môžeš kontaktovať priamo cez Telegram alebo odpoveďou na tento e-mail.</p>`;
    return this._shell('Potvrdenie prijatia správy', content, 'personal');
  },

  // ── INVOICE ──
  invoice(name, product, price, invoiceNum, pdfUrl) {
    const content = `<p>Ahoj ${name},</p>
<p>v prílohe tohto e-mailu nájdeš oficiálnu faktúru za <strong>${product}</strong>.</p>
<h3>Faktúra č. ${invoiceNum}</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th>Fakturovaná položka</th><th>Suma</th></tr>
  <tr><td>${product}</td><td style="color:#E8B86D; font-weight:700;">€${price}</td></tr>
</table>
<h3>💳 Platobné údaje (Bankový prevod)</h3>
<table class="data-table" cellpadding="0" cellspacing="0">
  <tr><th style="width:100px;">IBAN</th><td style="font-family:monospace; font-size:14px; color:#10B981;">SK60 1100 0000 0029 4827 4072</td></tr>
  <tr><th>SWIFT / BIC</th><td>TATRSKBX (Tatra banka a.s.)</td></tr>
  <tr><th>Variabilný symbol</th><td style="font-weight:700; color:#E8B86D;">${String(invoiceNum).replace(/[^0-9]/g, '').slice(-6) || '000001'}</td></tr>
</table>
<p style="margin:20px 0 0;"><a href="${pdfUrl}" class="btn-primary">Stiahnuť faktúru PDF</a></p>`;
    return this._shell(`FAKTÚRA č. ${invoiceNum}`, content, 'company');
  },

  // ── AUDIT DELIVERY ──
  auditDelivery(name, website, score, pdfUrl, auditType = 'AI GEO Audit') {
    const content = `<p>Ahoj ${name},</p>
<p>technická analýza domény <strong style="color:#E8B86D;">${website}</strong> bola úspešne dokončená. Nižšie uvádzam zhrnutie kľúčových metrík.</p>
<div class="metric-box">
  <table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr>
      <td>
        <div style="color:#CD7F32; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Namerané Skóre</div>
        <div style="font-size:28px; font-weight:800; color:#FFFFFF; line-height:1.2;">${score} <span style="font-size:14px; color:#64748B;">/ 100</span></div>
      </td>
      <td align="right">
        <span style="display:inline-block; padding:5px 12px; background:rgba(16,185,129,0.15); border:1px solid #10B981; border-radius:6px; font-size:11px; font-weight:700; color:#10B981;">
          AUDIT COMPLETED
        </span>
      </td>
    </tr>
  </table>
</div>
<p>Kompletný exekutívny 2-stranový report s rozpadom pilierov a technickou maticou nájdeš v priloženom PDF súbore.</p>
<p style="margin:18px 0 0;"><a href="${pdfUrl}" class="btn-primary">Stiahnuť kompletný PDF Report</a></p>`;
    return this._shell(`Výsledky auditu: ${website} (${score}/100)`, content, 'company');
  },

  // ── PLAIN TEXT FALLBACKS ──
  welcomeText() {
    return `MARIAN STANCIK — HERMES AGENT\n\nVitaj v newslettri!\nBlog: https://www.marianstancik.dev/blog\n\nS pozdravom, Marian Stancik`;
  },
  orderConfirmationText(name, product, price, website = '', notes = '') {
    return `MARIAN STANCIK — AI AGENT DEVELOPER\n\nAhoj ${name},\nĎakujem za objednávku: ${product} (${price ? '€' + price : 'Na mieru'}).\nWeb: ${website}\n\nS pozdravom, Marian Stancik`;
  },
  contactConfirmationText(name = '', message = '') {
    return `MARIAN STANCIK — HERMES AGENT\n\nAhoj${name ? ' ' + name : ''},\nSprávu som prijal. Odpoviem do 24 hodín.\n\nS pozdravom, Marian Stancik`;
  },
  invoiceText(name, product, price, invoiceNum, pdfUrl) {
    const vs = String(invoiceNum).replace(/[^0-9]/g, '').slice(-6) || '000001';
    return `Marián Stančík (FO)\n\nFAKTÚRA č. ${invoiceNum}\nAhoj ${name},\nfaktúra za ${product} (€${price}).\n\nStiahnuť PDF: ${pdfUrl}\nIBAN: SK60 1100 0000 0029 4827 4072\nBIC: TATRSKBX (Tatra banka a.s.)\nVS: ${vs}\n\n--\nMarián Stančík (marianstancik.dev)`;
  },
  auditDeliveryText(name, website, score, pdfUrl) {
    return `MARIAN STANCIK — AI AUDIT REPORT\n\nAhoj ${name},\naudit pre ${website} je pripravený.\nSkóre: ${score}/100\nStiahnuť PDF: ${pdfUrl}\n\n--\nMarian Stancik`;
  }
};