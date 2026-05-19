// Soul Forge Auth Routes (v1)

const express = require("express");
const router = express.Router();
const Auth = require("./soulforge-14-auth");

// Login route
router.post("/login", (req, res) => {
  const { username, password } = req.body;

  const result = Auth.login(username, password);
  res.json(result);
});

// Register route
router.post("/register", (req, res) => {
  const { username, password, role } = req.body;

  const result = Auth.register(username, password, role);
  res.json(result);
});

// List users
router.get("/users", (req, res) => {
  const users = Auth.listUsers();
  res.json({ users });
});

module.exports = router;