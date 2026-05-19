// Soul Forge System Health Monitor (v1)

const os = require("os");
const fs = require("fs");
const path = require("path");
const Logger = require("./soulforge-11-logger");

const HealthMonitor = {
  getCPU() {
    const cpus = os.cpus();
    let totalIdle = 0;
    let totalTick = 0;

    cpus.forEach(cpu => {
      for (let type in cpu.times) {
        totalTick += cpu.times[type];
      }
      totalIdle += cpu.times.idle;
    });

    const idle = totalIdle / cpus.length;
    const total = totalTick / cpus.length;

    const usage = 1 - idle / total;

    return Number((usage * 100).toFixed(2));
  },

  getMemory() {
    const total = os.totalmem();
    const free = os.freemem();
    const used = total - free;

    return {
      total,
      free,
      used,
      percentUsed: Number(((used / total) * 100).toFixed(2))
    };
  },

  getDisk() {
    try {
      const stat = fs.statSync(path.join(__dirname, "soulforge-db.json"));
      return {
        dbSizeBytes: stat.size
      };
    } catch (err) {
      return {
        dbSizeBytes: 0
      };
    }
  },

  getUptime() {
    return os.uptime();
  },

  getStatus() {
    const cpu = this.getCPU();
    const mem = this.getMemory();
    const disk = this.getDisk();
    const uptime = this.getUptime();

    const status = {
      cpuPercent: cpu,
      memory: mem,
      disk,
      uptimeSeconds: uptime,
      timestamp: new Date().toISOString()
    };

    Logger.event("System health check executed");

    return status;
  }
};

module.exports = HealthMonitor;