// Vercel serverless — Secure invoice proxy (HTTPS via marianstancik.dev)
// Fetches PDF from VPS and returns it with proper headers

export default async function handler(req, res) {
  const { id } = req.query;
  
  if (!id || !/^[\w-]+(\.pdf)?$/.test(id)) {
    return res.status(400).json({ error: 'Invalid invoice ID' });
  }
  
  const filename = id.endsWith('.pdf') ? id : `${id}.pdf`;
  const invoiceHost = process.env.INVOICE_HOST || 'https://api.marianstancik.dev';
  const vpsUrl = `${invoiceHost}/assets/invoices/${filename}`;
  
  try {
    const response = await fetch(vpsUrl);
    
    if (!response.ok) {
      return res.status(404).json({ error: 'Invoice not found' });
    }
    
    const buffer = await response.arrayBuffer();
    const pdfBuffer = Buffer.from(buffer);
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.setHeader('Content-Length', pdfBuffer.length);
    res.setHeader('Cache-Control', 'private, no-cache, no-store, must-revalidate');
    res.setHeader('X-Robots-Tag', 'noindex, nofollow, noarchive');
    
    return res.status(200).send(pdfBuffer);
  } catch (e) {
    console.error('Invoice proxy error:', e.message);
    return res.status(502).json({ error: 'Failed to fetch invoice' });
  }
}