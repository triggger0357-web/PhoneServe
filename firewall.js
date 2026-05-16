import rules from "./firewall-rules.json" assert { type: "json" };

export function isAllowed(service) {
  return rules.allow.includes(service);
}