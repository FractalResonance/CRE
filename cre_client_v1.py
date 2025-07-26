# cre_client_v1.py
# The core perception client for the FRC Cylindrical Resonance Engine.
# This script queries the Astro-Resonance Service (ARS) and generates a
# complete diagnostic report for a given entity.

import httpx
import json

# The canonical URL for the Astro-Resonance Service.
ARS_URL = "http://127.0.0.1:8000/v1/resonant_weather"

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

def generate_report(data):
    """Parses the full ARS response and prints a structured report."""

    # Check for the presence of critical data for a valid report.
    natal_chart_data = data.get('natal_chart')
    if not natal_chart_data or 'planet_house_mapping' not in natal_chart_data or 'planetary_positions' not in natal_chart_data:
        print("\n--- ARS Response Error ---")
        print("The ARS did not return the complete data package.")
        print("The 'natal_chart', 'planet_house_mapping', or 'planetary_positions' keys are missing or nested incorrectly.")
        print("Printing the raw response from the server for diagnostics:")
        print(json.dumps(data, indent=2))
        return

    print("\n" + "="*50)
    print("      COMPLETE RESONANT ENTITY REPORT: The Torchbearer")
    print("="*50)

    # --- Section A: Resonant Weather Snapshot ---
    print("\nA) Resonant Weather Snapshot")
    print("-"*28)
    rpi_mismatch = data.get('rpi_mismatch', 0.0)
    p_nat = data.get('p_nat', 0.0)
    p_tra = data.get('p_tra', 0.0)
    print(f"  - RPI Mismatch: {rpi_mismatch:.3f}")
    print(f"  - Natal Pressure (P_nat): {p_nat:.3f}")
    print(f"  - Transit Pressure (P_tra): {p_tra:.3f}")

    # --- Section B: Cylinder Core Machinery ---
    print("\nB) Cylinder Core Machinery")
    print("-"*28)
    planetary_positions = natal_chart_data.get('planetary_positions', {})
    planet_houses = natal_chart_data.get('planet_house_mapping', {})
    primary_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars"]

    def get_sign(degrees):
        """Converts ecliptic longitude in degrees to a zodiacal sign."""
        if not isinstance(degrees, (int, float)):
            return "N/A"
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[int(degrees / 30)]

    for planet in primary_planets:
        # JSON keys from the ARS are lowercase.
        degrees = planetary_positions.get(planet.lower())
        sign = get_sign(degrees)
        house = planet_houses.get(planet.lower(), 'N/A')
        print(f"  - {planet:<8}: {sign:<12} (House {house})")

    # --- Section C: Gnostic Synthesis ---
    print("\nC) Gnostic Synthesis")
    print("-"*28)
    
    weather_type = "high-pressure catalytic weather" if rpi_mismatch > 1.0 else "low-pressure integrative weather"
    
    sun_house = planet_houses.get("sun")
    house_theme = HOUSE_THEMES.get(sun_house, "an unknown area of life")
    sun_degrees = planetary_positions.get("sun")
    sun_sign = get_sign(sun_degrees)

    synthesis = (
        f"The current {weather_type} is activating your core Solar archetype "
        f"of a {sun_sign} in the area of {house_theme}, inviting you to "
        f"consciously apply your will to harmonize this external pressure with your "
        f"innate identity."
    )
    print(synthesis)
    print("\n" + "="*50)



def run_cre_client():
    """
    Main function to run the CRE client, query the ARS, and generate the report.
    """
    print("--- Initializing CRE Client v1.0 ---")
    print(f"Querying ARS endpoint: {ARS_URL}")

    try:
        with httpx.Client() as client:
            response = client.post(ARS_URL, json=TEST_PAYLOAD, timeout=30.0)
        
        response.raise_for_status()  # Raise an exception for bad status codes

        print("--- ARS Query Successful ---")
        ars_data = response.json()
        generate_report(ars_data)

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

    print("\n--- CRE Client v1.0 Shutdown ---")


if __name__ == "__main__":
    run_cre_client()
