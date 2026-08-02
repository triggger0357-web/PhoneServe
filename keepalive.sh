#!/data/data/com.termux/files/usr/bin/bash
cd ~/PhoneServe
while true; do
  pgrep -f etk_mail_server.py || nohup python etk_mail_server.py > iron.log 2>&1 &
  pgrep -f public_portal.py || nohup python public_portal.py > portal.log 2>&1 &
  pgrep -f "etk:80:localhost:3000" || nohup ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R etk:80:localhost:3000 serveo.net > serveo.log 2>&1 &
  sleep 15
done
