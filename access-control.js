import { Permissions } from "./role-permissions.js";

export function canAccess(role, action) {
  return Permissions[role]?.includes(action) || false;
}