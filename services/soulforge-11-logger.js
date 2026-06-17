// Soul Forge Logger (v1)

const fs = require("fs");
const path = require("path");

const LOG_PATH = path.join(__dirname, "soulforge-events.log");

function write(line) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${line}\n`;
  fs.appendFileSync(LOG_PATH, entry);
}

const Logger = {
  event(message) {
    write("EVENT: " + message);
  },

  action(aiId, actionType) {
    write(`ACTION: AI=${aiId} performed=${actionType}`);
  },

  upgrade(aiId, upgradeId) {
    write(`UPGRADE: AI=${aiId} applied=${upgradeId}`);
  },

  personality(aiId, personalityId) {
    write(`PERSONALITY: AI=${aiId} set=${personalityId}`);
  },

  error(message) {
    write("ERROR: " + message);
  }
};

module.exports = Logger;