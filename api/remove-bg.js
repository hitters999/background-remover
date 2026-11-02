function sendJson(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}

function allowCors(res, origin) {
  const allowed = new Set([
    'https://bg.toolyfi.com',
    'https://toolyfi.com',
    'https://www.toolyfi.com',
  ]);
  if (origin && allowed.has(origin)) res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Vary', 'Origin');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

module.exports = async function handler(req, res) {
  allowCors(res, req.headers.origin);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return sendJson(res, 405, { success: false, error: 'Method not allowed' });

  const apiKey = (process.env.CLIPDROP_KEY || '')
    .trim()
    .replace(/[‐‑‒–—−]/g, '-');
  if (!apiKey) return sendJson(res, 500, { success: false, error: 'Clipdrop API key is not configured' });

  try {
    const payload = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const dataUrl = payload.image;
    if (typeof dataUrl !== 'string' || !dataUrl.startsWith('data:image/')) {
      return sendJson(res, 400, { success: false, error: 'Send an image data URL in the image field' });
    }

    const comma = dataUrl.indexOf(',');
    if (comma < 0) return sendJson(res, 400, { success: false, error: 'Invalid image data' });
    const mime = dataUrl.slice(5, comma).split(';')[0] || 'image/png';
    const imageBuffer = Buffer.from(dataUrl.slice(comma + 1), 'base64');
    if (!imageBuffer.length) return sendJson(res, 400, { success: false, error: 'The uploaded image is empty' });
    if (imageBuffer.length > 3 * 1024 * 1024) {
      return sendJson(res, 413, { success: false, error: 'Image is too large for this free serverless plan. Maximum size is 3 MB.' });
    }

    const form = new FormData();
    form.append('image_file', new Blob([imageBuffer], { type: mime }), 'image');
    const response = await fetch('https://clipdrop-api.co/remove-background/v1', {
      method: 'POST',
      headers: { 'x-api-key': apiKey, accept: 'image/png' },
      body: form,
    });

    if (!response.ok) {
      const detail = await response.text();
      console.error('Clipdrop API error', response.status, detail.slice(0, 500));
      return sendJson(res, response.status === 402 ? 402 : 502, {
        success: false,
        error: response.status === 402 ? 'Clipdrop credits are unavailable' : 'Background removal provider failed',
      });
    }

    const result = Buffer.from(await response.arrayBuffer()).toString('base64');
    return sendJson(res, 200, { success: true, image: `data:image/png;base64,${result}`, type: 'image/png' });
  } catch (error) {
    console.error('Background removal error', error);
    return sendJson(res, 500, { success: false, error: 'Background removal failed. Please try another image.' });
  }
};
