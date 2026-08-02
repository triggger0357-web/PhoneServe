from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

leads = []

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            page = '<html><body style="background:#000; color:#0f0; font-family:monospace; padding:20px;"><h1>ETK Command Center</h1><div style="border:1px solid #0f0; padding:10px;"><input id="em" placeholder="Email" style="width:100%; background:#222; color:#fff; border:none; padding:10px;"><br><br><select id="cl" style="width:100%; background:#222; color:#fff; padding:10px;"><option value="Business">Business Class</option><option value="Corporate">Corporate Class</option></select><br><br><button onclick="save()" style="width:100%; padding:10px; background:#0f0; border:none; cursor:pointer;">REGISTER</button></div><h2>Live Leads</h2><div id="list">'
            for l in leads:
                page += f"<p>[{l['class']}] {l['email']}</p>"
            page += '</div><script>async function save(){ const d={email:document.getElementById("em").value, class:document.getElementById("cl").value}; await fetch("/api/signup",{method:"POST", body:JSON.stringify(d)}); location.reload(); }</script></body></html>'
            self.wfile.write(page.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/signup':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode())
            leads.append(data)
            self.send_response(200)
            self.end_headers()

print("--- COMMAND CENTER ONLINE ---")
httpd = HTTPServer(('127.0.0.1', 8585), Handler)
httpd.serve_forever()
