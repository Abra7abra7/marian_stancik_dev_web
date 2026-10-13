// Cloudflare Pages Function — Secure invoice proxy (HTTPS via marianstancik.dev)
export async function onRequestGet(context) {
  const { params, env } = context;
  const id = params.id;

  if (!id || !/^[\w-]+(\.pdf)?$/.test(id)) {
    return new Response(JSON.stringify({ error: 'Invalid invoice ID' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const filename = id.endsWith('.pdf') ? id : `${id}.pdf`;
  const invoiceHost = env.INVOICE_HOST || 'https://api.marianstancik.dev';
  const vpsUrl = `${invoiceHost}/assets/invoices/${filename}`;

  try {
    const response = await fetch(vpsUrl);

    if (!response.ok) {
      return new Response(JSON.stringify({ error: 'Invoice not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const pdfBuffer = await response.arrayBuffer();

    return new Response(pdfBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Cache-Control': 'private, no-cache, no-store, must-revalidate',
        'X-Robots-Tag': 'noindex, nofollow, noarchive'
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Failed to fetch invoice' }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
