// system/metrics/performance-metrics.js

import os from "os";

export function getPerformanceMetrics() {
  const load = os.loadavg();
  const memory = {
    total: os.totalmem(),
    free: os.freemem(),
    used: os.totalmem() - os.freemem()
  };

  return {
    timestamp: new Date().toISOString(),
    cpuLoad1m: load[0],
    cpuLoad5m: load[1],
    cpuLoad15m: load[2],
    memory,
    uptimeSeconds: os.uptime(),
    platform: os.platform()
  };
}