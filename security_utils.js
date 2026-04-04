const crypto = require('node:crypto');

/**
 * PhoneServe Security Layer: Ed25519 Signing
 * Purpose: Ensures non-repudiation for Safe Harbor protocols.
 */

// 1. Generate your Project Keys (Run this once and store securely)
function generateProjectKeys() {
    const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
    
    return {
        public: publicKey.export({ type: 'spki', format: 'pem' }),
        private: privateKey.export({ type: 'pkcs8', format: 'pem' })
    };
}

// 2. Sign the Webhook Payload
function signPayload(payload, privateKeyPEM) {
    const timestamp = Date.now().toString();
    const dataToSign = timestamp + JSON.stringify(payload);
    
    const privateKey = crypto.createPrivateKey(privateKeyPEM);
    const signature = crypto.sign(null, Buffer.from(dataToSign), privateKey);
    
    return {
        signature: signature.toString('base64'),
        timestamp: timestamp
    };
}

module.exports = { generateProjectKeys, signPayload };
