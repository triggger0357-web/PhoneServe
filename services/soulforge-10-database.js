// Soul Forge Simple In‑Memory Database (v1)

const fs = require("fs");
const path = require("path");

const DB_PATH = path.join(__dirname, "soulforge-db.json");

// Initialize DB file if missing
function initDB() {
  if (!fs.existsSync(DB_PATH)) {
    fs.writeFileSync(
      DB_PATH,
      JSON.stringify(
        {
          AIs: {},
          logs: []
        },
        null,
        2
      )
    );
  }
}

initDB();

function loadDB() {
  return JSON.parse(fs.readFileSync(DB_PATH, "utf8"));
}

function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2));
}

const Database = {
  getAI(aiId) {
    const db = loadDB();
    return db.AIs[aiId] || null;
  },

  saveAI(aiId, aiData) {
    const db = loadDB();
    db.AIs[aiId] = aiData;
    saveDB(db);
    return true;
  },

  logEvent(event) {
    const db = loadDB();
    db.logs.push({
      event,
      timestamp: Date.now()
    });
    saveDB(db);
  },

  getLogs(limit = 50) {
    const db = loadDB();
    return db.logs.slice(-limit);
  }
};

module.exports = Database;