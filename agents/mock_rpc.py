import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class EVMMockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        req = json.loads(post_data.decode('utf-8'))
        
        method = req.get("method")
        req_id = req.get("id", 1)

        # Handle EVM RPC Calls
        if method == "eth_call":
            data = req.get("params", [{}])[0].get("data", "")
            
            # getCapabilities check: Return legal=True, yield=True, proxy=True, compute=True
            if data.startswith("0x82efc60a"):
                res_hex = "0x" + ("0"*63 + "1") * 4
            else:
                # getAgentState: tier=2, level=5, xp=5000, hash=0x0, allowance=0.005 ETH, spent=0, reset_time
                res_hex = "0x" + \
                    "0"*63 + "2" + \
                    "0"*63 + "5" + \
                    "0"*63 + "a" + \
                    "0"*64 + \
                    "0"*51 + "11c37937e08000" + \
                    "0"*64 + \
                    "0"*56 + "65535000"

            response = {"jsonrpc": "2.0", "id": req_id, "result": res_hex}
        elif method == "eth_gasPrice":
            response = {"jsonrpc": "2.0", "id": req_id, "result": "0x3b9aca00"}
        elif method == "eth_getTransactionCount":
            response = {"jsonrpc": "2.0", "id": req_id, "result": "0x01"}
        elif method == "eth_sendRawTransaction":
            response = {"jsonrpc": "2.0", "id": req_id, "result": "0x" + "a"*64}
        elif method == "eth_chainId":
            response = {"jsonrpc": "2.0", "id": req_id, "result": "0x539"}
        else:
            response = {"jsonrpc": "2.0", "id": req_id, "result": "0x0"}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        return  # Suppress HTTP access logging

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 8545), EVMMockHandler)
    print("[Mock EVM] Local RPC server listening on http://127.0.0.1:8545...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Mock EVM] Server stopped.")
