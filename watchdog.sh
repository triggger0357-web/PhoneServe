#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  ETK Node Watchdog + Active Health Check
#  Edge Tech Knowledgey — VAN-WA-PRIMARY-01
#  Usage: bash watchdog.sh
# ─────────────────────────────────────────────────────────────────────────────

NODE_DIR="$HOME/PhoneServe"
LOG_FILE="$NODE_DIR/watchdog.log"
TUNNEL_LOG="$NODE_DIR/tunnel.log"
PORT=3002
RESTART_DELAY=5

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "[*] Acquiring wake lock..."
termux-wake-lock 2>/dev/null || log "[~] Wake lock unavailable (install termux-api if needed)"

cd "$NODE_DIR" || { log "[!] Cannot find PhoneServe directory"; exit 1; }

# Truncate log to keep last 200 lines on restart
if [ -f "$LOG_FILE" ]; then
  tail -n 200 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

log "╔══════════════════════════════════════╗"
log "║  ETK Watchdog Starting (Active Ping) ║"
log "║  Node: VAN-WA-PRIMARY-01             ║"
log "╚══════════════════════════════════════╝"

log "[*] Clearing old processes..."
pkill -f "node server.js" 2>/dev/null
pkill -f "ssh.*serveo" 2>/dev/null
sleep 2

while true; do

  log "[*] Starting Node server..."
  node server.js >> "$LOG_FILE" 2>&1 &
  NODE_PID=$!
  log "[*] Node PID: $NODE_PID"
  sleep 3

  log "[*] Opening serveo tunnel..."
  ssh -o StrictHostKeyChecking=no \
      -o ServerAliveInterval=30 \
      -o ServerAliveCountMax=3 \
      -o ExitOnForwardFailure=yes \
      -R 80:localhost:$PORT serveo.net > "$TUNNEL_LOG" 2>&1 &
  TUNNEL_PID=$!
  log "[*] Tunnel PID: $TUNNEL_PID"

  sleep 5
  TUNNEL_URL=$(grep -o 'https://[^ ]*serveousercontent.com' "$TUNNEL_LOG" | head -1)
  if [ -n "$TUNNEL_URL" ]; then
    log "[✓] Tunnel URL: $TUNNEL_URL"
    curl -s -X POST http://localhost:$PORT/api/register-tunnel \
      -H "Content-Type: application/json" \
      -d "{\"url\":\"$TUNNEL_URL\"}" > /dev/null
    log "[✓] Tunnel registered with node"
    echo ""
    echo "═══════════════════════════════════════"
    echo "  NODE ONLINE"
    echo "  $TUNNEL_URL"
    echo "  Admin: $TUNNEL_URL/admin.html"
    echo "═══════════════════════════════════════"
    echo ""
  else
    log "[!] Could not detect tunnel URL"
  fi

  # Active HTTP health check loop
  while true; do
    sleep 10

    # Active HTTP ping to local health route
    if ! curl -s --max-time 3 http://localhost:$PORT/api/health >/dev/null; then
      log "[!] Node unresponsive or memory degraded — restarting in ${RESTART_DELAY}s..."
      kill $TUNNEL_PID 2>/dev/null
      sleep $RESTART_DELAY
      break
    fi

    # Monitor SSH tunnel process
    if ! kill -0 $TUNNEL_PID 2>/dev/null; then
      log "[!] Tunnel dropped — restarting in ${RESTART_DELAY}s..."
      kill $NODE_PID 2>/dev/null
      sleep $RESTART_DELAY
      break
    fi
  done

  log "[*] Restarting processes..."
  pkill -f "node server.js" 2>/dev/null
  pkill -f "ssh.*serveo" 2>/dev/null
  sleep $RESTART_DELAY

done
