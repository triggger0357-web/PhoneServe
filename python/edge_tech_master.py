import time
import json
from node_handshake import PhoneServeNode
from data_relay import RelayNode, DataPacket
from energy_diagnostic import EnergyHarvestDiagnostic

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# CONTACT: 503-990-4004 (TEXT ONLY)
# ---------------------------

class PhoneServeMaster:
    def __init__(self, device_name):
        print(f"--- INITIALIZING EDGE TECH NODE: {device_name} ---")
        # Initialize the three core modules
        self.auth = PhoneServeNode(device_name)
        self.relay = RelayNode(self.auth.node_id)
        self.energy = EnergyHarvestDiagnostic(self.auth.node_id)
        
        self.is_active = False

    def startup_sequence(self):
        """Step 1: Perform Handshake and verify Energy levels."""
        # 1. Handshake
        self.auth.initiate_handshake()
        # Simulate mesh verification
        if self.auth.verify_mesh_response("EDGETECH-SECURE-2026"):
            # 2. Check Energy Diagnostic
            status = self.energy.log_harvest_cycle()
            
            if status['metrics']['voltage'] > 0.4:
                print("[MASTER] Sufficient atmospheric energy detected.")
                self.is_active = True
                print("--- NODE FULLY OPERATIONAL ---\n")
            else:
                print("[CRITICAL] Low energy. Entering passive harvest mode.")
        
    def handle_mesh_traffic(self, incoming_packet):
        """Step 2 & 3: Process and Relay Data using Harvested Power."""
        if not self.is_active:
            print("[DENIED] Node inactive. Complete startup sequence first.")
            return

        print(f"[MASTER] Processing traffic for Packet: {incoming_packet.packet_hash[:8]}")
        # Log the energy cost of this relay
        self.energy.log_harvest_cycle()
        # Process the relay
        self.relay.process_incoming_packet(incoming_packet)

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Initialize the Master Controller
    node_master = PhoneServeMaster("VAN-WA-PRIMARY-01")
    
    # Run the startup (Handshake + Energy Check)
    node_master.startup_sequence()
    
    # Simulate an incoming Data Packet to relay
    test_packet = DataPacket("REMOTE-SENDER", "TARGET-NODE-99", "Encrypted Data Stream")
    
    # Execute the Relay
    node_master.handle_mesh_traffic(test_packet)
    
    # Final Energy Efficiency Check
    print("\n--- FINAL NODE STATUS ---")
    print(json.dumps(node_master.energy.get_efficiency_report(), indent=4))
