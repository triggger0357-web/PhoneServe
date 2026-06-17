# AUTHORITY: THE COURT | CO-FOUNDERS: JOHN D. COURT & DAVID BRIAN INGALLS
import json
import time
import hashlib

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# ---------------------------

class DataPacket:
    def __init__(self, sender_id, destination_id, payload):
        self.sender_id = sender_id
        self.destination_id = destination_id
        self.payload = payload
        self.timestamp = time.time()
        self.packet_hash = self._sign_packet()

    def _sign_packet(self):
        """Creates a unique fingerprint for this data packet."""
        raw_string = f"{self.sender_id}{self.destination_id}{self.payload}{self.timestamp}"
        return hashlib.sha256(raw_string.encode()).hexdigest()

class RelayNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.relay_log = []

    def process_incoming_packet(self, packet):
        """Decides whether to keep the data or pass it along."""
        if packet.destination_id == self.node_id:
            print(f"[SUCCESS] Packet received at destination: {self.node_id}")
            self._decrypt_payload(packet.payload)
        else:
            print(f"[RELAY] Routing packet from {packet.sender_id[:8]} to neighbor...")
            self._forward_packet(packet)

    def _forward_packet(self, packet):
        """Simulates passing the data to the next available PhoneServe node."""
        log_entry = {
            "packet_id": packet.packet_hash[:12],
            "action": "FORWARDED",
            "time": time.ctime(packet.timestamp)
        }
        self.relay_log.append(log_entry)
        # In a live mesh, this would trigger a Bluetooth/Wi-Fi Direct broadcast
        print(f"[LOG] Packet {log_entry['packet_id']} moved through Edge Tech Mesh.")

    def _decrypt_payload(self, payload):
        # Placeholder for the decryption logic we established earlier
        print(f"[DATA] Content: {payload}")

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Setup two nodes
    node_vancouver = RelayNode("VAN-WA-NODE-001")
    
    # Create a packet meant for a different node
    secret_data = "Atmospheric Harvest: 1.2v detected."
    new_packet = DataPacket("SENDER-ID-XYZ", "DESTINATION-NODE-ABC", secret_data)
    
    # Simulate the node acting as a relay
    node_vancouver.process_incoming_packet(new_packet)
    
    print(f"\n[RECORDS] Relay History for Node {node_vancouver.node_id}:")
    print(json.dumps(node_vancouver.relay_log, indent=2))
