// Vercel serverless — CRM email dispatcher (triggered by VPS webhook)
// Reads pending actions, sends branded HTML emails via AgentMail
import emailTpl from '../email-templates.js';

const AGENTMAIL_API_KEY = process.env.AGENTMAIL_API_KEY;
const INVOICE_BASE = 'https://marianstancik.dev/api/invoice/';
const INBOX = 'marianstancik@agentmail.to';

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
      
      if (reason === 'invoice_sent' && invoice_id) {
        const pdfUrl = `${INVOICE_BASE}${invoice_id}`;
        const subject = `✧ FAKTÚRA č. ${invoice_id} — ${product || 'AI služba'}`;
        
        const html = `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body,table,td,p,a{-webkit-font-smoothing:antialiased;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;}</style>
</head><body style="margin:0;padding:0;background:#08080F;">
<table cellpadding="0" cellspacing="0" style="width:100%;background:#08080F;padding:20px 0;">
<tr><td align="center" style="padding:30px 20px;">
<div style="max-width:560px;background:#0D0D18;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:30px;">
<table cellpadding="0" cellspacing="0" style="width:100%;">
<tr><td style="border-bottom:1px solid #CD7F3220;padding-bottom:20px;">
<span style="font-size:22px;color:#CD7F32;">✦</span>
<span style="font-size:20px;color:#F0F0F5;font-weight:600;margin-left:8px;">marian<span style="color:#CD7F32;">stancik</span><span style="color:#8888A0;">.dev</span></span>
</td></tr>
<tr><td style="padding:20px 0;">
<h1 style="color:#F0F0F5;font-size:22px;font-weight:600;margin:0 0 15px 0;">✧ FAKTÚRA č. ${invoice_id}</h1>
<p style="color:#F0F0F5;font-size:14px;line-height:1.6;">Ahoj ${name || email},<br><br>v prílohe nájdeš faktúru za <strong>${product || 'AI službu'}</strong>.</p>
<table cellpadding="0" cellspacing="0" style="width:100%;background:#08080F;border-radius:8px;margin:15px 0;padding:15px;">
<tr><td style="padding:4px 0;color:#8888A0;font-size:12px;width:120px;">Produkt:</td><td style="padding:4px 0;color:#F0F0F5;font-size:13px;">${product || 'AI služba'}</td></tr>
${price ? `<tr><td style="padding:4px 0;color:#8888A0;font-size:12px;width:120px;">Suma:</td><td style="padding:4px 0;color:#F0F0F5;font-size:13px;">€${price}</td></tr>` : ''}
</table>
<h3 style="color:#CD7F32;font-size:14px;font-weight:600;margin:20px 0 10px 0;">💳 Platobné údaje</h3>
<table cellpadding="0" cellspacing="0" style="width:100%;background:#08080F;border-radius:8px;margin:10px 0;padding:15px;">
<tr><td style="padding:4px 0;color:#8888A0;font-size:12px;width:120px;">IBAN:</td><td style="padding:4px 0;color:#F0F0F5;font-size:13px;">SK78 1100 0000 0027 0129 7133</td></tr>
<tr><td style="padding:4px 0;color:#8888A0;font-size:12px;width:120px;">BIC:</td><td style="padding:4px 0;color:#F0F0F5;font-size:13px;">FIOZSKBAXXX</td></tr>
</table>
<p style="color:#F0F0F5;font-size:13px;">Po pripísaní platby spustíme analýzu do 24 hodín.</p>
<table cellpadding="0" cellspacing="0" style="margin:20px auto;">
<tr><td align="center" style="background:#CD7F32;border-radius:6px;padding:12px 28px;">
<a href="${pdfUrl}" style="color:#08080F;text-decoration:none;font-size:14px;font-weight:600;">Stiahnuť faktúru PDF</a></td></tr></table>
</td></tr>
<tr><td style="border-top:1px solid #CD7F3220;padding-top:20px;">
<p style="color:#8888A0;font-size:12px;margin:0 0 5px 0;">ASCENTIA s.r.o. · Klincová 37/B, 821 08 Bratislava · IČO: 51858959<br>marianstancik.dev · marianstancik@agentmail.to</p>
<p style="color:#8888A0;font-size:11px;margin:0;">Tento email bol odoslaný na základe objednávky na marianstancik.dev.</p>
</td></tr></table></div></td></tr></table></body></html>`;
        
        const text = `✧ FAKTÚRA č. ${invoice_id}\n\nAhoj ${name || email},\nnáš systém vygeneroval faktúru za ${product || 'AI službu'}.\n\nStiahnuť PDF: ${pdfUrl}\n\nIBAN: SK78 1100 0000 0027 0129 7133\nBIC: FIOZSKBAXXX\n\n--\nASCENTIA s.r.o.`;
        
        const sent = await sendAgentMail(email, subject, text, html);
        results.push({ email, action: 'invoice_sent', status: sent ? 'ok' : 'error' });
      }
      
      else if (reason === 'payment_reminder') {
        const subject = '✧ Pripomienka úhrady faktúry';
        const text = `Ahoj ${name || email},\n\npripomíname, že faktúra za ${product || 'službu'} čaká na úhradu.\n\nIBAN: SK78 1100 0000 0027 0129 7133\nBIC: FIOZSKBAXXX\n\n--\nASCENTIA s.r.o.`;
        
        const sent = await sendAgentMail(email, subject, text);
        results.push({ email, action: 'payment_reminder', status: sent ? 'ok' : 'error' });
      }
      
      else if (reason === 'followup_7d') {
        const subject = '✧ Čo sa u mňa udialo za posledný týždeň';
        const text = `Ahoj,\n\nodkedy si sa prihlásil k odberu, pribudlo niekoľko nových článkov:\n\n• Hermes Agent — autonómna AI na VPS\n• EU AI Act — praktický sprievodca compliance\n• Edge AI na drone — počítačové videnie v reálnom čase\n\nPozri celý blog: https://marianstancik.dev/blog\n\n--\nASCENTIA s.r.o.`;
        
        const sent = await sendAgentMail(email, subject, text);
        results.push({ email, action: 'followup_7d', status: sent ? 'ok' : 'error' });
      }
      
    } catch (e) {
      results.push({ action: action?.reason || 'unknown', error: e.message });
    }
  }
  
  return res.status(200).json({ processed: results.length, results });
}

async function sendAgentMail(to, subject, text, html) {
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
  
  const args = { inboxId: INBOX, to: [to], subject, text };
  if (html) args.html = html;
  
  const sendBody = JSON.stringify({ jsonrpc: '2.0', id: '2', method: 'tools/call', params: { name: 'send_message', arguments: args } });
  const msgRes = await fetch(url, { method: 'POST', headers: msgHeaders, body: sendBody });
  return msgRes.ok;
}