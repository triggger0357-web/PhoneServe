import { loadSystem } from "./system-loader.js";

export function launch() {
  const system = loadSystem();
  return {
    message: "Edge Tech Knowledgey Platform Online",
    system
  };
}