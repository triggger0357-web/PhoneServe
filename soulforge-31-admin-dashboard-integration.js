// Soul Forge Admin Dashboard Integration (v1)

const path = require("path");

function integrateAdminDashboard(app) {
  const dashboardPath = path.join(__dirname, "soulforge-28-admin-dashboard.html");

  // Dashboard UI route
  app.get("/admin/dashboard", (req, res) => {
    res.sendFile(dashboardPath);
  });
}

module.exports = integrateAdminDashboard;