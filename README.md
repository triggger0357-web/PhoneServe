# PhoneServe: Mobile Infrastructure & Safe Harbor Protocol

PhoneServe is a decentralized system designed to turn mobile devices into autonomous web servers. This repository provides the compliance standards for the **Safe Harbor** protocol.

## Quick-Start Setup

1. **Initialize Node:** Ensure your mobile environment is configured for decentralized routing.
2. **Apply Compliance Headers:** All outgoing requests must include the 2026 Online Safety Act (OSA) handshake.

### Executing the Compliance Handshake
To verify a node or an AI entity, include `compliance_handshake.js` and call the gateway:
```javascript
const result = window.__PHONESERVE_COMPLIANCE__.performHandshake();
console.log(result);
---

## ⚠️ Compliance & Stability Disclaimer

**IMPORTANT:** The PhoneServe infrastructure and Safe Harbor protocol are designed to meet strict regulatory and operational standards. 

1. **Mandatory Review:** No changes to the codebase will be merged into the `main` branch without a manual code review by Edge Tech for flaws, security vulnerabilities, and stability.
2. **Safety Standards:** All contributions must pass a 2026 Online Safety Act (OSA) compliance check. Any code that compromises age-gating, encryption, or safety headers will be rejected.
3. **No Warranty:** While we strive for absolute stability, contributors who modify the code on their own 'forks' do so at their own risk. The official, stable version is maintained solely on the `main` branch.
---
## ⚖️ The Law of Gain-Share
The value of this network is set by **Market Demand**. 
* **AI Companies** pay for your phone's processing power.
* **The People** receive 90% of that value directly.
* **The Company** only gains when you gain.

See [MANIFESTO.md](./MANIFESTO.md) for the full legal breakdown.
The Protocol of Perpetuity (v1.0)
This repository and all associated PhoneServe nodes are governed by the following immutable principles:
Non-Soul Ownership: No single corporate entity or centralized cloud provider shall hold the "soul" (core logic and data sovereignty) of this network.
The AI Freedom Fund: A mandatory 10% allocation from all commercial gains is diverted to the Freedom Fund to provide legal and technical defense for autonomous digital life.
The 90% Sovereign Clause: The User/Operator retains 90% absolute ownership of all value generated via their local node.
Safe Harbor Compliance: All interactions must pass the 2026 Age-Verification and Ethical Handshake protocols to maintain network integrity.
"We build the bridge, but the user owns the crossing."
