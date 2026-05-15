// Soul Forge Action Handler (v1)

const SoulForge = require("./soulforge-1-core");
const EvolutionRules = require("./soulforge-7-evolution-rules.json");

const ActionEngine = {
  performAction(aiId, actionType) {
    const track = EvolutionRules.actions[actionType];

    if (!track) {
      return {
        success: false,
        error: "Unknown action type: " + actionType
      };
    }

    // Apply evolution gain
    const result = SoulForge.evolve(aiId, track, 1);

    return {
      success: true,
      action: actionType,
      evolvedTrack: track,
      ai: result.ai
    };
  },

  listActions() {
    return Object.keys(EvolutionRules.actions).map(a => ({
      action: a,
      evolves: EvolutionRules.actions[a]
    }));
  }
};

module.exports = ActionEngine;