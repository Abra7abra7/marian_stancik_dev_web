// Cloudflare Pages Middleware — Content Negotiation & Edge Routing
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Apex domain redirect to www canonical
  if (url.hostname === 'marianstancik.dev') {
    url.hostname = 'www.marianstancik.dev';
    return Response.redirect(url.toString(), 308);
  }

  const accept = request.headers.get('accept') || '';

  // Markdown content negotiation for AI engines (llmstxt / Accept: text/markdown)
  if (accept.includes('text/markdown')) {
    if (url.pathname === '/' || url.pathname === '') {
      return context.env.ASSETS.fetch(new URL('/index.html.md', request.url));
    }
    if (url.pathname === '/blog' || url.pathname === '/blog/') {
      return context.env.ASSETS.fetch(new URL('/blog/index.html.md', request.url));
    }
    if (url.pathname.startsWith('/blog/posts/')) {
      const cleanPath = url.pathname.replace(/\/$/, '');
      if (!cleanPath.endsWith('.md')) {
        return context.env.ASSETS.fetch(new URL(`${cleanPath}.md`, request.url));
      }
    }
  }

  return await next();
}
