module.exports = (req, res) => {
  const token = req.headers['authorization'] || req.query.token;
  const validToken = process.env.ADMIN_TOKEN || '2026-18plus-v1-secure-key';

  if (!token || token !== validToken) {
    return res.status(401).json({ error: 'Unauthorized: Sovereign token invalid' });
  }

  return res.status(200).json({
    nodeStatus: 'active',
    compliance: '2026-18plus-v1',
    uptimeSeconds: Math.floor(process.uptime()),
    peersConnected: 8,
    bandwidth: { rx_kb: 2048, tx_kb: 5120 },
    timestamp: new Date().toISOString()
  });
};
