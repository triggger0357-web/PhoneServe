// system/health/health-check.js

const services = [
  { name: "internet-service", url: "http://localhost:5000/status" },
  { name: "email-service", url: "http://localhost:5001/status" },
  { name: "admin-portal", url: "http://localhost:5002/status" },
  { name: "diagnostics", url: "http://localhost:5003/status" },
  { name: "user-dashboard", url: "http://localhost:5004/status" }
];

async function checkService(service) {
  try {
    const response = await fetch(service.url);
    if (!response.ok) throw new Error("Service returned non-OK status");
    return { service: service.name, status: "online" };
  } catch (err) {
    return { service: service.name, status: "offline", error: err.message };
  }
}

export async function runHealthCheck() {
  const results = await Promise.all(services.map(checkService));
  return {
    timestamp: new Date().toISOString(),
    results
  };
}