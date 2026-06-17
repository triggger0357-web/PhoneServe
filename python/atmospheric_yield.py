# Edge Tech Atmospheric Energy Harvester v1.0
# Purpose: Calculate power from Humidity (MEG) and Wind Vibration (TENG).

def calculate_atmospheric_power(humidity_percentage, wind_speed_ms):
    # 1. Moisture-Electric Generation (MEG)
    # Extracts power from the movement of water ions in the air
    moisture_yield = (humidity_percentage / 100) * 0.85 # Watts per module
    
    # 2. Triboelectric Wind Harvest (TENG)
    # Captures energy from wind-induced "wobble" or friction
    # Low-start speed: 0.9 m/s (as per 2026 standards)
    wind_yield = (wind_speed_ms * 1.2) * 0.50 # Watts per module
    
    total_watts = moisture_yield + wind_yield
    return round(total_watts, 2)

# Example: A foggy day in Vancouver (90% humidity, 5 m/s wind)
print(f"Atmospheric Node Output: {calculate_atmospheric_power(90, 5)} Watts")
