import asyncio, logging, urllib.parse, json, time, hashlib, re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ETK-MeshGateway")

LOCAL_HOST, LOCAL_PORT, STATUS_PORT = "127.0.0.1", 1080, 8080
BUFFER_SIZE = 8192

TOKEN_RE = re.compile(r'^COMP-2026-[A-F0-9]{8}-\d+$')
VERSION = "2026-18plus-v1"
STANDARD = "2026 Online Safety Act — Under-18 AI Content Compliance"

def valid_compliance_header(h):
    if not h: return False
    m = re.search(r'token:(COMP-2026-[A-F0-9]{8}-\d+)', h)
    if not m: return False
    return bool(TOKEN_RE.match(m.group(1)))

MESH_NODE_REGISTRY = {
    "phoneserve.node": ("127.0.0.1", 9001),
    "void-odyssey.node": ("127.0.0.1", 9002),
}

stats = {
    "requests_total": 0, "mesh_routed": 0, "clearweb_routed": 0, "errors": 0,
    "started_at": time.time(),
    "node_id": "ETK-" + hashlib.sha256(b"phoneserve-local").hexdigest()[:8].upper(),
    "peers": len(MESH_NODE_REGISTRY),
}

async def handle_status(req_data):
    uptime = int(time.time() - stats["started_at"])
    body = json.dumps({
        "nodeId": stats["node_id"], "peers": stats["peers"], "uptime": uptime,
        "mesh_routed": stats["mesh_routed"], "clearweb_routed": stats["clearweb_routed"],
        "requests_total": stats["requests_total"], "status": "online",
        "compliance": VERSION, "standard": STANDARD
    })
    return body

async def status_router(reader, writer):
    try:
        data = await reader.read(4096)
        req = data.decode('utf-8', errors='ignore')
        first = req.split('\n')[0]
        path = first.split(' ')[1] if len(first.split(' '))>1 else '/status'
        cors = "Access-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type, X-Compliance-Token\r\n"

        if "OPTIONS" in first:
            writer.write(f"HTTP/1.1 204 No Content\r\n{cors}\r\n".encode())
            await writer.drain(); writer.close(); return

        # /search handling
        if "/search" in path:
            parsed = urllib.parse.urlparse(path)
            q = urllib.parse.parse_qs(parsed.query).get('q',[''])[0]
            # Check compliance token in request
            if not valid_compliance_header(req):
                body = json.dumps({"error": "2026-18plus-v1 token required", "source": "compliance-gate"})
            else:
                body = json.dumps({
                    "query": q, "source": "ETK Mesh Network (hardened)",
                    "results": [{"title": f"Mesh result for: {q}", "url": f"http://search.mesh/?q={q}", "snippet": "Routed via sovereign mesh", "source": "mesh"}],
                    "fallback_url": f"https://www.google.com/search?q={urllib.parse.quote(q)}"
                })
        else:
            body = await handle_status(req)

        resp = f"HTTP/1.1 200 OK\r\n{cors}Content-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        writer.write(resp.encode())
        await writer.drain()
    except Exception as e:
        logger.error(e)
    finally:
        try: writer.close()
        except: pass

async def proxy_handler(local_reader, local_writer):
    try:
        line = await local_reader.readline()
        if not line:
            local_writer.close(); return
        # read rest of headers for token check
        headers = b""
        while True:
            l = await local_reader.readline()
            headers += l
            if l == b"\r\n" or not l: break

        if not valid_compliance_header(headers.decode('utf-8', errors='ignore')):
            local_writer.write(b"HTTP/1.1 403 Forbidden\r\n\r\nSafe Harbor: token required")
            await local_writer.drain()
            local_writer.close()
            return

        # For demo, just close - real proxy logic in original file
        local_writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await local_writer.drain()
    except:
        pass
    finally:
        try: local_writer.close()
        except: pass

async def main():
    s1 = await asyncio.start_server(proxy_handler, LOCAL_HOST, LOCAL_PORT)
    s2 = await asyncio.start_server(status_router, LOCAL_HOST, STATUS_PORT)
    print(f"✅ MESH PROXY ONLINE {LOCAL_HOST}:{LOCAL_PORT}")
    print(f"✅ STATUS API ONLINE {LOCAL_HOST}:{STATUS_PORT} — Enforcing {VERSION}")
    async with s1, s2:
        await asyncio.gather(s1.serve_forever(), s2.serve_forever())

if __name__ == "__main__":
    asyncio.run(main())
