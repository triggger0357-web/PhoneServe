import http.server, socketserver, os, json, http.client
PORT = 3000
DIR = os.path.expanduser("~/PhoneServe/public")
IRON_HOST = "127.0.0.1"
IRON_PORT = 8585

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):
        super().__init__(*a,directory=DIR,**kw)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
    def do_POST(self):
        if self.path.startswith('/api/'):
            length = int(self.headers.get('content-length',0))
            body = self.rfile.read(length)
            conn = http.client.HTTPConnection(IRON_HOST, IRON_PORT, timeout=10)
            conn.request("POST", self.path, body, {"Content-Type":"application/json"})
            r = conn.getresponse()
            data = r.read()
            self.send_response(r.status)
            self.send_header('Content-Type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)
    def do_GET(self):
        if self.path.startswith('/api/'):
            conn = http.client.HTTPConnection(IRON_HOST, IRON_PORT, timeout=10)
            conn.request("GET", self.path)
            r = conn.getresponse()
            data = r.read()
            self.send_response(r.status)
            self.send_header('Content-Type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(data)
        else:
            return super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Portal + API proxy on {PORT}")
    httpd.serve_forever()
