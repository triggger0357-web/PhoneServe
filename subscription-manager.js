import plans from "./subscription-plans.json" assert { type: "json" };

export const Subscriptions = {
  active: {},

  assign(userId, plan) {
    this.active[userId] = { plan, since: Date.now() };
  },

  get(userId) {
    return this.active[userId] || { plan: "free" };
  }
};