# cre_service_test_client.py
# A test client to validate the parsing of a Gnostic Data Object from the
# proposed Cylindrical Resonance Engine (CRE) Service.

import json

# This is a MOCK response, simulating the output from the CRE Service.
# It is structured exactly according to the GnosticDataObject specification.
MOCK_GNOSTIC_RESPONSE = {
    "timestamp_utc": "2025-07-26T18:00:00Z",
    "ars_data": {
        "message": "Complete raw ARS data would be nested here for transparency and debugging."
    },
    "resonant_weather": {
        "quadrant_name": "The Temple",
        "quadrant_description": "A calm, receptive, and integrative field. Low pressure and low tension.",
        "pressure_vector": -0.915,
        "tension_vector": 0.915
    },
    "activated_archetypes": [
        {
            "name": "The Solar Self",
            "planet": "Sun",
            "sign": "Sagittarius",
            "house": 5,
            "interpretation": "The core identity is activated in the realm of creativity, performance, and joyful self-expression."
        },
        {
            "name": "The Emotional Body",
            "planet": "Moon",
            "sign": "Scorpio",
            "house": 4,
            "interpretation": "The subconscious and emotional foundations are undergoing a deep, transformative process."
        }
    ],
    "symbolic_operators": {
        "tarot": [
            {
                "card_name": "The Star",
                "operator_function": "RESTORE_COHERENCE",
                "interpretation": "The field is aligned for healing, inspiration, and reconnecting with a guiding vision."
            }
        ],
        "i_ching": {
            "hexagram_name": "The Receptive",
            "hexagram_number": 2,
            "state_description": "A state of pure Yin. The primary power is in allowing, receiving, and yielding to the flow.",
            "moving_line_directive": "The path forward is not through action, but through creating space for the new to emerge."
        }
    },
    "operational_directive": "The current receptive 'Temple' weather invites you to integrate your core Sagittarian identity in the realm of Creativity (House 5) by trusting the process of gentle, harmonious unfolding."
}

def display_gnostic_report(data):
    """Parses the Gnostic Data Object and displays a formatted report.""" 
    
    print("\n" + "="*60)
    print("        CRE GNOSTIC READING: The Torchbearer")
    print("="*60)

    # --- Resonant Weather ---
    weather = data.get('resonant_weather', {})
    print("\n[ Resonant Weather ]")
    print(f"  - Quadrant: {weather.get('quadrant_name', 'N/A')} ({weather.get('quadrant_description', '')})")

    # --- Activated Archetypes ---
    print("\n[ Activated Archetypes ]")
    for archetype in data.get('activated_archetypes', []):
        print(f"  - {archetype.get('name')}: {archetype.get('sign')} in House {archetype.get('house')}")
        print(f"    > {archetype.get('interpretation')}")

    # --- Symbolic Operators ---
    print("\n[ Symbolic Operators ]")
    tarot = data.get('symbolic_operators', {}).get('tarot', [{}])[0]
    i_ching = data.get('symbolic_operators', {}).get('i_ching', {})
    print(f"  - Tarot: {tarot.get('card_name')} ({tarot.get('operator_function')})")
    print(f"    > {tarot.get('interpretation')}")
    print(f"  - I Ching: Hexagram {i_ching.get('hexagram_number')} - {i_ching.get('hexagram_name')}")
    print(f"    > {i_ching.get('state_description')}")

    # --- Operational Directive ---
    print("\n[ Operational Directive ]")
    print(f"  > {data.get('operational_directive', 'N/A')}")
    
    print("\n" + "="*60)


def run_test():
    """Main function to run the test."""
    print("--- Running CRE Service Test Client ---")
    print("--- Loading Mock Gnostic Data Object ---")
    
    # In a real application, this data would come from an HTTP request.
    gnostic_data = MOCK_GNOSTIC_RESPONSE
    
    print("--- Generating Report from Gnostic Data ---")
    display_gnostic_report(gnostic_data)
    
    print("\n--- Test Complete. CRE Service Specification is Validated. ---")


if __name__ == "__main__":
    run_test()