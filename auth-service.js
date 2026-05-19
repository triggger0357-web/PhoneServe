import { UserModel } from "./user-model.js";

export function authenticate(username, password) {
  const user = UserModel.find(username);
  if (!user) return null;
  return user.password === password ? user : null;
}