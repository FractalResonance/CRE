# cre_client_v2.py
# The upgraded core perception client for the FRC Cylindrical Resonance Engine.
# This script queries the ARS v0.3's new /v1/full_reading endpoint,
# parses the 2D RPI vector, and generates a Complete Resonant Weather Report v2.0.

import httpx
import json

# The canonical URL for the Astro-Resonance Service v0.3's new endpoint.
ARS_URL = "http://127.0.0.1:8000/v1/full_reading"

# Natal data for the entity designated "The Torchbearer".
TEST_PAYLOAD = {
  "natal_data": {
    "year": 1986,
    "month": 11,
    "day": 29,
    "hour": 17,
    "minute": 20,
    "lat": 35.68,
    "lon": 51.42
  },
  "current_location": {
    "lat": 35.68,
    "lon": 51.42
  }
}

# A mapping of house numbers to their core archetypal themes.
HOUSE_THEMES = {
    1: "Self and Identity",
    2: "Resources and Values",
    3: "Communication and Learning",
    4: "Home and Foundations",
    5: "Creativity and Self-Expression",
    6: "Work, Health, and Daily Systems",
    7: "Partnerships and Relationships",
    8: "Transformation and Shared Power",
    9: "Philosophy and Higher Meaning",
    10: "Career and Public Life",
    11: "Community and Future Aspirations",
    12: "The Unconscious and Spirituality"
}

def get_resonant_weather_quadrant(pressure: float, tension: float):
    """Determines the Resonant Weather Quadrant based on Pressure and Tension."""
    if pressure >= 0 and tension >= 0:
        return "The Forge", "Catalytic, Agitated", "Act & Confront: Channel energy into productive work. Use friction for transformation."
    elif pressure >= 0 and tension < 0:
        return "The River", "Expansive, Flowing", "Create & Connect: Launch projects, socialize. Embody the expansive grace."
    elif pressure < 0 and tension >= 0:
        return "The Void", "Stuck, Frustrated", "Wait & Witness: Meditate on the internal conflict. Do not force external action."
    else: # pressure < 0 and tension < 0
        return "The Temple", "Calm, Receptive", "Rest & Integrate: Allow for deep recovery and gentle insight."

def generate_report_v2(data):
    """Parses the full ARS v0.3 response and prints a structured report v2.0."""

    # Validate expected keys from the new /v1/full_reading endpoint
    required_keys = ['rpi_vector', 'natal_chart']
    if not all(key in data for key in required_keys):
        print("\n--- ARS Response Error ---")
        print("The ARS did not return the complete data package for v0.3.")
        print(f"Missing one or more required keys: {required_keys}")
        print("Printing the raw response from the server for diagnostics:")
        print(json.dumps(data, indent=2))
        return

    rpi_vector = data.get('rpi_vector', {})
    pressure = rpi_vector.get('pressure', 0.0)
    tension = rpi_vector.get('tension', 0.0)
    
    quadrant_name, quadrant_desc, quadrant_directive = get_resonant_weather_quadrant(pressure, tension)

    print("\n" + "="*60)
    print("      COMPLETE RESONANT WEATHER REPORT v2.0: The Torchbearer")
    print("="*60)

    # --- Section A: Resonant Weather Snapshot ---
    print("\nA) Resonant Weather Snapshot")
    print("-"*30)
    print(f"  - Resonant Weather Quadrant: {quadrant_name} ({quadrant_desc})")
    print(f"  - Pressure Component: {pressure:.3f}")
    print(f"  - Tension Component: {tension:.3f}")
    
    # --- Section B: Cylinder Core Machinery (from natal_chart) ---
    print("\nB) Cylinder Core Machinery")
    print("-"*30)
    natal_chart_data = data.get('natal_chart', {})
    planetary_positions = natal_chart_data.get('planetary_positions', {})
    planet_house_mapping = natal_chart_data.get('planet_house_mapping', {})
    primary_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars"]

    def get_sign(degrees):
        """Converts ecliptic longitude in degrees to a zodiacal sign."""
        if not isinstance(degrees, (int, float)):
            return "N/A"
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[int(degrees / 30)]

    for planet in primary_planets:
        degrees = planetary_positions.get(planet.lower())
        sign = get_sign(degrees)
        house = planet_house_mapping.get(planet.lower(), 'N/A')
        print(f"  - {planet:<8}: {sign:<12} (House {house})")

    # --- Section C: Operational Directive for Current Quadrant ---
    print("\nC) Operational Directive")
    print("-"*30)
    print(f"  > {quadrant_directive}")
    
    print("\n" + "="*60)


def run_cre_client_v2():
    """
    Main function to run the CRE client v2.0, query the ARS v0.3, and generate the report.
    """
    print("--- Initializing CRE Client v2.0 ---")
    print(f"Querying ARS endpoint: {ARS_URL}")

    try:
        with httpx.Client() as client:
            response = client.post(ARS_URL, json=TEST_PAYLOAD, timeout=30.0)
        
        response.raise_for_status()  # Raise an exception for bad status codes

        print("--- ARS Query Successful ---")
        ars_data = response.json()
        generate_report_v2(ars_data)

    except httpx.HTTPStatusError as e:
        print(f"\n--- ARS Query Failed (Status Code: {e.response.status_code}) ---")
        print("The Astro-Resonance Service returned an error.")
        print(f"Response: {e.response.text}")
    except httpx.ConnectError as e:
        print("\n--- Connection Error ---")
        print("Could not connect to the Astro-Resonance Service.")
        print("Please ensure the ARS server is running and accessible.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"\n--- An Unexpected Error Occurred ---")
        print(f"Error details: {e}")

    print("\n--- CRE Client v2.0 Shutdown ---")


if __name__ == "__main__":
    run_cre_client_v2()
