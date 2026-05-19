import profiles from "./personality-profiles.json" assert { type: "json" };
import { Personality } from "./personality-core.js";

export function loadProfile(name) {
  const profile = profiles[name] || profiles["default"];
  Object.assign(Personality, profile);
  return Personality;
}