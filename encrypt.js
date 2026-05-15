import crypto from "crypto";

const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);

export function encrypt(text) {
  const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
  return cipher.update(text, "utf8", "hex") + cipher.final("hex");
}