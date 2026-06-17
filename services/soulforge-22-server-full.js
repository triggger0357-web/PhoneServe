// Soul Forge Full Server (API + UI + Auth + Tokens) (v1)

const express = require("express");
const app = express();
const path = require("path");

// Core integrations
const integrateAuth = require("./soulforge-17-auth-integration");
const integrateTokens = require("./soulforge-21-token-integration");

// API
const api = require("./soulforge-12-api");

// UI
const uiPath = path.join(__dirname, "soulforge-3-ui.html");

app.use(express.json());

// Authentication + Token systems
integrateAuth(app);
integrateTokens(app);

// Protected API routes
app.use("/api/soulforge", api);

// UI route
app.get("/", (req, res) => {
  res.sendFile(uiPath);
});

// Static files
app.use(express.static(__dirname));

const PORT = 8080;
app.listen(PORT, () => {
  console.log(`Soul Forge Full Server running on port ${PORT}`);
});