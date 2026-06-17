// Soul Forge Token Integration Layer (v1)

const TokenRoutes = require("./soulforge-20-token-routes");
const TokenManager = require("./soulforge-19-token-manager");
const Auth = require("./soulforge-14-auth");
const AuthMiddleware = require("./soulforge-16-auth-middleware");
const express = require("express");

function integrateTokens(app) {
  // Public route to exchange login for token
  app.post("/auth/token-login", (req, res) => {
    const { username, password } = req.body;

    const result = Auth.login(username, password);

    if (!result.success) {
      return res.json(result);
    }

    const token = TokenManager.create(username, result.role);

    AuthMiddleware.registerToken(username, result.role, token);

    res.json({
      success: true,
      username,
      role: result.role,
      token
    });
  });

  // Token management routes (protected)
  app.use("/auth/manage", (req, res, next) => {
    AuthMiddleware.requireAuth(req, res, next);
  });

  app.use("/auth/manage", TokenRoutes);
}

module.exports = integrateTokens;