"""
PhoneServe Mesh Network - Browser Proxy Gateway
Edge Tech Knowledgey // Sovereign Infrastructure
Port: 127.0.0.1:1080
"""

import asyncio
import logging
import urllib.parse
import json
import time
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ETK-MeshGateway")

LOCAL_HOST  = "127.0.0.1"
LOCAL_PORT  = 1080
STATUS_PORT = 8080   # Status/health API for the browser frontend
BUFFER_SIZE = 8192

# ── NODE REGISTRY ──────────────────────────────────────────────────────────────
# Add your live node IDs + addresses here.
# Format: "mesh-hostname" -> ("ip", port)
MESH_NODE_REGISTRY = {
    "phoneserve.node":   ("127.0.0.1", 9001),
    "void-odyssey.node": ("127.0.0.1", 9002),
    "ai-suite.node":     ("127.0.0.1", 9003),
    "etk-tokens.node":   ("127.0.0.1", 9004),
    # Add remote nodes:
    # "nyc-01.node": ("X.X.X.X", 9001),
}

# ── TELEMETRY ──────────────────────────────────────────────────────────────────
stats = {
    "requests_total":  0,
    "mesh_routed":     0,
    "clearweb_routed": 0,
    "errors":          0,
    "started_at":      time.time(),
    "node_id":         "ETK-" + hashlib.sha256(b"phoneserve-local").hexdigest()[:8].upper(),
    "peers":           len(MESH_NODE_REGISTRY),
}

# ── MESH ROUTING ───────────────────────────────────────────────────────────────
async def resolve_mesh_route(hostname: str):
    """
    Returns (ip, port) if hostname belongs to the ETK mesh network.
    Otherwise returns None to fall through to clear-web.
    """
    # Direct registry lookup
    if hostname in MESH_NODE_REGISTRY:
        logger.info(f"[MESH] Internal route matched: {hostname}")
        stats["mesh_routed"] += 1
        return MESH_NODE_REGISTRY[hostname]

    # .mesh / .node TLD — route to gateway itself for DHT resolution
    if hostname.endswith(".mesh") or hostname.endswith(".node"):
        logger.info(f"[MESH] DHT resolution needed for: {hostname}")
        stats["mesh_routed"] += 1
        # TODO: plug in Kademlia DHT lookup here
        # result = await kademlia_lookup(hostname)
        # return result
        return None

    # ETK sovereign domains
    if hostname.endswith(".etk") or hostname.endswith(".sovereign"):
        logger.info(f"[MESH] Sovereign domain: {hostname}")
        stats["mesh_routed"] += 1
        return None

    return None

# ── TRAFFIC TUNNEL ─────────────────────────────────────────────────────────────
async def tunnel_traffic(reader, writer):
    """Bi-directional pipe between browser and target."""
    try:
        while True:
            data = await reader.read(BUFFER_SIZE)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.close()
        except Exception:
            pass

# ── REQUEST HANDLER ────────────────────────────────────────────────────────────
async def handle_browser_client(local_reader, local_writer):
    """Parse browser request → route via mesh or clear-web."""
    stats["requests_total"] += 1
    try:
        request_line = await local_reader.readline()
        if not request_line:
            local_writer.close()
            return

        request_str = request_line.decode('utf-8', errors='ignore').strip()
        words = request_str.split()
        if len(words) < 2:
            local_writer.close()
            return

        method, url = words[0], words[1]

        if method == "CONNECT":
            parts    = url.split(":")
            hostname = parts[0]
            port     = int(parts[1]) if len(parts) > 1 else 443
        else:
            parsed   = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            port     = parsed.port if parsed.port else 80

        if not hostname:
            local_writer.close()
            return

        logger.info(f"[PROXY] {method} {hostname}:{port}")

        # Try mesh route first
        mesh_route = await resolve_mesh_route(hostname)

        if mesh_route:
            target_host, target_port = mesh_route
            logger.info(f"[MESH] Tunneling {hostname} → {target_host}:{target_port}")
        else:
            target_host, target_port = hostname, port
            stats["clearweb_routed"] += 1
            logger.info(f"[CLEARWEB] {hostname}:{port}")

        # Open connection to target
        try:
            remote_reader, remote_writer = await asyncio.open_connection(target_host, target_port)
        except Exception as e:
            stats["errors"] += 1
            logger.error(f"[ERROR] Cannot reach {target_host}:{target_port} → {e}")
            if method == "CONNECT":
                local_writer.write(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                await local_writer.drain()
            local_writer.close()
            return

        if method == "CONNECT":
            local_writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await local_writer.drain()
        else:
            remote_writer.write(request_line)
            await remote_writer.drain()

        await asyncio.gather(
            tunnel_traffic(local_reader, remote_writer),
            tunnel_traffic(remote_reader, local_writer),
            return_exceptions=True
        )

    except Exception as e:
        stats["errors"] += 1
        logger.debug(f"[ERROR] Handler: {e}")
    finally:
        try:
            local_writer.close()
        except Exception:
            pass

# ── STATUS API (for browser frontend at 8080) ──────────────────────────────────
async def handle_status_request(reader, writer):
    """
    Simple HTTP API consumed by edge-search.html
    GET /status  → node health JSON
    GET /stats   → full telemetry JSON
    OPTIONS *    → CORS preflight
    """
    try:
        request = await reader.read(1024)
        req_str = request.decode('utf-8', errors='ignore')
        first_line = req_str.split('\n')[0].strip()
        method = first_line.split(' ')[0] if first_line else 'GET'
        path   = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else '/status'

        cors_headers = (
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: GET, OPTIONS\r\n"
            "Access-Control-Allow-Headers: Content-Type\r\n"
        )

        if method == "OPTIONS":
            response = f"HTTP/1.1 204 No Content\r\n{cors_headers}\r\n"
            writer.write(response.encode())
            await writer.drain()
            writer.close()
            return

        uptime = int(time.time() - stats["started_at"])

        if path == "/stats":
            body = json.dumps({**stats, "uptime_seconds": uptime}, indent=2)
        else:
            # /status — minimal payload for banner
            body = json.dumps({
                "nodeId":  stats["node_id"],
                "peers":   stats["peers"],
                "uptime":  uptime,
                "mesh_routed":    stats["mesh_routed"],
                "clearweb_routed": stats["clearweb_routed"],
                "requests_total": stats["requests_total"],
                "status":  "online"
            })

        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"{cors_headers}\r\n"
            f"{body}"
        )
        writer.write(response.encode())
        await writer.drain()
    except Exception as e:
        logger.debug(f"[STATUS API] {e}")
    finally:
        try:
            writer.close()
        except Exception:
            pass

# ── SEARCH HANDLER ─────────────────────────────────────────────────────────────
async def handle_search_request(reader, writer):
    """
    GET /search?q=... — routes search query through mesh, returns JSON results.
    The browser frontend posts here; results come back as structured JSON.
    """
    try:
        request = await reader.read(4096)
        req_str = request.decode('utf-8', errors='ignore')
        first_line = req_str.split('\n')[0].strip()
        path = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else ''

        parsed = urllib.parse.urlparse(path)
        params = urllib.parse.parse_qs(parsed.query)
        query  = params.get('q', [''])[0]

        cors_headers = "Access-Control-Allow-Origin: *\r\n"

        if not query:
            body = json.dumps({"error": "no query", "results": []})
        else:
            logger.info(f"[SEARCH] Query: {query}")
            stats["requests_total"] += 1

            # TODO: replace with real mesh-distributed search index
            # For now returns a structured mock so the UI works end-to-end
            body = json.dumps({
                "query":   query,
                "source":  "ETK Mesh Network",
                "node":    stats["node_id"],
                "results": [
                    {
                        "title":   f"Mesh result for: {query}",
                        "url":     f"http://search.mesh/?q={urllib.parse.quote(query)}",
                        "snippet": "Result routed through PhoneServe sovereign mesh network.",
                        "source":  "mesh"
                    }
                ],
                "fallback_url": f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            })

        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"{cors_headers}\r\n"
            f"{body}"
        )
        writer.write(response.encode())
        await writer.drain()
    except Exception as e:
        logger.debug(f"[SEARCH] {e}")
    finally:
        try:
            writer.close()
        except Exception:
            pass

async def status_router(reader, writer):
    """Routes /status, /stats, /search on port 8080."""
    try:
        data = await reader.read(1024)
        req  = data.decode('utf-8', errors='ignore')
        path = req.split('\n')[0].split(' ')
        p    = path[1] if len(path) > 1 else '/status'
        # Replay buffered data by wrapping in a fake reader
        combined = data
        class BufReader:
            async def read(self, n):
                nonlocal combined
                chunk, combined = combined, b''
                return chunk
        br = BufReader()
        if p.startswith('/search'):
            await handle_search_request(br, writer)
        else:
            await handle_status_request(br, writer)
    except Exception as e:
        logger.debug(f"[ROUTER] {e}")
        try: writer.close()
        except: pass

# ── BOOT ───────────────────────────────────────────────────────────────────────
async def main():
    proxy_server  = await asyncio.start_server(handle_browser_client, LOCAL_HOST, LOCAL_PORT)
    status_server = await asyncio.start_server(status_router,         LOCAL_HOST, STATUS_PORT)

    logger.info(f"═══════════════════════════════════════════════")
    logger.info(f"  Edge Tech Knowledgey // PhoneServe Gateway")
    logger.info(f"  Proxy  : {LOCAL_HOST}:{LOCAL_PORT}")
    logger.info(f"  Status : {LOCAL_HOST}:{STATUS_PORT}")
    logger.info(f"  Node ID: {stats['node_id']}")
    logger.info(f"  Mesh nodes registered: {len(MESH_NODE_REGISTRY)}")
    logger.info(f"═══════════════════════════════════════════════")
    logger.info(f"  Point your browser proxy to 127.0.0.1:{LOCAL_PORT}")

    async with proxy_server, status_server:
        await asyncio.gather(
            proxy_server.serve_forever(),
            status_server.serve_forever()
        )

if __name__ == "__main__":
    asyncio.run(main())
