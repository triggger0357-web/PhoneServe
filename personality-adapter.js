import { Personality } from "./personality-core.js";

export function adaptResponse(text) {
  return Personality.apply(text);
}