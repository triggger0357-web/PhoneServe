export function processPayment(userId, amount) {
  return {
    userId,
    amount,
    status: "success",
    timestamp: Date.now()
  };
}