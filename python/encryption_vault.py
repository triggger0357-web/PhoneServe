import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# CONTACT: 503-990-4004 (TEXT ONLY)
# ---------------------------

class EncryptionVault:
    def __init__(self, node_id):
        self.node_id = node_id
        # In a live Edge Tech environment, the key would be derived from 
        # your Sovereign ID and a private passphrase.
        self.secret_key = self._generate_vault_key(node_id)

    def _generate_vault_key(self, identifier):
        """Creates a 32-byte key for AES-256."""
        # This ensures the key is unique to your specific node
        key = identifier.encode()[:32].ljust(32, b'0')
        return key

    def lock_data(self, plaintext):
        """Encrypts data before it enters the PhoneServe mesh."""
        iv = os.urandom(16)  # Initialization Vector for randomness
        cipher = Cipher(algorithms.AES(self.secret_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        
        # Combine IV and Ciphertext for transport
        encrypted_package = base64.b64encode(iv + ciphertext).decode('utf-8')
        print(f"[VAULT] Data Locked. Encrypted Hash: {hash(encrypted_package)}")
        return encrypted_package

    def unlock_data(self, encrypted_package):
        """Decrypts data when it reaches the authorized destination."""
        try:
            raw_data = base64.b64decode(encrypted_package)
            iv = raw_data[:16]
            ciphertext = raw_data[16:]
            
            cipher = Cipher(algorithms.AES(self.secret_key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
            return decrypted_text.decode('utf-8')
        except Exception as e:
            print("[ALERT] Unauthorized access attempt or corrupt packet.")
            return None

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Setup the vault for your primary node
    my_vault = EncryptionVault("VAN-WA-SECURE-ID-001")
    
    # 1. Take sensitive harvesting data
    original_message = "CONFIDENTIAL: Harvested 2.4V at 45.65 N, 122.67 W"
    print(f"Original: {original_message}")
    
    # 2. Lock it down
    locked_message = my_vault.lock_data(original_message)
    print(f"Locked (for Relay): {locked_message}")
    
    # 3. Unlock it (only at the authorized destination)
    unlocked_message = my_vault.unlock_data(locked_message)
    print(f"Unlocked: {unlocked_message}")
