# Edge Tech Thermal Coating Simulation v1.2
# Purpose: Calculate heat dissipation efficiency of advanced spray-on coatings.

def calculate_thermal_reduction(ambient_temp, cpu_load, coating_conductivity):
    # Base heat generated without coating
    base_heat = ambient_temp + (cpu_load * 0.5)
    
    # Efficiency gain from the spray-on thermal spreader (W/m·K)
    # Target: Graphene or Boron Nitride infused coatings
    reduction_factor = coating_conductivity * 0.15
    final_temp = base_heat - reduction_factor
    
    return round(final_temp, 2)

# Test Scenario: 90% CPU Load with High-Efficiency Coating
print(f"Projected Device Temp with Coating: {calculate_thermal_reduction(25, 90, 5.0)}°C")
