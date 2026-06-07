const pm2 = require('pm2');

function showDashboard() {
    pm2.connect((err) => {
        if (err) { console.error(err); process.exit(2); }

        pm2.list((err, list) => {
            console.log("\n--- EdgeTech Admin AI Panel ---");
            list.forEach(proc => {
                console.log(`Node: ${proc.name} | Status: ${proc.pm2_env.status} | CPU: ${proc.monit.cpu}% | Mem: ${(proc.monit.memory/1024/1024).toFixed(2)}MB`);
            });
            console.log("-------------------------------\nOptions: [1] Restart Node [2] Run Backup [3] Exit");
            pm2.disconnect();
        });
    });
}

showDashboard();
