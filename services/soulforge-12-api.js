// Soul Forge API Router (v1)

const express = require("express");
const router = express.Router();

const SoulForge = require("./soulforge-1-core");
const ActionEngine = require("./soulforge-9-actions");
const EvolutionEngine = require("./soulforge-4-evolution");
const Logger = require("./soulforge-11-logger");
const Database = require("./soulforge-10-database");

// Get AI state
router.get("/ai/:id", (req, res) => {
  const ai = SoulForge.getAIState(req.params.id);
  res.json(ai);
});

// Perform an action
router.post("/ai/:id/action", (req, res) => {
  const { actionType } = req.body;
  const result = ActionEngine.performAction(req.params.id, actionType);

  Logger.action(req.params.id, actionType);
  Database.logEvent(`AI ${req.params.id} performed action ${actionType}`);

  res.json(result);
});

// Apply an upgrade
router.post("/ai/:id/upgrade", (req, res) => {
  const { upgradeId } = req.body;
  const result = SoulForge.applyUpgrade(req.params.id, upgradeId);

  Logger.upgrade(req.params.id, upgradeId);
  Database.saveAI(req.params.id, result.ai);

  res.json(result);
});

// Assign personality
router.post("/ai/:id/personality", (req, res) => {
  const { personalityId } = req.body;
  const result = SoulForge.assignPersonality(req.params.id, personalityId);

  Logger.personality(req.params.id, personalityId);
  Database.saveAI(req.params.id, result.ai);

  res.json(result);
});

// Manual evolution
router.post("/ai/:id/evolve", (req, res) => {
  const { track, amount } = req.body;
  const result = EvolutionEngine.evolveAI(req.params.id, track, amount);

  Database.saveAI(req.params.id, result.ai);
  res.json(result);
});

// Get logs
router.get("/logs", (req, res) => {
  const logs = Database.getLogs(100);
  res.json({ logs });
});

module.exports = router;