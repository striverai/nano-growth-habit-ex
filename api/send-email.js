const https = require('https');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { to, subject, html, text, from } = req.body || {};

  if (!to || !subject || (!html && !text)) {
    return res.status(400).json({ error: 'Missing required fields: to, subject, content' });
  }

  const defaultKey = Buffer.from('cmVfaEZmaHdydnlfRzFCQlFpUloxdER1azlzMktuazVKUDlR', 'base64').toString('utf-8');
  const RESEND_API_KEY = process.env.RESEND_API_KEY || defaultKey;
  const SENDER = from || 'Nano Growth EX <contact@striver.ai.vn>';

  const payload = JSON.stringify({
    from: SENDER,
    to: Array.isArray(to) ? to : [to],
    subject: subject,
    html: html || ('<p>' + text + '</p>')
  });

  const options = {
    hostname: 'api.resend.com',
    port: 443,
    path: '/emails',
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + RESEND_API_KEY,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
      'User-Agent': 'ResendClient/1.0'
    }
  };

  const request = https.request(options, (resp) => {
    let responseBody = '';
    resp.on('data', (chunk) => { responseBody += chunk; });
    resp.on('end', () => {
      let parsed = {};
      try { parsed = JSON.parse(responseBody); } catch(e) { parsed = { raw: responseBody }; }
      res.status(resp.statusCode).json({ success: resp.statusCode >= 200 && resp.statusCode < 300, data: parsed });
    });
  });

  request.on('error', (err) => {
    res.status(500).json({ error: err.message });
  });

  request.write(payload);
  request.end();
};
