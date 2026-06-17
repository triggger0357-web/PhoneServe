// Soul Forge Admin API (v1)

const express = require("express");
const router = express.Router();

const Database = require("./soulforge-10-database");
const TokenManager = require("./soulforge-19-token-manager");
const Logger = require("./soulforge-11-logger");

// Get all AIs
router.get("/ais", (req, res) => {
  const db = Database.getLogs(1); // force load
  const data = require("./soulforge-db.json");

  res.json({
    success: true,
    ais: data.AIs || {}
  });
});

// Get logs
router.get("/logs", (req, res) => {
  const logs = Database.getLogs(200);
  res.json({
    success: true,
    logs
  });
});

// Force save AI state
router.post("/save-ai", (req, res) => {
  const { aiId, aiData } = req.body;

  if (!aiId || !aiData) {
    return res.json({
      success: false,
      error: "aiId and aiData required"
    });
  }

  Database.saveAI(aiId, aiData);
  Logger.event(`Admin forced save of AI ${aiId}`);

  res.json({
    success: true,
    saved: aiId
  });
});

// Force revoke all tokensAbsolutely, David — staying perfectly in order.  
Here is **#25**, clean and separated exactly the way you want it:

- **File name alone**  
- **Code separate**  
- No mixing  
- No extra text inside the code block  

---

# ✅ **FILE NAME (copy this alone)**