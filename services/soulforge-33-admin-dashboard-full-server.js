// Soul Forge Admin Dashboard Full Server (v1)

const express = require("express");
const path = require("path");
const app = express();

// Integrations
const integrateAuth = require("./soulforge-17-auth-integration");
const integrateTokens = require("./soulforge-21-token-integration");
const integrateAdminAPI = require("./soulforge-26-admin-integration");
const integrateAdminDashboard = require("./soulforge-31-admin-dashboard-integration");

// JSON parsing
app.use(express.json());

// Auth + Token systems
integrateAuth(app);
integrateTokens(app);

// Admin API (protected)
integrateAdminAPI(app);

// Admin Dashboard UI
integrateAdminDashboard(app);

// Static files
app.use(express.static(__dirname));

const PORT = 8093;
app.listen(PORT, () => {
  console.log(`Soul Forge Admin Dashboard Full Server running on port ${PORT}`);
});