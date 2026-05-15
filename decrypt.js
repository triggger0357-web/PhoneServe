import crypto from "crypto";

export function decrypt(encrypted, key, iv) {
  const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
  return decipher.update(encrypted, "hex", "utf8") + decipher.final("utf8");
}