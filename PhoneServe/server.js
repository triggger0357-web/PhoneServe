const express = require('express');
const http = require('http');

const app = express();
const server = http.createServer(app);

app.use(express.json());
app.use(express.static(__dirname));

let latestOffer = null;

// Handle WebRTC offer incoming from a caller
app.post('/offer', (req, res) => {
    latestOffer = req.body;
    console.log('WebRTC Offer received successfully!');
    res.json({ status: 'success' });
});

// Allow the other peer to fetch the offer
app.get('/offer', (req, res) => {
    res.json(latestOffer || {});
});

server.listen(9090, '0.0.0.0', () => {
    console.log('PhoneServe is live at http://0.0.0.0:9090');
});
