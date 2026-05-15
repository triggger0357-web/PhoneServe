// Soul Forge Metrics Collector (v1)

const fs = require("fs");
const path = require("path");
const Logger = require("./soulforge-11-logger");

const METRICS_FILE = path.join(__dirname, "soulforge-metrics.json");

// Ensure metrics file exists
if (!fs.existsSync(METRICS_FILE)) {
  fs.writeFileSync(METRICS_FILE, JSON.stringify({
    totalRequests: 0,
    perAI: {},
    timestamps: []
  }, null, 2));
}

const MetricsCollector = {
  load() {
    try {
      return JSON.parse(fs.readFileSync(METRICS_FILE, "utf8"));
    } catch (err) {
      Logger.error("Failed to load metrics: " + err.message);
      return null;
    }
  },

  save(data) {
    try {
      fs.writeFileSync(METRICS_FILE, JSON.stringify(data, null, 2));
    } catch (err) {
      Logger.error("Failed to save metrics: " + err.message);
    }
  },

  recordRequest(aiId) {
    const metrics = this.load();
    if (!metrics) return;

    metrics.totalRequests++;

    if (!metrics.perAI[aiId]) {
      metrics.perAI[aiId] = {
        requests: 0,
        lastUsed: null
      };
    }

    metrics.perAI[aiId].requests++;
    metrics.perAI[aiId].lastUsed = new Date().toISOString();

    metrics.timestamps.push({
      aiId,
      time: new Date().toISOString()
    });

    this.save(metrics);
    Logger.event(`Metrics updated for AI: ${aiId}`);
  },

  getSummary() {
    return this.load();
  }
};

module.exports = MetricsCollector;