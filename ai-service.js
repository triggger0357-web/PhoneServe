import { generateBaseResponse } from "./ai-core.js";
import { adaptResponse } from "./personality-adapter.js";

export function askAI(prompt) {
  const base = generateBaseResponse(prompt);
  const styled = adaptResponse(base);
  return {
    prompt,
    response: styled,
    timestamp: new Date().toISOString()
  };
}