// Soul Forge System Health API (v1)

const express = require("express");
const router = express.Router();

const HealthMonitor = require("./soulforge-37-system-health-monitor");
const Logger = require("./soulforge-11-logger");

// Get full system health snapshot
router.get("/status", (req, res) => {
  const status = HealthMonitor.getStatus();
  res.json({
    success: true,
    status
  });
});

// Get CPU only
router.get("/cpu", (req, res) => {
  const cpu = HealthMonitor.getCPU();
  res.json({
    success: true,
    cpuPercent: cpu
  });
});

// Get memory only
router.get("/memory", (req, res) => {
  const mem = HealthMonitor.getMemory();
  res.json({
    success: true,
    memory: mem
  });
});

// Get disk info
router.get("/disk", (req, res) => {
  const disk = HealthMonitor.getDisk();
  res.json({
    success: true,
    disk
  });
});

// Get uptime
router.get("/uptime", (req, res) => {
  const uptime = HealthMonitor.getUptime();
  res.json({
    success: true,
    uptimeSeconds: uptime
  });
});

module.exports = router;