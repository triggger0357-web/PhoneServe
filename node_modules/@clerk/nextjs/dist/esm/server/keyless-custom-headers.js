"use server";
import "../chunk-BUSYA2B4.js";
import { headers } from "next/headers";
async function collectKeylessMetadata() {
  var _a, _b, _c, _d, _e, _f;
  const headerStore = await headers();
  return {
    nodeVersion: process.version,
    nextVersion: getNextVersion(),
    npmConfigUserAgent: process.env.npm_config_user_agent,
    // eslint-disable-line
    userAgent: (_a = headerStore.get("User-Agent")) != null ? _a : "unknown user-agent",
    port: process.env.PORT,
    // eslint-disable-line
    host: (_b = headerStore.get("host")) != null ? _b : "unknown host",
    xPort: (_c = headerStore.get("x-forwarded-port")) != null ? _c : "unknown x-forwarded-port",
    xHost: (_d = headerStore.get("x-forwarded-host")) != null ? _d : "unknown x-forwarded-host",
    xProtocol: (_e = headerStore.get("x-forwarded-proto")) != null ? _e : "unknown x-forwarded-proto",
    xClerkAuthStatus: (_f = headerStore.get("x-clerk-auth-status")) != null ? _f : "unknown x-clerk-auth-status",
    isCI: detectCIEnvironment()
  };
}
const CI_ENV_VARS = [
  "CI",
  "CONTINUOUS_INTEGRATION",
  "BUILD_NUMBER",
  "BUILD_ID",
  "BUILDKITE",
  "CIRCLECI",
  "GITHUB_ACTIONS",
  "GITLAB_CI",
  "JENKINS_URL",
  "TRAVIS",
  "APPVEYOR",
  "WERCKER",
  "DRONE",
  "CODESHIP",
  "SEMAPHORE",
  "SHIPPABLE",
  "TEAMCITY_VERSION",
  "BAMBOO_BUILDKEY",
  "GO_PIPELINE_NAME",
  "TF_BUILD",
  "SYSTEM_TEAMFOUNDATIONCOLLECTIONURI",
  "BITBUCKET_BUILD_NUMBER",
  "HEROKU_TEST_RUN_ID",
  "VERCEL",
  "NETLIFY"
];
function detectCIEnvironment() {
  const ciIndicators = CI_ENV_VARS;
  const falsyValues = /* @__PURE__ */ new Set(["", "false", "0", "no"]);
  return ciIndicators.some((indicator) => {
    const value = process.env[indicator];
    if (value === void 0) {
      return false;
    }
    const normalizedValue = value.trim().toLowerCase();
    return !falsyValues.has(normalizedValue);
  });
}
function getNextVersion() {
  var _a;
  try {
    return (_a = process.title) != null ? _a : "unknown-process-title";
  } catch {
    return void 0;
  }
}
async function formatMetadataHeaders(metadata) {
  const headers2 = new Headers();
  if (metadata.nodeVersion) {
    headers2.set("Clerk-Node-Version", metadata.nodeVersion);
  }
  if (metadata.nextVersion) {
    headers2.set("Clerk-Next-Version", metadata.nextVersion);
  }
  if (metadata.npmConfigUserAgent) {
    headers2.set("Clerk-NPM-Config-User-Agent", metadata.npmConfigUserAgent);
  }
  if (metadata.userAgent) {
    headers2.set("Clerk-Client-User-Agent", metadata.userAgent);
  }
  if (metadata.port) {
    headers2.set("Clerk-Node-Port", metadata.port);
  }
  if (metadata.host) {
    headers2.set("Clerk-Client-Host", metadata.host);
  }
  if (metadata.xPort) {
    headers2.set("Clerk-X-Port", metadata.xPort);
  }
  if (metadata.xHost) {
    headers2.set("Clerk-X-Host", metadata.xHost);
  }
  if (metadata.xProtocol) {
    headers2.set("Clerk-X-Protocol", metadata.xProtocol);
  }
  if (metadata.xClerkAuthStatus) {
    headers2.set("Clerk-Auth-Status", metadata.xClerkAuthStatus);
  }
  if (metadata.isCI) {
    headers2.set("Clerk-Is-CI", "true");
  }
  return headers2;
}
export {
  collectKeylessMetadata,
  formatMetadataHeaders
};
//# sourceMappingURL=keyless-custom-headers.js.map