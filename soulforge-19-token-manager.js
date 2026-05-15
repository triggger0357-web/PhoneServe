// Soul Forge Token Manager (v1)

const crypto = require("crypto");

const TokenManager = {
  activeTokens: {},

  create(username, role) {
    const token = crypto.randomBytes(24).toString("hex");

    this.activeTokens[token] = {
      username,
      role,
      createdAt: Date.now()
    };

    return token;
  },

  validate(token) {
    return this.activeTokens[token] || null;
  },

  revoke(token) {
    delete this.activeTokens[token];
  },

  list() {
    return Object.keys(this.activeTokens).map(t => ({
      token: t,
      username: this.activeTokens[t].username,
      role: this.activeTokens[t].role,
      createdAt: this.activeTokens[t].createdAt
    }));
  }
};

module.exports = TokenManager;