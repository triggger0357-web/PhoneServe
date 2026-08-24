const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static(__dirname));
app.use(express.static(path.join(__dirname, 'public')));

const verifyAdminToken = (req, res, next) => {
  const token = req.headers['authorization'] || req.query.token;
  const validToken = process.env.ADMIN_TOKEN || '2026-18plus-v1-secure-key';

  if (!token || token !== validToken) {
    return res.status(401).json({ error: 'Unauthorized: Sovereign token invalid' });
  }
  next();
};

app.get('/api/admin/telemetry', verifyAdminToken, (req, res) => {
  res.json({
    nodeStatus: 'active',
    compliance: '2026-18plus-v1',
    uptimeSeconds: Math.floor(process.uptime()),
    peersConnected: 8,
    bandwidth: { rx_kb: 2048, tx_kb: 5120 },
    timestamp: new Date().toISOString()
  });
});

app.get(['/admin', '/admin.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => console.log(`PhoneServe node active on port ${PORT}`));

// Inner Reality Clock & Health Endpoint
app.get('/api/health', (req, res) => {
  const mem = process.memoryUsage().heapUsed / 1024 / 1024;
  res.json({
    status: 'HEALTHY',
    uptime: Math.floor(process.uptime()),
    memoryMB: Math.round(mem),
    timestamp: new Date().toISOString()
  });
});
