/**
 * Pages Functions — API proxy to Worker
 * Všetky requesty na /api/* sú presmerované na Worker
 */

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // Forward to Worker
  const workerUrl = `https://marian-stancik.stancikmarian8.workers.dev${url.pathname}${url.search}`;
  
  const headers = new Headers(request.headers);
  headers.set('Host', 'marian-stancik.stancikmarian8.workers.dev');
  
  const workerResponse = await fetch(workerUrl, {
    method: request.method,
    headers: headers,
    body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : undefined,
  });
  
  return new Response(workerResponse.body, {
    status: workerResponse.status,
    statusText: workerResponse.statusText,
    headers: workerResponse.headers,
  });
}