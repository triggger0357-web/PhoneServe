import crypto from "crypto";

export function hash(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}