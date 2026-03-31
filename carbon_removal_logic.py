# Edge Tech Carbon Sequestration Module
# Purpose: Calculate carbon removal offset using thermal energy reclamation.

def calculate_carbon_offset(nodes_active, run_time_hours):
    # Estimated CO2 removed if nodes are linked to micro-DAC filters
    # Based on 2026 Direct Air Capture standards
    tons_per_node_hour = 0.00005 
    total_removed = nodes_active * run_time_hours * tons_per_node_hour
    
    return f"Total CO2 Scrubbed: {total_removed} Tons"

# Example: 100-node pilot running for 24 hours
print(calculate_carbon_offset(100, 24))
