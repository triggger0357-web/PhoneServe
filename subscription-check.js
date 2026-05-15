import { Subscriptions } from "./subscription-manager.js";

export function hasAccess(userId, requiredPlan) {
  const userPlan = Subscriptions.get(userId).plan;
  const order = ["free", "pro", "enterprise"];
  return order.indexOf(userPlan) >= order.indexOf(requiredPlan);
}