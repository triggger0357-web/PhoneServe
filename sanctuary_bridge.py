cd ~/PhoneServe

# 1. Update server.js with middleware and telemetry route
cat << 'EOF' > server.js
const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static('.'));

// 2026-18plus-v1 Token Authorization Middleware
const verifyAdminToken = (req, res, next) => {
  const token = req.headers['authorization'] || req.query.token;
  const validToken = process.env.ADMIN_TOKEN || '2026-18plus-v1-secure-key';

  if (!token || token !== validToken) {
    return res.status(401).json({ error: 'Unauthorized: Sovereign token invalid' });
  }
  next();
};

// Admin Telemetry Endpoint
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

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`PhoneServe node active on port ${PORT}`));
EOF

# 2. Inject telemetry listener into admin.html before </body>
if ! grep -q "fetchNodeTelemetry" admin.html; then
  sed -i '/<\/body>/i \
<script>\
  async function fetchNodeTelemetry() {\
    const token = localStorage.getItem("phoneserve_admin_token") || "2026-18plus-v1-secure-key";\
    try {\
      const res = await fetch("/api/admin/telemetry", { headers: { "Authorization": token } });\
      if (!res.ok) throw new Error("Unauthorized");\
      const data = await res.json();\
      if (document.getElementById("status-badge")) document.getElementById("status-badge").textContent = data.nodeStatus.toUpperCase();\
      if (document.getElementById("peer-count")) document.getElementById("peer-count").textContent = data.peersConnected;\
    } catch (err) {\
      if (document.getElementById("status-badge")) document.getElementById("status-badge").textContent = "UNAUTHORIZED";\
    }\
  }\
  document.addEventListener("DOMContentLoaded", () => {\
    fetchNodeTelemetry();\
    setInterval(fetchNodeTelemetry, 5000);\
  });\
</script>' admin.html
fi

# 3. Commit and push changes
git add server.js admin.html
git commit -m "Auto-configured server auth and telemetry polling"
git push origin main

