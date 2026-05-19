// system/logs/error-logger.js

import fs from "fs";
import path from "path";

export function log(level, message) {
  const date = new Date();
  const fileName = `${date.toISOString().split("T")[0]}.log`;
  const logPath = path.join("logs", fileName);

  const entry = `[${date.toISOString()}] [${level}] ${message}\n`;

  fs.appendFileSync(logPath, entry);
}

export const Logger = {
  info: (msg) => log("INFO", msg),
  warn: (msg) => log("WARN", msg),
  error: (msg) => log("ERROR", msg),
  critical: (msg) => log("CRITICAL", msg)
};