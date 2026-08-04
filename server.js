const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const PORT = process.env.PORT || 3002;
const ADMIN_PASSCODE = process.env.ADMIN_PASSCODE || 'DAVIDGOD';
const sessions = new Set();
function sendJSON(res, status, obj) {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(obj));
}
function readBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try { resolve(body ? JSON.parse(body) : {}); }
            catch (e) { reject(e); }
        });
        req.on('error', reject);
    });
}
function isAuthed(req) {
    const auth = req.headers['authorization'] || '';
    const token = auth.replace('Bearer ', '').trim();
    return sessions.has(token);
}
const server = http.createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

    if (req.url === '/api/auth' && req.method === 'POST') {
        try {
            const { passcode } = await readBody(req);
            if (passcode === ADMIN_PASSCODE) {
                const token = crypto.randomBytes(24).toString('hex');
                sessions.add(token);
                return sendJSON(res, 200, { token });
            }
            return sendJSON(res, 401, { error: 'Invalid passcode.' });
        } catch (e) {
            return sendJSON(res, 400, { error: 'Bad request.' });
        }
    }
    if (req.url === '/api/admin' && req.method === 'POST') {
        if (!isAuthed(req)) return sendJSON(res, 401, { error: 'Not authenticated.' });
        try {
            const { action } = await readBody(req);
            if (action === 'status') {
                return sendJSON(res, 200, { result: `Node OK. Uptime: ${process.uptime().toFixed(0)}s` });
            }
            if (action === 'restart') {
                sendJSON(res, 200, { result: 'Restart signal received (manual restart required in Termux).' });
                return;
            }
            return sendJSON(res, 400, { error: 'Unknown action.' });
        } catch (e) {
            return sendJSON(res, 400, { error: 'Bad request.' });
        }
    }

    let filePath = path.join(__dirname, 'public', req.url === '/' ? 'index.html' : req.url);
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end("Not Found - " + req.url);
        } else {
            res.writeHead(200);
            res.end(data);
        }
    });
});

server.listen(PORT, () => console.log(`✅ COMMAND CENTER ONLINE ON PORT ${PORT}`));
