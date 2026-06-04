const { execSync } = require('child_process');

function launchNode() {
    console.log("Launching PhoneServe Node...");
    try {
        execSync('docker run -d --name edgetech-node edgetech/node:latest');
        console.log("Node started successfully.");
    } catch (e) {
        console.log("Error: Is Docker installed?");
    }
}

launchNode();
