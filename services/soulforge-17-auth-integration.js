// Soul Forge Auth Integration Layer (v1)

const AuthRoutes = require("./soulforge-15-auth-routes");
const AuthMiddleware = require("./soulforge-16-auth-middleware");
const express = require("express");

function integrateAuth(app) {
  // Public auth routes
  app.use("/auth", AuthRoutes);

  // Protect all Soul Forge API routes
  app.use("/api/soulforge", (req, res, next) => {
    AuthMiddleware.requireAuth(req, res, next);
  });
}

module.exports = integrateAuth;