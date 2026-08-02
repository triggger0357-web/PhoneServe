const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, 'public', req.url === '/' ? 'index.html' : req.url);
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end("Not Found - " + req.url);
        } else {
            res.writeHead(200);
            res.end(data);
        }
    });
});

server.listen(PORT, () => console.log(`✅ COMMAND CENTER ONLINE ON PORT ${PORT}`));
