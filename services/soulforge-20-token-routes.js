// Soul Forge Token Routes (v1)

const express = require("express");
const router = express.Router();
const TokenManager = require("./soulforge-19-token-manager");

// List active tokens
router.get("/tokens", (req, res) => {
  const tokens = TokenManager.list();
  res.json({ tokens });
});

// Revoke a token
router.post("/tokens/revoke", (req, res) => {
  const { token } = req.body;

  if (!token) {
    return res.json({
      success: false,
      error: "Token required"
    });
  }

  TokenManager.revoke(token);

  res.json({
    success: true,
    revoked: token
  });
});

// Validate a token
router.post("/tokens/validate", (req, res) => {
  const { token } = req.body;

  const data = TokenManager.validate(token);

  if (!data) {
    return res.json({
      success: false,
      valid: false
    });
  }

  res.json({
    success: true,
    valid: true,
    user: data
  });
});

module.exports = router;