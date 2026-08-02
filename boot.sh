#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/PhoneServe
fuser -k 3000/tcp 2>/dev/null; fuser -k 8025/tcp 2>/dev/null; fuser -k 8080/tcp 2>/dev/null; fuser -k 8585/tcp 2>/dev/null; fuser -k 1080/tcp 2>/dev/null
sleep 1
node server.js >> server.log 2>&1 &
python core/gateway/mesh_gateway_hardened.py >> mesh_gateway.log 2>&1 &
python etk_mail_server.py >> etk_mail.log 2>&1 &
echo "ETK Iron Core booted"
ps aux | grep -E "server|mesh|mail" | grep -v grep
