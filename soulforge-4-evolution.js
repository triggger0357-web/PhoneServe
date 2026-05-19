// Soul Forge Evolution Engine (v1)

const SoulForge = require("./soulforge-1-core");

const EvolutionEngine = {
  evolveAI(aiId, track, amount = 1) {
    return SoulForge.evolve(aiId, track, amount);
  },

  getEvolutionState(aiId) {
    const ai = SoulForge.getAIState(aiId);
    return ai.evolution || {
      technical: 0,
      creative: 0,
      safety: 0,
      operational: 0
    };
  },

  autoEvolve(aiId, actionType) {
    const map = {
      "email_generation": "creative",
      "data_processing": "technical",
      "safety_check": "safety",
      "task_execution": "operational"
    };

    const track = map[actionType];
    if (!track) return { success: false, error: "Unknown action type" };

    return SoulForge.evolve(aiId, track, 1);
  }
};

module.exports = EvolutionEngine;