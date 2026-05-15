// Soul Forge Metrics API (v1)

const express = require("express");
const router = express.Router();

const MetricsCollector = require("./soulforge-41-metrics-collector");
const Logger = require("./soulforge-11-logger");

// Get full metrics summary
router.get("/summary", (req, res) => {
  const summary = MetricsCollector.getSummary();
  res.json({
    success: true,
    summary
  });
});

// Get total requests only
router.get("/total", (req, res) => {
  const summary = MetricsCollector.getSummary();
  res.json({
    success: true,
    totalRequests: summary.totalRequests
  });
});

// Get per-AI metrics
router.get("/per-ai", (req, res) => {
  const summary = MetricsCollector.getSummary();
  res.json({
    success: true,
    perAI: summary.perAI
  });
});

// Get request timestamps
router.get("/timestamps", (req, res) => {
  const summary = MetricsCollector.getSummary();
  res.json({
    success: true,
    timestamps: summary.timestamps
  });
});

// Clear metrics (admin only)
router.post("/clear", (req, res) => {
  MetricsCollector.save({
    totalRequests: 0,
    perAI: {},
    timestamps: []
  });

  Logger.event("Metrics cleared");

  res.json({
    success: true,
    message: "Metrics reset"
  });
});

module.exports = router;