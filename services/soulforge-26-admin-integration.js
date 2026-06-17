// Soul Forge Admin API Integration Layer (v1)

const AdminAPI = require("./soulforge-25-admin-api");
const AuthMiddleware = require("./soulforge-16-auth-middleware");

function integrateAdminAPI(app) {
  // Protect all admin API routes
  app.use("/admin/api", (req, res, next) => {
    AuthMiddleware.requireAuth(req, res, next);
  });

  // Mount admin API
  app.use("/admin/api", AdminAPI);
}

module.exports = integrateAdminAPI;