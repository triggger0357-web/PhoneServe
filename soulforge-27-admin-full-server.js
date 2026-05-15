// Soul Forge Full Admin Server (Admin Panel + Admin API + Auth + Tokens) (v1)

const express = require("express");
const path = require("path");
const app = express();

// Integrations
const integrateAuth = require("./soulforge-17-auth-integration");
const integrateTokens = require("./soulforge-21-token-integration");
const integrateAdminAPI = require("./soulforge-26-admin-integration");

// Admin UI
const adminPanelPath = path.join(__dirname, "soulforge-23-admin-panel.html");

// JSON parsing
app.use(express.json());

// Auth + Token systems
integrateAuth(app);
integrateTokens(app);

// Admin API (protected)
integrateAdminAPI(app);

// Admin Panel UI
app.get("/admin", (req, res) => {
  res.sendFile(adminPanelPath);
});

// Static files
app.use(express.static(__dirname));

const PORT = 8091;
app.listen(PORT, () => {
  console.log(`Soul Forge Full Admin Server running on port ${PORT}`);
});