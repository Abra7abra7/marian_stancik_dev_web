// Vercel serverless — CRM email dispatcher (triggered by VPS webhook)
// Reads pending actions, sends branded HTML emails via AgentMail
import emailTpl from '../email-templates.js';

const AGENTMAIL_API_KEY = process.env.AGENTMAIL_API_KEY;
const INVOICE_BASE = 'https://www.marianstancik.dev/api/invoice/';
const INBOX_PERSONAL = 'marianstancik@agentmail.to';
const INBOX_COMPANY = 'ascentia@agentmail.to';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  
  const { actions } = req.body;
  if (!Array.isArray(actions) || actions.length === 0) {
    return res.status(400).json({ error: 'Missing actions array' });
  }
  
  const results = [];
  
  for (const action of actions) {
    try {
      const { reason, email, name, product, price, invoice_id } = action;
      
      // ── Invoice: branded HTML via emailTpl, from ASCENTIA inbox ──
      if (reason === 'invoice_sent' && invoice_id) {
        const pdfUrl = `${INVOICE_BASE}${invoice_id}`;
        const html = emailTpl.invoice(name || email, product || 'AI služba', price || '0', invoice_id, pdfUrl);
        const text = `✧ FAKTÚRA č. ${invoice_id}\n\nAhoj ${name || email},\nnáš systém vygeneroval faktúru za ${product || 'AI službu'}.\n\nStiahnuť PDF: ${pdfUrl}\n\nIBAN: SK78 1100 0000 0027 0129 7133\nBIC: FIOZSKBAXXX\n\n--\nASCENTIA s.r.o.`;
        
        const sent = await sendAgentMail(email, `✧ FAKTÚRA č. ${invoice_id} — ${product || 'AI služba'}`, text, html, INBOX_COMPANY);
        results.push({ email, action: 'invoice_sent', status: sent ? 'ok' : 'error' });
      }
      
      // ── Payment reminder: plain, from ASCENTIA inbox ──
      else if (reason === 'payment_reminder') {
        const text = `Ahoj ${name || email},\n\npripomíname, že faktúra za ${product || 'službu'} čaká na úhradu.\n\nIBAN: SK78 1100 0000 0027 0129 7133\nBIC: FIOZSKBAXXX\n\n--\nASCENTIA s.r.o.`;
        const sent = await sendAgentMail(email, '✧ Pripomienka úhrady faktúry', text, null, INBOX_COMPANY);
        results.push({ email, action: 'payment_reminder', status: sent ? 'ok' : 'error' });
      }
      
      // ── Follow-up: from personal inbox ──
      else if (reason === 'followup_7d') {
        const html = emailTpl.followup();
        const text = `Ahoj,\n\nodkedy si sa prihlásil k odberu, pribudlo niekoľko nových článkov:\n\n• Hermes Agent — autonómna AI na VPS\n• EU AI Act — praktický sprievodca compliance\n• Edge AI na drone — počítačové videnie\n\nBlog: https://marianstancik.dev/blog\n\n--\nMarian Stancik`;
        const sent = await sendAgentMail(email, '✧ Čo sa udialo za posledný týždeň', text, html, INBOX_PERSONAL);
        results.push({ email, action: 'followup_7d', status: sent ? 'ok' : 'error' });
      }
      
    } catch (e) {
      results.push({ action: action?.reason || 'unknown', error: e.message });
    }
  }
  
  return res.status(200).json({ processed: results.length, results });
}

async function sendAgentMail(to, subject, text, html, inboxId = INBOX_PERSONAL) {
  const url = 'https://mcp.agentmail.to/mcp';
  const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'x-api-key': AGENTMAIL_API_KEY };
  
  const initBody = JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'hermes-crm', version: '1.0' } } });
  const initRes = await fetch(url, { method: 'POST', headers, body: initBody });
  const initText = await initRes.text();
  const sessionMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
  const sessionId = sessionMatch ? sessionMatch[1] : null;
  const msgHeaders = { ...headers };
  if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;
  
  await fetch(url, { method: 'POST', headers: msgHeaders, body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) });
  
  const args = { inboxId, to: [to], subject, text };
  if (html) args.html = html;
  
  const sendBody = JSON.stringify({ jsonrpc: '2.0', id: '2', method: 'tools/call', params: { name: 'send_message', arguments: args } });
  const msgRes = await fetch(url, { method: 'POST', headers: msgHeaders, body: sendBody });
  return msgRes.ok;
}