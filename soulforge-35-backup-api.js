// Soul Forge Backup API (v1)

const express = require("express");
const router = express.Router();

const BackupManager = require("./soulforge-34-backup-manager");
const Database = require("./soulforge-10-database");
const Logger = require("./soulforge-11-logger");

// Create a new backup
router.post("/create", (req, res) => {
  const result = BackupManager.createBackup();
  res.json(result);
});

// List all backups
router.get("/list", (req, res) => {
  const result = BackupManager.listBackups();
  res.json(result);
});

// Restore a backup
router.post("/restore", (req, res) => {
  const { file } = req.body;

  if (!file) {
    return res.json({
      success: false,
      error: "Backup file name required"
    });
  }

  const loaded = BackupManager.loadBackup(file);

  if (!loaded.success) {
    return res.json(loaded);
  }

  try {
    Database.overwrite(loaded.data);
    Logger.event(`Backup restored from ${file}`);

    res.json({
      success: true,
      restoredFrom: file
    });
  } catch (err) {
    res.json({
      success: false,
      error: err.message
    });
  }
});

module.exports = router;