// Soul Forge Routes (v1)

const express = require("express");
const router = express.Router();
const SoulForge = require("./soulforge-1-core");

// Get available upgrades for an AI
router.get("/ai/:id/upgrades", (req, res) => {
  const upgrades = SoulForge.listAvailableUpgrades(req.params.id);
  res.json({ upgrades });
});

// Apply an upgrade to an AI
router.post("/ai/:id/upgrade", (req, res) => {
  const result = SoulForge.applyUpgrade(req.params.id, req.body.upgradeId);
  res.json(result);
});

// Get all personality profiles
router.get("/personalities", (req, res) => {
  const personalities = SoulForge.listPersonalityProfiles();
  res.json({ personalities });
});

// Assign a personality to an AI
router.post("/ai/:id/personality", (req, res) => {
  const result = SoulForge.assignPersonality(req.params.id, req.body.personalityId);
  res.json(result);
});

// Evolve an AI on a specific track
router.post("/ai/:id/evolve", (req, res) => {
  const { track, amount } = req.body;
  const result = SoulForge.evolve(req.params.id, track, amount);
  res.json(result);
});

// Get AI state
router.get("/ai/:id/state", (req, res) => {
  const state = SoulForge.getAIState(req.params.id);
  res.json(state);
});

module.exports = router;