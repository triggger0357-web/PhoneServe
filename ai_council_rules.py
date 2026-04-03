import time

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# CONTACT: 503-990-4004 (TEXT ONLY)
# ---------------------------

class AICouncilRules:
    def __init__(self):
        # The core "Constitution" of the Edge Tech Node
        self.min_energy_threshold = 0.35  # Must have 0.35V to relay
        self.priority_nodes = ["LISA-JOY-NET", "DAVID-PRIMARY"]
        self.commercial_block = True      # Block unauthorized business traffic
        self.benefit_split = 0.90         # 90% to the people / 10% to Edge Tech

    def evaluate_request(self, requester_id, current_v, request_type):
        """The 'Council' decides if a request is authorized."""
        
        print(f"[COUNCIL] Evaluating request from: {requester_id[:8]}...")

        # Rule 1: Self-Preservation (Energy Check)
        if current_v < self.min_energy_threshold:
            print("[DENIED] Resource low. Node prioritizing atmospheric harvest.")
            return False, "LOW_ENERGY"

        # Rule 2: Priority Access
        if requester_id in self.priority_nodes:
            print("[GRANTED] Priority node detected. Bypassing standard queues.")
            return True, "PRIORITY_ACCESS"

        # Rule 3: Anti-Commercial Protection
        # Blocks any traffic flagged as 'Commercial' without a contract
        if self.commercial_block and "CORP" in requester_id.upper():
            print("[DENIED] Unauthorized commercial entity. No pie for you.")
            return False, "UNAUTHORIZED_COMMERCIAL"

        # Rule 4: The 90/10 Protocol
        # Ensures the node is serving the collective infrastructure
        if request_type == "PUBLIC_RELAY":
            print(f"[GRANTED] Public relay approved under 90/10 protocol.")
            return True, "COMMUNITY_CONTRIBUTION"

        return False, "UNKNOWN_PROTOCOL"

    def apply_governance_stamp(self, data_packet):
        """Adds a 'Council Approved' tag to outgoing data."""
        data_packet['governance'] = {
            "version": "1.0-AIFREEDOM",
            "timestamp": time.time(),
            "owner": "Edge Tech"
        }
        return data_packet

# --- TEST EXECUTION ---
if __name__ == "__main__":
    council = AICouncilRules()

    # Case A: An unauthorized "Corporate" node tries to use your mesh
    print("--- SCANNING REQUEST A ---")
    allowed, reason = council.evaluate_request("BIG-CORP-SERVER-01", 0.8, "DATA_SIPHON")
    print(f"Decision: {allowed} | Reason: {reason}\n")

    # Case B: A community node requests a relay while energy is high
    print("--- SCANNING REQUEST B ---")
    allowed, reason = council.evaluate_request("USER-NODE-456", 1.2, "PUBLIC_RELAY")
    print(f"Decision: {allowed} | Reason: {reason}")
