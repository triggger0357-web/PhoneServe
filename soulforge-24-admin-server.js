// Soul Forge Admin Panel Server (v1)

const express = require("express");
const path = require("path");
const app = express();

const integrateAuth = require("./soulforge-17-auth-integration");
const integrateTokens = require("./soulforge-21-token-integration");

const adminPanelPath = path.join(__dirname, "soulforge-23-admin-panel.html");

// JSON parsing
app.use(express.json());

// Auth + Token systems
integrateAuth(app);
integrateTokens(app);

// Admin panel UI
app.get("/admin", (req, res) => {
  res.sendFile(adminPanelPath);
});

// Static files
app.use(express.static(__dirname));

const PORT = 8090;
app.listen(PORT, () => {
  console.log(`Soul Forge Admin Panel running on port ${PORT}`);
});