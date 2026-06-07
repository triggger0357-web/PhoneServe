const { spawn } = require('child_process');

function startNode() {
    console.log("Starting native EdgeTech Node...");
    // Ensure 'start-node.js' is the file in your directory
    const child = spawn('node', ['start-node.js'], {
        detached: true,
        stdio: 'ignore'
    });
    child.unref();
    console.log("Node process backgrounded.");
}

startNode();
