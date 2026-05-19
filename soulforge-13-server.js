// Soul Forge Main Server (v1)

const express = require("express");
const app = express();
const path = require("path");

const api = require("./soulforge-12-api");
const uiPath = path.join(__dirname, "soulforge-3-ui.html");

app.use(express.json());

// API routes
app.use("/api/soulforge", api);

// UI route
app.get("/", (req, res) => {
  res.sendFile(uiPath);
});

// Static files (if needed)
app.use(express.static(__dirname));

// Start server
const PORT = 8080;
app.listen(PORT, () => {
  console.log(`Soul Forge server running on port ${PORT}`);
});