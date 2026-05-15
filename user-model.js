export const UserModel = {
  users: [],

  create(username, password) {
    const user = { id: Date.now(), username, password, role: "user" };
    this.users.push(user);
    return user;
  },

  find(username) {
    return this.users.find(u => u.username === username);
  }
};