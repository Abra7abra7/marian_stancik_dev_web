// Gmail API sender for Cloudflare Pages Functions (Google Workspace) — legal v3.0.1.
// Legacy third-party inbox provider fully removed from the personal-data flow: transactional e-mails (opt-in
// confirmation, welcome/kit, admin alerts) are sent from the operator's own
// Google Workspace mailbox.
//
// Auth — two supported paths, set in Cloudflare Pages environment variables:
//   A) GMAIL_REFRESH_TOKEN + GMAIL_CLIENT_ID + GMAIL_CLIENT_SECRET
//      (OAuth2 offline refresh token — works for the Workspace mailbox)
//   B) GMAIL_SERVICE_ACCOUNT_JSON + GMAIL_IMPERSONATED_USER
//      (service account JSON key + domain-wide delegation, Workspace only)
// Optional: GMAIL_USER (defaults to stancikmarian8@gmail.com), GMAIL_FROM_NAME.
//
// TODO(Marián — Google Workspace Admin konzola, mimo repozitára):
//   - Data Region = Europe (Sheets + Gmail). Zásady OOU v3.0.1 to deklarujú;
//     nastavenie je v Admin konzole (Account > Data regions).
// TODO(Marián — Google Cloud Console): vytvor OAuth client / service account
//   a vlož credentials do Pages env varsov. Bez nich vracia sendGmail chybu
//   a /api/subscribe odpovedá 500 (rovnako ako predtým chýbajúci e-mail credentials).

const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const SCOPE = 'https://www.googleapis.com/auth/gmail.send';
const DEFAULT_USER = 'stancikmarian8@gmail.com';

function b64urlEncode(bytes) {
  let bin = '';
  const arr = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  for (const b of arr) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function b64EncodeUtf8(str) {
  return btoa(String.fromCharCode(...new TextEncoder().encode(str)));
}

function pemToArrayBuffer(pem) {
  const body = pem
    .replace(/-----BEGIN PRIVATE KEY-----/, '')
    .replace(/-----END PRIVATE KEY-----/, '')
    .replace(/\\n/g, '\n')
    .replace(/\s+/g, '');
  const bin = atob(body);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr.buffer;
}

async function accessTokenFromServiceAccount(env) {
  const sa = JSON.parse(env.GMAIL_SERVICE_ACCOUNT_JSON);
  const now = Math.floor(Date.now() / 1000);
  const header = b64urlEncode(new TextEncoder().encode(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const claim = b64urlEncode(new TextEncoder().encode(JSON.stringify({
    iss: sa.client_email,
    scope: SCOPE,
    aud: TOKEN_URL,
    sub: env.GMAIL_IMPERSONATED_USER || DEFAULT_USER, // domain-wide delegation
    iat: now,
    exp: now + 3600
  })));
  const key = await crypto.subtle.importKey(
    'pkcs8', pemToArrayBuffer(sa.private_key),
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(`${header}.${claim}`));
  const assertion = `${header}.${claim}.${b64urlEncode(sig)}`;

  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion
    })
  });
  if (!res.ok) throw new Error(`Gmail token (service account) failed: HTTP ${res.status}`);
  const data = await res.json();
  if (!data.access_token) throw new Error('Gmail token (service account): no access_token');
  return data.access_token;
}

async function accessTokenFromRefreshToken(env) {
  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: env.GMAIL_REFRESH_TOKEN,
      client_id: env.GMAIL_CLIENT_ID,
      client_secret: env.GMAIL_CLIENT_SECRET
    })
  });
  if (!res.ok) throw new Error(`Gmail token (refresh) failed: HTTP ${res.status}`);
  const data = await res.json();
  if (!data.access_token) throw new Error('Gmail token (refresh): no access_token');
  return data.access_token;
}

async function getAccessToken(env) {
  if (env.GMAIL_REFRESH_TOKEN) return accessTokenFromRefreshToken(env);
  if (env.GMAIL_SERVICE_ACCOUNT_JSON) return accessTokenFromServiceAccount(env);
  throw new Error('Gmail credentials not configured (set GMAIL_REFRESH_TOKEN or GMAIL_SERVICE_ACCOUNT_JSON in Pages env)');
}

function buildMime({ from, to, subject, text, html }) {
  const boundary = 'alt_' + crypto.randomUUID();
  const headers = [
    `From: ${from}`,
    `To: ${to}`,
    `Subject: =?UTF-8?B?${btoa(String.fromCharCode(...new TextEncoder().encode(subject)))}?=`,
    'MIME-Version: 1.0',
    `Content-Type: multipart/alternative; boundary="${boundary}"`
  ];
  const parts = [
    `--${boundary}\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n${text}`,
    html
      ? `--${boundary}\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n${b64EncodeUtf8(html)}`
      : null
  ].filter(Boolean);
  return headers.join('\r\n') + '\r\n\r\n' + parts.join('\r\n') + `\r\n--${boundary}--`;
}

export async function sendGmail(env, to, subject, text, html) {
  const accessToken = await getAccessToken(env);
  const user = env.GMAIL_USER || DEFAULT_USER;
  const fromName = env.GMAIL_FROM_NAME || 'Marian Stancik';
  const mime = buildMime({ from: `${fromName} <${user}>`, to, subject, text, html });

  const boundary = 'msg_' + crypto.randomUUID();
  const body =
    `--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{}\r\n` +
    `--${boundary}\r\nContent-Type: message/rfc822\r\n\r\n${mime}\r\n--${boundary}--`;

  const res = await fetch(
    `https://gmail.googleapis.com/upload/gmail/v1/users/${encodeURIComponent(user)}/messages/send?uploadType=multipart`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': `multipart/related; boundary=${boundary}`
      },
      body
    }
  );
  if (!res.ok) {
    const errText = (await res.text()).slice(0, 200);
    throw new Error(`Gmail send failed: HTTP ${res.status} ${errText}`);
  }
  return { ok: true };
}
