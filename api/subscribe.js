// Vercel serverless — Lead & Order capture → AgentMail (dedicated email templates + admin alerts)
export default async function handler(req, res) {
  try {
    res.setHeader('Access-Control-Allow-Origin', 'https://www.marianstancik.dev');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

    const apiKey = process.env.AGENTMAIL_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

    const body = typeof req.body === 'object' ? req.body : {};
    const email = (body.email || '').trim().toLowerCase();
    const name = body.name || '';
    const source = body.source || 'web';
    const message = body.message || '';
    const product = body.product || '';
    const price = body.price || '';
    const website = body.website || '';
    const notes = body.notes || '';

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email' });

    // ── SAFETY GUARD: Test/pre-commit requests DON'T send real emails ──
    const isTest = source.startsWith('pre-commit') || email.endsWith('.local');
    const isOrder = Boolean(product) || source === 'product_order' || source === 'stripe_checkout_intent';
    const isContact = Boolean(message) || source === 'contact_form';

    if (isTest && !isOrder && !isContact) {
      return res.status(200).json({ status: 'ok', type: 'test-skip', email, note: 'Test request — email not sent' });
    }

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = now.toTimeString().split(' ')[0];

    const url = 'https://mcp.agentmail.to/mcp';
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'x-api-key': apiKey
    };

    // Helper: MCP session → send email
    async function sendEmail(to, subject, text) {
      const initBody = JSON.stringify({
        jsonrpc: '2.0', id: '1', method: 'initialize',
        params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'hermes-crm', version: '1.0' } }
      });
      const initRes = await fetch(url, { method: 'POST', headers, body: initBody });
      const initText = await initRes.text();
      const sessionMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
      const sessionId = sessionMatch ? sessionMatch[1] : null;
      const msgHeaders = { ...headers };
      if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;

      await fetch(url, { method: 'POST', headers: msgHeaders, body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) });

      const sendBody = JSON.stringify({
        jsonrpc: '2.0', id: '2', method: 'tools/call',
        params: {
          name: 'send_message',
          arguments: { inboxId: 'marianstancik@agentmail.to', to: [to], subject, text }
        }
      });
      const msgRes = await fetch(url, { method: 'POST', headers: msgHeaders, body: sendBody });
      const msgText = await msgRes.text();
      if (msgText.includes('"isError":true')) {
        const errMsg = msgText.match(/"message"\s*:\s*"([^"]+)"/)?.[1] || 'Unknown error';
        throw new Error(`AgentMail: ${errMsg}`);
      }
    }

    // ── CRM: forward to Google Sheets webhook ──
    const CRM_URL = process.env.CRM_WEBHOOK_URL || 'https://api.marianstancik.dev/crm/';
    const CRM_KEY = process.env.CRM_WEBHOOK_KEY || '';
    async function crmToSheets(entryType, data) {
      if (!CRM_KEY) return;
      try {
        await fetch(CRM_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CRM-Key': CRM_KEY },
          body: JSON.stringify({ type: entryType, ...data }),
        });
      } catch (e) {
        console.error('CRM webhook error:', e.message);
      }
    }

    const sep = '─'.repeat(44);

    // ─────────────────────────────────────────────────────────────
    // TEMPLATE 1: PRODUCT / AUDIT ORDER
    // ─────────────────────────────────────────────────────────────
    if (isOrder) {
      const prodName = product || 'AI GEO / Web Readiness Audit';
      const userSubject = `✦ Potvrdenie objednávky: ${prodName} — Marian Stancik`;
      const userText = `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
${sep}

Ahoj,

ďakujem za tvoju objednávku: ${prodName}.

📋 ZHRNUTIE OBJEDNÁVKY:
• Služba / Produkt: ${prodName}
• Suma: ${price ? '€' + price : 'Na mieru'}
• Webstránka na audit / automatizáciu: ${website || 'Zadaj prosím v odpovedi'}
• E-mail pre doručenie: ${email}
${notes ? `• Poznámka: ${notes}\n` : ''}
⚡ ČO SA BUDE DIAŤ ĎALEJ:
1. Tvoju objednávku a zadanú doménu som zaevidoval v systéme.
2. Hermes Agent a ja spúšťame technickú analýzu / prípravu do 24 hodín.
3. Kompletný výsledný report s konkrétnymi kódovými odporúčaniami ti doručím priamo na tento e-mail do 48 hodín.
4. Ak potrebuješ vystaviť faktúru na firmu (IČO / DIČ / IČ DPH), stačí odpovedať na tento e-mail s fakturačnými údajmi.

V prípade akýchkoľvek otázok stačí priamo odpovedať na túto správu.

S pozdravom,

Marian Stancik
AI Engineer & Autonomous Systems Builder
marianstancik@agentmail.to · https://www.marianstancik.dev
`;

      await sendEmail(email, userSubject, userText).catch(e => console.error('Order user email failed:', e.message));

      const adminNotif = `🛒 NOVÁ OBJEDNÁVKA PRODUKTU — marianstancik.dev
${sep}
Dátum:   ${dateStr} ${timeStr}
Produkt: ${prodName} (${price ? '€' + price : 'N/A'})
Email:   ${email}
Web:     ${website || 'N/A'}
Poznámka: ${notes || 'Žiadna'}
Zdroj:   ${source}
Status:  Potvrdenie odoslané klientovi ✅
${sep}`;

      await sendEmail('marianstancik@agentmail.to', `[OBJEDNÁVKA] ${prodName} — ${email}`, adminNotif).catch(e => console.error('Order admin notif failed:', e.message));

      await crmToSheets('order', { email, name, product, price, website, notes, source, status: 'new' }).catch(e => console.error('CRM order failed:', e.message));

      return res.status(200).json({ status: 'ok', type: 'order', email, product: prodName });
    }

    // ─────────────────────────────────────────────────────────────
    // TEMPLATE 2: CONTACT FORM MESSAGE
    // ─────────────────────────────────────────────────────────────
    if (isContact) {
      const userSubject = `✦ Potvrdenie prijatia správy — Marian Stancik`;
      const userText = `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
${sep}

Ahoj ${name ? name : ''},

ďakujem za tvoju správu a záujem o spoluprácu!

Správu som bezpečne prijal. Zvyčajne odpovedám do 24 hodín.

📋 PREHĽAD ODOSLANEJ SPRÁVY:
${message ? `„${message}“\n` : ''}
Ak ide o urgentný projekt alebo máš doplňujúce podklady, môžeš odpovedať priamo na tento e-mail.

S pozdravom,

Marian Stancik
AI Engineer & Autonomous Systems Builder
marianstancik@agentmail.to · https://www.marianstancik.dev
`;

      await sendEmail(email, userSubject, userText).catch(e => console.error('Contact user email failed:', e.message));

      const adminNotif = `💬 NOVÁ SPRÁVA Z WEBU — marianstancik.dev
${sep}
Dátum:   ${dateStr} ${timeStr}
Od:      ${name || 'Nezadané'} <${email}>
Správa:  ${message || 'Prázdna'}
Zdroj:   ${source}
${sep}`;

      await sendEmail('marianstancik@agentmail.to', `[SPRÁVA] ${name || email}`, adminNotif).catch(e => console.error('Contact admin notif failed:', e.message));

      await crmToSheets('contact', { email, name, message, source }).catch(e => console.error('CRM contact failed:', e.message));

      return res.status(200).json({ status: 'ok', type: 'contact', email });
    }

    // ─────────────────────────────────────────────────────────────
    // TEMPLATE 3: NEWSLETTER WELCOME
    // ─────────────────────────────────────────────────────────────
    const userSubject = `✦ Vitaj v newslettri Mariana Stancika!`;
    const userText = `✦ MARIAN STANCIK — AI AGENTS & ENGINEERING
https://www.marianstancik.dev
${sep}

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
marianstancik@agentmail.to · https://www.marianstancik.dev
`;

    await sendEmail(email, userSubject, userText).catch(e => console.error('Newsletter user email failed:', e.message));

    const adminNotif = `📰 NOVÝ ODBERATEĽ NEWSLETTRU — marianstancik.dev
${sep}
Dátum:   ${dateStr} ${timeStr}
Email:   ${email}
Zdroj:   ${source}
${sep}`;

    await sendEmail('marianstancik@agentmail.to', `[NEWSLETTER] ${email}`, adminNotif).catch(e => console.error('Newsletter admin notif failed:', e.message));

          await crmToSheets('lead', { email, name, source, status: 'active', gdpr: 'yes' }).catch(e => console.error('CRM lead failed:', e.message));

      return res.status(200).json({ status: 'ok', type: 'newsletter', email, welcome_sent: true });

  } catch (e) {
    console.error('API error:', e.message);
    return res.status(500).json({ error: e.message });
  }
}
