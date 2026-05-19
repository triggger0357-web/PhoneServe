const express = require('express');
const path = require('path');
const crypto = require('crypto');
const os = require('os');

const app = express();
const PORT = 5000;

const NODE_PASSCODE = 'EdgeTechNode0357!';
const AUTH_TOKEN = Buffer.from(NODE_PASSCODE).toString('base64');

// Generate a persistent, local Ed25519 Key Pair for this session's Node Identity
const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
const nodePublicKeyHex = publicKey.export({ type: 'spki', format: 'der' }).toString('hex').slice(0, 32);

app.use(express.json());

const projectDir = '/data/data/com.termux/files/home/PhoneServe';
app.use(express.static(path.join(projectDir, 'public')));

// Public Root Route
app.get('/', (req, res) => {
    res.sendFile(path.join(projectDir, 'index.html'));
});

// 1. Diagnostics Endpoint (CPU, Memory, Node Status)
app.get('/api/diagnostics', (req, res) => {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    
    res.json({
        uptime: Math.floor(process.uptime()),
        memory: {
            total: (totalMem / (1024 * 1024)).toFixed(2) + ' MB',
            used: (usedMem / (1024 * 1024)).toFixed(2) + ' MB',
            free: (freeMem / (1024 * 1024)).toFixed(2) + ' MB',
            percentage: ((usedMem / totalMem) * 100).toFixed(1) + '%'
        },
        platform: os.platform(),
        arch: os.arch(),
        nodeId: 'PS-0357',
        publicKey: nodePublicKeyHex
    });
});

// 2. Safe Harbor Compliance Handshake
app.post('/api/safe-harbor', (req, res) => {
    const { ageVerified, userConsent } = req.body;
    if (ageVerified && userConsent) {
        return res.json({
            status: 'COMPLIANT',
            handshakeToken: crypto.randomBytes(16).toString('hex'),
            timestamp: new Date().toISOString(),
            framework: 'Online Safety Act 2026'
        });
    }
    res.status(400).json({ status: 'NON_COMPLIANT', error: 'Verification or consent missing.' });
});

// 3. Enhanced Proxy Gateway with Ed25519 Cryptographic Signatures
app.get('/api/gateway', async (req, res) => {
    const targetUrl = req.query.url;
    if (!targetUrl) {
        return res.status(400).send('Missing target url parameter (?url=...)');
    }
    try {
        const axios = require('axios');
        const response = await axios.get(targetUrl, { responseType: 'text' });
        const payload = response.data;
        
        // Sign the data using our node's private key
        const signature = crypto.sign(null, Buffer.from(payload), privateKey).toString('hex');
        
        // Return signed payload architecture
        res.json({
            gateway: 'PhoneServe Edge Node',
            nodeId: 'PS-0357',
            signature: signature,
            publicKey: nodePublicKeyHex,
            data: payload
        });
    } catch (error) {
        res.status(500).send('Gateway routing error: ' + error.message);
    }
});

// Bind Server
try {
    app.listen(PORT, () => {
        console.log(`PhoneServe Node successfully bound to port ${PORT}`);
    });
} catch (err) {
    console.error('Critical binding error:', err.message);
}
