​📱 PhoneServe: Node & Terminal Operations Guide
​1. Initial Node Authentication
​To link your mobile hardware to the Sovereign Edge, use the handshake protocol:
ps-node auth --id [YOUR_DEVICE_ID] --key [YOUR_ENCRYPTED_KEY]
​2. Code Deployment (Pushing to Edge)
​To upload your local files or logic updates directly to the distributed server:
ps-deploy push ./my-logic-folder --target=edge-mesh
​3. Network Analysis (Vulnerability Testing)
​Since we’re focused on cybersecurity, use the built-in diagnostic to check node integrity:
ps-check --health --vulnerability-scan
​4. Revenue & Resource Monitoring
​To track your 90/10 split and see how much traffic your node is serving:
ps-stats --revenue --uptime
​5. Emergency Shutdown / IP Vaulting
​To pull a node offline and encrypt local data stores:
ps-secure --lock-all