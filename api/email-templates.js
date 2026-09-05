// Branded HTML email templates matching ASCENTIA bronze-neural design
// JS version for Vercel serverless (subscribe.js)

const BRAND = {
  bg: '#08080F',
  card: '#0D0D18',
  cardBorder: 'rgba(255,255,255,0.06)',
  bronze: '#CD7F32',
  gold: '#E8B86D',
  text: '#F0F0F5',
  textMuted: '#8888A0',
  textDark: '#08080F',
};

function header(title) {
  return `<table cellpadding="0" cellspacing="0" style="width:100%;background:${BRAND.bg};padding:20px 0;">
<tr><td align="center" style="padding:30px 20px;">
<div style="max-width:560px;background:${BRAND.card};border:1px solid ${BRAND.cardBorder};border-radius:12px;padding:30px;">
<table cellpadding="0" cellspacing="0" style="width:100%;">
<tr><td style="border-bottom:1px solid ${BRAND.bronze}20;padding-bottom:20px;">
<span style="font-size:22px;color:${BRAND.bronze};">✦</span>
<span style="font-size:20px;color:${BRAND.text};font-weight:600;margin-left:8px;">marian<span style="color:${BRAND.bronze};">stancik</span><span style="color:${BRAND.textMuted};">.dev</span></span>
</td></tr>
<tr><td style="padding:20px 0;">
<h1 style="color:${BRAND.text};font-size:22px;font-weight:600;margin:0 0 15px 0;">${title}</h1>`;
}

function footer() {
  return `</td></tr>
<tr><td style="border-top:1px solid ${BRAND.bronze}20;padding-top:20px;">
<p style="color:${BRAND.textMuted};font-size:12px;margin:0 0 5px 0;">
ASCENTIA s.r.o. · Klincová 37/B, 821 08 Bratislava · IČO: 51858959<br>
marianstancik.dev · marianstancik@agentmail.to</p>
<p style="color:${BRAND.textMuted};font-size:11px;margin:0;">
Tento email bol odoslaný na základe tvojej aktivity na webe. Odhlásiť sa môžeš odpoveďou.</p>
</td></tr></table></div></td></tr></table>`;
}

function button(text, url) {
  return `<table cellpadding="0" cellspacing="0" style="margin:20px auto;">
<tr><td align="center" style="background:${BRAND.bronze};border-radius:6px;padding:12px 28px;">
<a href="${url}" style="color:${BRAND.textDark};text-decoration:none;font-size:14px;font-weight:600;">${text}</a>
</td></tr></table>`;
}

function row(label, value) {
  return `<tr><td style="padding:4px 0;color:${BRAND.textMuted};font-size:12px;width:120px;">${label}</td>
<td style="padding:4px 0;color:${BRAND.text};font-size:13px;">${value}</td></tr>`;
}

function wrap(bodyHtml) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body,table,td,p,a,li,blockquote{-webkit-font-smoothing:antialiased;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}</style>
</head><body style="margin:0;padding:0;background:${BRAND.bg};">
${bodyHtml}
</body></html>`;
}

module.exports = {

  // ── NEWSLETTER WELCOME ──
  welcome(name = '', source = 'web') {
    const body = header('Vitaj v mojom newslettri! 👋');
    return wrap(body + `<p style="color:${BRAND.text};font-size:14px;line-height:1.6;">
Ahoj${name ? ' ' + name : ''},<br><br>
Ďakujem za prihlásenie. Posielam ti pravidelné novinky z AI sveta bez zbytočného šumu.</p>
<h3 style="color:${BRAND.bronze};font-size:14px;font-weight:600;margin:20px 0 10px 0;">Čo môžeš očakávať</h3>
<table cellpadding="0" cellspacing="0" style="width:100%;margin:10px 0;">
<tr><td style="padding:6px 0;color:${BRAND.text};font-size:13px;">🤖 AI Agent Systems — multi-agent orchestration v praxi</td></tr>
<tr><td style="padding:6px 0;color:${BRAND.text};font-size:13px;">🚁 Edge AI na UAV — počítačové videnie v reálnom čase</td></tr>
<tr><td style="padding:6px 0;color:${BRAND.text};font-size:13px;">⚖️ EU AI Act & Compliance — praktické zhrnutia regulácií</td></tr>
<tr><td style="padding:6px 0;color:${BRAND.text};font-size:13px;">🔧 Building in Public — kódové ukážky a architektúry</td></tr>
</table>` +
    button('Pozri blog →', 'https://marianstancik.dev/blog') +
    footer());
  },

  // ── ORDER CONFIRMATION ──
  orderConfirmation(name, product, price, website = '') {
    const title = `✧ Potvrdenie objednávky: ${product}`;
    const body = header(title);
    return wrap(body + `<p style="color:${BRAND.text};font-size:14px;line-height:1.6;">
Ahoj ${name},<br><br>
ďakujem za tvoju objednávku. Nižšie nájdeš zhrnutie.</p>
<table cellpadding="0" cellspacing="0" style="width:100%;background:${BRAND.bg};border-radius:8px;margin:15px 0;padding:15px;">
${row('Služba:', product)}
${row('Suma:', price ? '€' + price : 'Na mieru')}
${row('Web:', website || 'Zadaj prosím v odpovedi')}
${row('Email:', 'marianstancik@agentmail.to')}
</table>
<h3 style="color:${BRAND.bronze};font-size:14px;font-weight:600;margin:20px 0 10px 0;">⚡ Čo bude ďalej</h3>
<ol style="color:${BRAND.text};font-size:13px;padding-left:20px;margin:10px 0;">
<li>Objednávku a doménu som zaevidoval v systéme</li>
<li>Spúšťam technickú analýzu do 24 hodín</li>
<li>Kompletný report doručím do 48 hodín</li>
<li>Faktúra bude doručená samostatne</li>
</ol>` +
    footer());
  },

  // ── CONTACT CONFIRMATION ──
  contactConfirmation(name = '', message = '') {
    const body = header('✧ Potvrdenie prijatia správy');
    return wrap(body + `<p style="color:${BRAND.text};font-size:14px;line-height:1.6;">
Ahoj${name ? ' ' + name : ''},<br><br>
ďakujem za tvoju správu. Prijal som ju a zvyčajne odpovedám do 24 hodín.${message ? `</p>
<blockquote style="border-left:3px solid ${BRAND.bronze};padding:10px 15px;margin:15px 0;color:${BRAND.textMuted};font-size:13px;font-style:italic;">${message}</blockquote>` : '</p>'}
<p style="color:${BRAND.text};font-size:13px;">
Ak ide o urgentný projekt, pokojne mi napíš priamo.</p>` +
    footer());
  },

  // ── PLAIN TEXT variants (fallback) ──
  welcomeText() {
    return `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
────────────────────────────────────────────

Vitaj v mojom newslettri! 👋

Ďakujem za prihlásenie k odberu noviniek zo sveta autonómnych AI agentov, edge robotiky a legal-by-design compliance.

ČO MÔŽEŠ OČAKÁVAŤ:
• AI Agent Systems — reálne poznatky z prevádzky Hermes Agent, MCP serverov a multi-LLM orchestrácie
• UAV & Edge AI — hardvérové stavby, ArduPilot, Raspberry Pi 5 a computer vision
• EU AI Act & Compliance — praktické zhrnutia regulácií a audity pripravenosti
• Building in Public — konkrétne čísla, kódové ukážky a architektúry

Môj web: https://www.marianstancik.dev
X (Twitter): https://x.com/marian_s_ai
GitHub: https://github.com/Abra7abra7

Odhlásiť sa môžeš kedykoľvek odpoveďou na tento e-mail.

S pozdravom,
Marian Stancik
AI Engineer & UAV Builder
marianstancik@agentmail.to · https://www.marianstancik.dev`;
  },

  orderConfirmationText(name, product, price, website = '', notes = '') {
    return `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
────────────────────────────────────────────

Ahoj ${name},

ďakujem za tvoju objednávku: ${product}.

📋 ZHRNUTIE OBJEDNÁVKY:
• Služba / Produkt: ${product}
• Suma: ${price ? '€' + price : 'Na mieru'}
• Webstránka na audit / automatizáciu: ${website || 'Zadaj prosím v odpovedi'}
• E-mail pre doručenie: ${email}
${notes ? `• Poznámka: ${notes}\n` : ''}
⚡ ČO SA BUDE DIAŤ ĎALEJ:
1. Tvoju objednávku a zadanú doménu som zaevidoval v systéme.
2. Hermes Agent a ja spúšťame technickú analýzu / prípravu do 24 hodín.
3. Kompletný výsledný report s konkrétnymi odporúčaniami ti doručím na tento e-mail do 48 hodín.
4. Ak potrebuješ vystaviť faktúru na firmu (IČO / DIČ), stačí odpovedať s fakturačnými údajmi.

V prípade akýchkoľvek otázok stačí priamo odpovedať na túto správu.

S pozdravom,
Marian Stancik
AI Engineer & Autonomous Systems Builder
marianstancik@agentmail.to · https://www.marianstancik.dev`;
  },

  contactConfirmationText(name = '', message = '') {
    return `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
────────────────────────────────────────────

Ahoj ${name ? name : ''},

ďakujem za tvoju správu a záujem o spoluprácu!

Správu som bezpečne prijal. Zvyčajne odpovedám do 24 hodín.

📋 PREHĽAD ODOSLANEJ SPRÁVY:
${message ? `"${message}"\n` : ''}Ak ide o urgentný projekt alebo máš doplňujúce podklady, môžeš odpovedať priamo na tento e-mail.

S pozdravom,
Marian Stancik
AI Engineer & Autonomous Systems Builder
marianstancik@agentmail.to · https://www.marianstancik.dev`;
  },
};