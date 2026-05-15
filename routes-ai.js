const express = require('express');
const router = express.Router();

router.post('/task', async (req, res) => {
  const { request } = req.body;

  // Simple AI logic (expand later)
  let response = "";

  if (request.includes("email")) {
    response = "I can help you set up email or send automated messages.";
  } else if (request.includes("internet")) {
    response = "I can activate or diagnose your internet service.";
  } else if (request.includes("webspace")) {
    response = "I can create, edit, or manage your webspace files.";
  } else if (request.includes("diagnose")) {
    response = "Running diagnostics now.";
  } else {
    response = "I understand your request. I will perform the task.";
  }

  res.json({ result: response });
});

module.exports = router;