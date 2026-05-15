function loadTokens() {
  fetch("/auth/manage/tokens", {
    headers: { "x-auth-token": token }
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById("tokensOut").textContent = JSON.stringify(d, null, 2);
  });
}

function revoke() {
  fetch("/auth/manage/tokens/revoke", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-auth-token": token
    },
    body: JSON.stringify({
      token: document.getElementById("revokeInput").value
    })
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById("revokeOut").textContent = JSON.stringify(d, null, 2);
  });
}

function loadAIs() {
  fetch("/admin/api/ais", {
    headers: { "x-auth-token": token }
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById("aisOut").textContent = JSON.stringify(d, null, 2);
  });
}

function loadLogs() {
  fetch("/admin/api/logs", {
    headers: { "x-auth-token": token }
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById("logsOut").textContent = JSON.stringify(d, null, 2);
  });
}

function saveAI() {
  fetch("/admin/api/save-ai", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-auth-token": token
    },
    body: JSON.stringify({
      aiId: document.getElementById("aiId").value,
      aiData: JSON.parse(document.getElementById("aiData").value)
    })
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById("saveOut").textContent = JSON.stringify(d, null, 2);
  });
}