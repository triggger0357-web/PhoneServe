#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
echo "[+] Acoustic bootstrap successful! Launching PhoneServe..."
cd $HOME/PhoneServe
npm install
pm2 delete all 2>/dev/null
pm2 start server.js --name "phoneserve-core"
pm2 save --force
echo "[+] Node is live and permanent!"
