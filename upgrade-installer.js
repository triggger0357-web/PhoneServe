export function installUpgrade(version) {
  return {
    status: "installed",
    version,
    timestamp: Date.now()
  };
}