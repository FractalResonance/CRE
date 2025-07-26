# ars_client_test.py
# A simple client to test the FRC Alchemical Resonance System (ARS) API.

import httpx
import json

# 1. Define the target URL for the ARS API.
ARS_URL = "http://127.0.0.1:8000/v1/resonant_weather"

# 2. Define the test payload for "The Alchemist" (Hadi) in Tehran.
test_payload = {
  "natal_data": {
    "year": 1985,
    "month": 12,
    "day": 8,
    "hour": 13,
    "minute": 15,
    "lat": 35.68,
    "lon": 51.42
  },
  "current_location": {
    "lat": 35.68,
    "lon": 51.42
  }
}

def run_test():
    """
    Sends a request to the ARS API and prints a report of the response.
    """
    print("--- Starting ARS Client Test ---")
    print(f"Targeting API endpoint: {ARS_URL}")

    try:
        # 3. Make the API call using an httpx client.
        with httpx.Client() as client:
            print("Sending POST request with the following payload:")
            print(json.dumps(test_payload, indent=2))
            
            response = client.post(ARS_URL, json=test_payload, timeout=30.0)

        # 4. Process the response.
        if response.status_code == 200:
            print("\n--- Test Successful (Status Code: 200) ---")
            data = response.json()
            
            # 5. Generate a coherent report.
            p_nat = data.get("p_nat")
            p_tra = data.get("p_tra")
            rpi_mismatch = data.get("rpi_mismatch")

            if all(v is not None for v in [p_nat, p_tra, rpi_mismatch]):
                print("\nResonant Weather Report:")
                print(f"  - Natal Pressure (P_nat):      {p_nat:.3f}")
                print(f"  - Transit Pressure (P_tra):    {p_tra:.3f}")
                print(f"  - RPI Mismatch:                {rpi_mismatch:.3f}")
            else:
                print("\nError: Response JSON is missing expected keys.")
                print("Received data:", data)

        else:
            print(f"\n--- Test Failed (Status Code: {response.status_code}) ---")
            print("Error response:")
            print(response.text)

    except httpx.ConnectError as e:
        print("\n--- Connection Error ---")
        print("Could not connect to the ARS API.")
        print("Please ensure the ARS server is running at the specified URL.")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"\n--- An Unexpected Error Occurred ---")
        print(f"Error details: {e}")

    print("\n--- ARS Client Test Complete ---")

if __name__ == "__main__":
    run_test()
