module.exports = async (req, res) => {
  try {
    // CORS headers
    res.setHeader(Access-Control-Allow-Origin, *);
    res.setHeader(Access-Control-Allow-Methods, POST, OPTIONS);
    res.setHeader(Access-Control-Allow-Headers, Content-Type);

    if (req.method === OPTIONS) {
      return res.status(200).end();
    }

    if (req.method !== POST) {
      return res.status(405).json({ error: Method Not Allowed });
    }

    let body = req.body;
    if (typeof body === string) {
      try { body = JSON.parse(body); } catch(e) {}
    }
    const { to, subject, html, text, from } = body || {};

    if (!to || !subject || (!html && !text)) {
      return res.status(400).json({ error: Missing required fields: to, subject, content });
    }

    const defaultKey = Buffer.from(cmVfaEZmaHdydnlfRzFCQlFpUlowdER1azlzMktuazVKUDlR, base64).toString(utf-8);
    const RESEND_API_KEY = process.env.RESEND_API_KEY || defaultKey;
    const SENDER = from || Nano Growth EX <contact@striver.ai.vn>;

    const response = await fetch(https://api.resend.com/emails, {
      method: POST,
      headers: {
        Authorization: Bearer ,
        Content-Type: application/json,
        User-Agent: ResendClient/1.0
      },
      body: JSON.stringify({
        from: SENDER,
        to: Array.isArray(to) ? to : [to],
        subject,
        html: html || <p></p>
      })
    });

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json(data);
    }

    return res.status(200).json({ success: true, data });
  } catch (err) {
    return res.status(500).json({ error: err.message, stack: err.stack });
  }
};
