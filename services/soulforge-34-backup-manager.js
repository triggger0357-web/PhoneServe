// Soul Forge Backup Manager (v1)

const fs = require("fs");
const path = require("path");
const Logger = require("./soulforge-11-logger");

const BACKUP_DIR = path.join(__dirname, "backups");

// Ensure backup directory exists
if (!fs.existsSync(BACKUP_DIR)) {
  fs.mkdirSync(BACKUP_DIR);
}

const BackupManager = {
  createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const backupFile = path.join(BACKUP_DIR, `soulforge-backup-${timestamp}.json`);

    try {
      const dbPath = path.join(__dirname, "soulforge-db.json");
      const data = fs.readFileSync(dbPath, "utf8");

      fs.writeFileSync(backupFile, data);

      Logger.event(`Backup created: ${backupFile}`);

      return {
        success: true,
        file: backupFile
      };
    } catch (err) {
      Logger.error("Backup failed: " + err.message);
      return {
        success: false,
        error: err.message
      };
    }
  },

  listBackups() {
    try {
      const files = fs.readdirSync(BACKUP_DIR)
        .filter(f => f.endsWith(".json"))
        .map(f => ({
          file: f,
          path: path.join(BACKUP_DIR, f)
        }));

      return {
        success: true,
        backups: files
      };
    } catch (err) {
      return {
        success: false,
        error: err.message
      };
    }
  },

  loadBackup(fileName) {
    try {
      const filePath = path.join(BACKUP_DIR, fileName);

      if (!fs.existsSync(filePath)) {
        return {
          success: false,
          error: "Backup file not found"
        };
      }

      const data = fs.readFileSync(filePath, "utf8");
      return {
        success: true,
        data: JSON.parse(data)
      };
    } catch (err) {
      return {
        success: false,
        error: err.message
      };
    }
  }
};

module.exports = BackupManager;