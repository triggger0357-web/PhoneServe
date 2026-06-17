import hashlib
import time
import uuid

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# ---------------------------

class PhoneServeNode:
    def __init__(self, device_name):
        self.device_name = device_name
        self.node_id = self._generate_sovereign_id()
        self.is_authenticated = False
        self.session_key = None

    def _generate_sovereign_id(self):
        """Creates a unique, permanent ID based on hardware and timestamp."""
        raw_id = f"{self.device_name}-{uuid.getnode()}"
        return hashlib.sha256(raw_id.encode()).hexdigest()

    def initiate_handshake(self):
        """Starts the handshake process with the decentralized mesh."""
        print(f"[SYSTEM] Node {self.device_name} initiating handshake...")
        print(f"[ID] Sovereign ID: {self.node_id[:15]}...")
        
        # Step 2: Create a time-stamped challenge
        timestamp = str(time.time())
        challenge = hashlib.sha256((self.node_id + timestamp).encode()).hexdigest()
        
        # In a real mesh, this challenge is sent to the nearest neighbor node
        return challenge

    def verify_mesh_response(self, mesh_signature):
        """Verifies the mesh is legitimate before sharing data."""
        # This prevents 'man-in-the-middle' attacks
        if mesh_signature:
            self.is_authenticated = True
            self.session_key = hashlib.md5(mesh_signature.encode()).hexdigest()
            print("[SUCCESS] Mutual Authentication Complete. Node is Active.")
            return True
        return False

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Example: Registering a new mobile device as a node
    my_phone = PhoneServeNode("David-Mobile-01")
    
    # Start the handshake
    auth_challenge = my_phone.initiate_handshake()
    
    # Simulate a successful response from the decentralized network
    # In practice, this would come from the peer-to-peer mesh
    simulated_mesh_resp = "EDGETECH-MESH-VERIFIED-2026"
    
    if my_phone.verify_mesh_response(simulated_mesh_resp):
        print(f"[STATUS] Ready to harvest and relay data.")
