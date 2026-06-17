import random
import time
import json

# --- PROPRIETARY HEADER ---
# PROPERTY OF DAVID INGALLS | EDGE TECH
# NO COMMERCIAL USE WITHOUT WRITTEN CONSENT
# ---------------------------

class EnergyHarvestDiagnostic:
    def __init__(self, node_id):
        self.node_id = node_id
        self.harvest_history = []
        self.threshold_v = 0.5  # Minimum voltage to trigger storage

    def read_atmospheric_potential(self):
        """Simulates reading voltage from the aerosol conductive mesh."""
        # In a live setup, this would interface with a GPIO pin or ADC
        # Harvesting from the 'Global Circuit' (Ionosphere to Ground)
        ambient_v = round(random.uniform(0.1, 2.5), 3) 
        rf_induction_v = round(random.uniform(0.05, 0.8), 3)
        
        total_input = ambient_v + rf_induction_v
        return {
            "source": "Atmospheric/RF",
            "voltage": total_input,
            "status": "CHARGING" if total_input > self.threshold_v else "IDLE"
        }

    def log_harvest_cycle(self):
        """Records a snapshot of the energy being pulled from the air."""
        data = self.read_atmospheric_potential()
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "node_id": self.node_id,
            "metrics": data
        }
        
        self.harvest_history.append(entry)
        
        if data["status"] == "CHARGING":
            print(f"[ENERGY] +{data['voltage']}V harvested via Edge Tech Mesh.")
        else:
            print("[SYSTEM] Low ambient energy. Monitoring atmospheric gradient...")
            
        return entry

    def get_efficiency_report(self):
        """Calculates total energy harvested over the current session."""
        total_v = sum(item["metrics"]["voltage"] for item in self.harvest_history)
        avg_v = total_v / len(self.harvest_history) if self.harvest_history else 0
        
        return {
            "total_harvested_v": round(total_v, 2),
            "average_efficiency": round(avg_v, 2),
            "cycle_count": len(self.harvest_history)
        }

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Initialize diagnostic for the Vancouver node
    diagnostic = EnergyHarvestDiagnostic("VAN-WA-NODE-001")
    
    print("--- STARTING ENERGY DIAGNOSTIC SCAN ---")
    # Simulate 5 harvest cycles (e.g., every few seconds)
    for _ in range(5):
        diagnostic.log_harvest_cycle()
        time.sleep(1)
        
    # Generate the final report for Edge Tech records
    report = diagnostic.get_efficiency_report()
    print("\n[REPORT] Edge Tech Energy Harvesting Summary:")
    print(json.dumps(report, indent=4))
