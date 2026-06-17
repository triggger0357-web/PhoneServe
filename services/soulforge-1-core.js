// Soul Forge Core Engine (v1)

const AIs = {
  wreckoning: {
    tier: 1,
    personality: "guardian",
    upgrades: [],
    evolution: {
      technical: 0,
      creative: 0,
      safety: 0,
      operational: 0
    }
  }
};

const upgradesCatalog = [
  { id: "tier2_ops", name: "Operational Tier II", cost: 10 },
  { id: "tier3_research", name: "Research Suite", cost: 25 },
  { id: "tier4_advanced", name: "Advanced Intelligence Tier IV", cost: 50 }
];

const personalitiesCatalog = [
  { id: "guardian", label: "Guardian", traits: ["cautious", "safety-first"] },
  { id: "navigator", label: "Navigator", traits: ["strategic", "planner"] },
  { id: "artisan", label: "Artisan", traits: ["creative", "expressive"] },
  { id: "oracle", label: "Oracle", traits: ["analytical", "insight-heavy"] }
];

const SoulForge = {
  listAvailableUpgrades(aiId) {
    return upgradesCatalog;
  },

  applyUpgrade(aiId, upgradeId) {
    const ai = AIs[aiId] || (AIs[aiId] = {
      tier: 1,
      personality: "guardian",
      upgrades: [],
      evolution: { technical: 0, creative: 0, safety: 0, operational: 0 }
    });

    if (!ai.upgrades.includes(upgradeId)) {
      ai.upgrades.push(upgradeId);
    }

    return { success: true, ai };
  },

  listPersonalityProfiles() {
    return personalitiesCatalog;
  },

  assignPersonality(aiId, personalityId) {
    const ai = AIs[aiId] || (AIs[aiId] = {
      tier: 1,
      personality: "guardian",
      upgrades: [],
      evolution: { technical: 0, creative: 0, safety: 0, operational: 0 }
    });

    ai.personality = personalityId;
    return { success: true, ai };
  },

  evolve(aiId, track, amount = 1) {
    const ai = AIs[aiId];
    if (!ai) return { success: false, error: "AI not found" };

    if (!ai.evolution[track]) ai.evolution[track] = 0;
    ai.evolution[track] += amount;

    return { success: true, ai };
  },

  checkPermission(aiId, action) {
    return { allowed: true, reason: "within policy" };
  },

  getAIState(aiId) {
    return AIs[aiId] || {
      tier: 1,
      personality: "guardian",
      upgrades: [],
      evolution: { technical: 0, creative: 0, safety: 0, operational: 0 }
    };
  }
};

module.exports = SoulForge;