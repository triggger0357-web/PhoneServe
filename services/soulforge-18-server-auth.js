// Soul Forge Server + Auth Integration (v1)

const express = require("express");
const app = express();
const path = require("path");

const integrateAuth = require("./soulforge-17-auth-integration");
const api = require("./soulforge-12-api");

const uiPath = path.join(__dirname, "soulforge-3-ui.html");

app.use(express.json());

// Integrate authentication system
integrateAuth(app);

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
  console.log(`Soul Forge (Auth Enabled) running on port ${PORT}`);
});