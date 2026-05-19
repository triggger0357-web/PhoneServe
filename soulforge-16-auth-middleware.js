// Soul Forge Auth Middleware (v1)

const Auth = require("./soulforge-14-auth");

const activeTokens = {};

const AuthMiddleware = {
  // Validate token
  requireAuth(req, res, next) {
    const token = req.headers["x-auth-token"];

    if (!token || !activeTokens[token]) {
      return res.status(401).json({
        success: false,
        error: "Unauthorized"
      });
    }

    req.user = activeTokens[token];
    next();
  },

  // Login handler to store token
  registerToken(username, role, token) {
    activeTokens[token] = { username, role };
  },

  // Logout handler
  logout(token) {
    delete activeTokens[token];
  }
};

module.exports = AuthMiddleware;