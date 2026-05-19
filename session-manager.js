export const Sessions = {
  active: {},

  create(userId) {
    const token = Math.random().toString(36).slice(2);
    this.active[token] = { userId, created: Date.now() };
    return token;
  },

  validate(token) {
    return this.active[token] || null;
  }
};