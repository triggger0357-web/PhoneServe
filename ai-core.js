export function generateBaseResponse(prompt) {
  // Placeholder logic — later you can swap in a real model/API
  if (prompt.toLowerCase().includes("status")) {
    return "System is operational with minor background tasks running.";
  }
  if (prompt.toLowerCase().includes("help")) {
    return "I can assist with diagnostics, status summaries, and user insights.";
  }
  return `You said: "${prompt}". I have recorded and interpreted this input.`;
}