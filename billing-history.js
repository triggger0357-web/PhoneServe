export const BillingHistory = {
  records: [],

  add(record) {
    this.records.push(record);
  },

  list(userId) {
    return this.records.filter(r => r.userId === userId);
  }
};