#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════════
# ETK AUTO-BOOT SCRIPT
# Edge Tech Knowledgey // Sovereign Infrastructure
# Runs automatically when your Moto G Stylus powers on
# 
# Setup:
#   1. Install Termux from F-Droid
#   2. Install Termux:Boot from F-Droid
#   3. Copy this file to ~/.termux/boot/boot.sh
#   4. chmod +x ~/.termux/boot/boot.sh
#   5. Open Termux:Boot app once to enable it
# ═══════════════════════════════════════════════════════════

# Wait for Android to finish booting
sleep 10

# Log file
LOG="$HOME/etk_boot.log"
echo "═══════════════════════════════════" >> $LOG
echo "ETK Boot: $(date)" >> $LOG
echo "═══════════════════════════════════" >> $LOG

# Wake lock — keep CPU alive
termux-wake-lock

# ── START MESH GATEWAY (port 1080 + status 8080) ───────────
echo "[ETK] Starting Mesh Gateway..." >> $LOG
if [ -f "$HOME/PhoneServe/mesh_gateway.py" ]; then
    python3 "$HOME/PhoneServe/mesh_gateway.py" >> "$HOME/mesh_gateway.log" 2>&1 &
    MESH_PID=$!
    echo "[ETK] Mesh Gateway PID: $MESH_PID" >> $LOG
else
    echo "[ETK] mesh_gateway.py not found — skipping" >> $LOG
fi

sleep 2

# ── START ETK MAIL SERVER (port 8025 + api 8585) ──────────
echo "[ETK] Starting Mail Server..." >> $LOG
if [ -f "$HOME/PhoneServe/etk_mail_server.py" ]; then
    python3 "$HOME/PhoneServe/etk_mail_server.py" >> "$HOME/mail_server.log" 2>&1 &
    MAIL_PID=$!
    echo "[ETK] Mail Server PID: $MAIL_PID" >> $LOG
else
    echo "[ETK] etk_mail_server.py not found — skipping" >> $LOG
fi

sleep 2

# ── SAVE PIDS FOR MONITORING ───────────────────────────────
echo $MESH_PID > "$HOME/etk_pids.txt"
echo $MAIL_PID >> "$HOME/etk_pids.txt"

echo "[ETK] All services started" >> $LOG
echo "[ETK] Mesh Gateway : 127.0.0.1:1080 (proxy) + :8080 (status)" >> $LOG
echo "[ETK] Mail Server  : 127.0.0.1:8025 (smtp) + :8585 (api)" >> $LOG

# ── KEEP TERMUX ALIVE ──────────────────────────────────────
# This loop keeps the session active and monitors services
while true; do
    sleep 60

    # Check mesh gateway still running
    if ! kill -0 $MESH_PID 2>/dev/null; then
        echo "[ETK] Mesh Gateway crashed — restarting at $(date)" >> $LOG
        python3 "$HOME/PhoneServe/mesh_gateway.py" >> "$HOME/mesh_gateway.log" 2>&1 &
        MESH_PID=$!
    fi

    # Check mail server still running
    if ! kill -0 $MAIL_PID 2>/dev/null; then
        echo "[ETK] Mail Server crashed — restarting at $(date)" >> $LOG
        python3 "$HOME/PhoneServe/etk_mail_server.py" >> "$HOME/mail_server.log" 2>&1 &
        MAIL_PID=$!
    fi

done
