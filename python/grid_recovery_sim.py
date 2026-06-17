# Edge Tech Power Line Recovery Module v1.0
# Purpose: Calculate energy reclamation from High-Voltage Dielectric Gels.

def calculate_grid_recovery(line_voltage_kv, cable_length_km, gel_conductivity):
    # Standard corona discharge loss (energy leaking into the air)
    base_loss_per_km = line_voltage_kv * 0.05 
    
    # Recovery factor provided by the Edge Tech conductive gel matrix
    # The gel captures the electric field energy and redirects it
    recovered_energy_kwh = (base_loss_per_km * cable_length_km) * (gel_conductivity * 0.25)
    
    return round(recovered_energy_kwh, 2)

# Example: 500kV line, 10km stretch, using High-Performance Gel
print(f"Energy Recovered from Grid Leakage: {calculate_grid_recovery(500, 10, 0.95)} kWh")
