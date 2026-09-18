module.exports = async (req, res) => {
  try {
    res.setHeader(Access-Control-Allow-Origin, *);
    res.setHeader(Access-Control-Allow-Methods, POST, OPTIONS);
    res.setHeader(Access-Control-Allow-Headers, Content-Type);

    if (req.method === OPTIONS) {
      res.statusCode = 200;
      return res.end();
    }

    // Read body buffer safely
    let body = req.body;
    if (!body || typeof body !== object) {
      const chunks = [];
      for await (const chunk of req) {
        chunks.push(typeof chunk === string ? Buffer.from(chunk) : chunk);
      }
      const raw = Buffer.concat(chunks).toString(utf-8);
      try { body = JSON.parse(raw); } catch(e) { body = {}; }
    }

    const { to, subject, html, text, from } = body || {};

    if (!to || !subject || (!html && !text)) {
      res.statusCode = 400;
      res.setHeader(Content-Type, application/json);
      return res.end(JSON.stringify({ error: Missing required fields: to, subject, content }));
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
        subject: subject,
        html: html || <p></p>
      })
    });

    const data = await response.json();
    res.statusCode = response.ok ? 200 : response.status;
    res.setHeader(Content-Type, application/json);
    return res.end(JSON.stringify({ success: response.ok, data }));
  } catch (err) {
    res.statusCode = 500;
    res.setHeader(Content-Type, application/json);
    return res.end(JSON.stringify({ error: err.message, stack: err.stack }));
  }
};
