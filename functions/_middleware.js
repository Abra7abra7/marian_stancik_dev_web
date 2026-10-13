// Cloudflare Pages Middleware — Content Negotiation & Edge Routing
export async function onRequest(context) {
  const { request, next } = context;
  const accept = request.headers.get('accept') || '';
  const url = new URL(request.url);

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

  // Trailing slash normalization: remove trailing slash if not root
  if (url.pathname.length > 1 && url.pathname.endsWith('/')) {
    url.pathname = url.pathname.slice(0, -1);
    return Response.redirect(url.toString(), 308);
  }

  return await next();
}
