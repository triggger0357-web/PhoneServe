import manifest from "./upgrade-manifest.json" assert { type: "json" };

export function checkForUpdates(currentVersion) {
  return manifest.version !== currentVersion;
}