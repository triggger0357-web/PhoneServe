# Edge Tech Multimodal Energy Harvester v1.0
# Purpose: Calculate electricity generated from spray-on "Active Surfaces."

def calculate_total_power(surface_area_m2, sunlight_w, engine_temp_c, wind_speed_mph):
    # 1. Photocatalytic Solar (Sunlight to Electrons)
    solar_yield = surface_area_m2 * (sunlight_w * 0.05) 
    
    # 2. Thermoelectric (Engine Heat to Electrons)
    # Uses the Seebeck effect from the Graphene-Silver coating
    thermal_delta = engine_temp_c - 25 # Difference from ambient
    thermal_yield = surface_area_m2 * (thermal_delta * 0.12)
    
    # 3. Piezoelectric (Vibration/Wind to Electrons)
    # Harvests energy from the car moving through air
    kinetic_yield = (wind_speed_mph * 0.08) * surface_area_m2
    
    total_watts = solar_yield + thermal_yield + kinetic_yield
    return round(total_watts, 2)

# Example: A coated car hood (2m2) in the sun, engine at 90C, driving 60mph
print(f"Current Power Generation: {calculate_total_power(2, 800, 90, 60)} Watts")
