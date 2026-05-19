// Soul Forge Basic Auth System (v1)

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const AUTH_PATH = path.join(__dirname, "soulforge-users.json");

// Initialize user database if missing
function initAuthDB() {
  if (!fs.existsSync(AUTH_PATH)) {
    fs.writeFileSync(
      AUTH_PATH,
      JSON.stringify(
        {
          users: {
            admin: {
              passwordHash: hash("admin123"),
              role: "owner"
            }
          }
        },
        null,
        2
      )
    );
  }
}

initAuthDB();

function loadUsers() {
  return JSON.parse(fs.readFileSync(AUTH_PATH, "utf8"));
}

function saveUsers(data) {
  fs.writeFileSync(AUTH_PATH, JSON.stringify(data, null, 2));
}

function hash(str) {
  return crypto.createHash("sha256").update(str).digest("hex");
}

const Auth = {
  login(username, password) {
    const db = loadUsers();
    const user = db.users[username];

    if (!user) {
      return { success: false, error: "User not found" };
    }

    if (user.passwordHash !== hash(password)) {
      return { success: false, error: "Invalid password" };
    }

    return {
      success: true,
      username,
      role: user.role,
      token: crypto.randomBytes(24).toString("hex")
    };
  },

  register(username, password, role = "user") {
    const db = loadUsers();

    if (db.users[username]) {
      return { success: false, error: "User already exists" };
    }

    db.users[username] = {
      passwordHash: hash(password),
      role
    };

    saveUsers(db);

    return { success: true, username, role };
  },

  listUsers() {
    const db = loadUsers();
    return Object.keys(db.users).map(u => ({
      username: u,
      role: db.users[u].role
    }));
  }
};

module.exports = Auth;