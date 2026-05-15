export const Personality = {
  tone: "professional",
  energy: "medium",
  style: "direct",

  apply(message) {
    return `[${this.tone.toUpperCase()} | ${this.energy}] ${message}`;
  }
};