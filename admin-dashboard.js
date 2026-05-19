import { runHealthCheck } from "./system/health/health-check.js";
import { getPerformanceMetrics } from "./system/metrics/performance-metrics.js";
import { Logger } from "./system/logs/error-logger.js";
// You can wire real user data here later

const panels = {
  overview: document.getElementById("panel-overview"),
  health: document.getElementById("panel-health"),
  metrics: document.getElementById("panel-metrics"),
  logs: document.getElementById("panel-logs"),
  users: document.getElementById("panel-users")
};

const statusPill = document.getElementById("systemStatus");

document.querySelectorAll(".sidebar nav button").forEach(btn => {
  btn.addEventListener("click", () => {
    const target = btn.getAttribute("data-panel");
    switchPanel(target);
  });
});

function switchPanel(name) {
  document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
  document.getElementById(`panel-${name}`).classList.add("active");
}

async function renderHealth() {
  const health = await runHealthCheck();
  const allOnline = health.results.every(r => r.status === "online");

  statusPill.textContent = allOnline ? "All systems online" : "Issues detected";
  statusPill.classList.toggle("online", allOnline);
  statusPill.classList.toggle("offline", !allOnline);

  panels.health.innerHTML = `
    <div class="card">
      <h2>Service Status</h2>
      <table class="table">
        <thead>
          <tr><th>Service</th><th>Status</th><th>Error</th></tr>
        </thead>
        <tbody>
          ${health.results
            .map(
              r => `
            <tr>
              <td>${r.service}</td>
              <td><span class="badge ${r.status}">${r.status}</span></td>
              <td>${r.error || ""}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderMetrics() {
  const metrics = getPerformanceMetrics();
  panels.metrics.innerHTML = `
    <div class="card">
      <h2>Performance Metrics</h2>
      <p>CPU Load (1m): ${metrics.cpuLoad1m.toFixed(2)}</p>
      <p>CPU Load (5m): ${metrics.cpuLoad5m.toFixed(2)}</p>
      <p>CPU Load (15m): ${metrics.cpuLoad15m.toFixed(2)}</p>
      <p>Memory Used: ${(metrics.memory.used / 1024 / 1024).toFixed(1)} MB</p>
      <p>Uptime: ${metrics.uptimeSeconds} seconds</p>
    </div>
  `;
}

function renderOverview() {
  panels.overview.innerHTML = `
    <div class="card">
      <h2>Edge Tech Knowledgey Overview</h2>
      <p>Central control panel for internet, email, diagnostics, and user services.</p>
    </div>
  `;
}

function renderLogs() {
  // Placeholder: you can later read from log files via backend
  panels.logs.innerHTML = `
    <div class="card">
      <h2>Logs</h2>
      <p>Log viewer wiring goes here (backend endpoint to stream logs).</p>
    </div>
  `;
}

function renderUsers() {
  panels.users.innerHTML = `
    <div class="card">
      <h2>Users</h2>
      <p>User management UI goes here (list, roles, actions).</p>
    </div>
  `;
}

async function init() {
  renderOverview();
  renderMetrics();
  renderLogs();
  renderUsers();
  await renderHealth();
}

init();