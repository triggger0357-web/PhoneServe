#!/data/data/com.termux/files/usr/bin/bash
cd ~/PhoneServe

# Kill old
pkill -f etk_mail_server; pkill -f mesh_gateway; pkill -f "http.server 3000" 2>/dev/null
fuser -k 1080/tcp 2>/dev/null; fuser -k 8585/tcp 2>/dev/null; fuser -k 8025/tcp 2>/dev/null; fuser -k 3000/tcp 2>/dev/null
sleep 1

# Start Iron Core (mail + api)
nohup python etk_mail_server.py >> etk_mail.log 2>&1 &
echo "[+] Iron Core :8585 :8025"

# Start Gateway (if you use it - safe to fail)
nohup python core/gateway/mesh_gateway_hardened.py >> mesh_gateway.log 2>&1 &
echo "[+] Gateway :1080"

# Start Public Portal :3000
nohup python -m http.server 3000 --directory public >> portal.log 2>&1 &
echo "[+] Portal :3000"

sleep 2
echo ""
echo "=== STATUS ==="
curl -s http://127.0.0.1:8585/api/accounts | head -c 200
echo ""
ps aux | grep -E "etk|gateway|http.server" | grep -v grep
