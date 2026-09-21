const https = require('https');

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const text = req.body?.text || req.query?.text;
  if (!text) {
    return res.status(400).json({ error: 'Nội dung thông báo (text) là bắt buộc' });
  }

  const parse_mode = req.body?.parse_mode || req.query?.parse_mode || 'HTML';
  const chat_id = req.body?.chat_id || req.query?.chat_id || TELEGRAM_CHAT_ID;

  const params = new URLSearchParams({
    chat_id: chat_id,
    text: text,
    parse_mode: parse_mode
  });

  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage?` + params.toString();

  https.get(url, (teleResp) => {
    let data = '';
    teleResp.on('data', chunk => data += chunk);
    teleResp.on('end', () => {
      try {
        const json = JSON.parse(data);
        return res.status(200).json({ success: true, result: json });
      } catch (e) {
        return res.status(200).json({ success: true, raw: data });
      }
    });
  }).on('error', (err) => {
    return res.status(500).json({ error: err.message });
  });
};
