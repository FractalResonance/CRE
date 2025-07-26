# cre_service_public.py
# Initial CRE Service: Public Weather Report Endpoint

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
import json
import asyncio # Added for direct async function call

# --- FastAPI App Initialization ---
# This part is for actual deployment with Uvicorn.
# When run directly for testing, 'app' will not be used for HTTP routing.
try:
    app = FastAPI(
        title="CRE Public Weather Report Service",
        description="Provides the current collective resonant weather quadrant and a Gnostic Synthesis.",
        version="1.0.0"
    )
except RuntimeError:
    # This handles cases where FastAPI might complain about being initialized multiple times
    # in environments like interactive sessions.
    app = None

# --- Configuration ---
ARS_GENERAL_WEATHER_URL = "http://127.0.0.1:8000/v1/general/weather"

# --- Response Model ---
class WeatherReportResponse(BaseModel):
    quadrant_name: str = Field(..., description="The name of the active resonant weather quadrant.")
    quadrant_description: str = Field(..., description="A brief description of the quadrant's energetic signature.")
    mantra_of_the_day: str = Field(..., description="A Gnostic Synthesis or 'Mantra of the Day' for the quadrant.")

# --- Internal Logic: Quadrant Mapping and Mantras ---
def get_resonant_weather_quadrant_and_mantra(pressure: float, tension: float) -> dict:
    """
    Determines the Resonant Weather Quadrant and selects a corresponding mantra.
    """
    quadrant_data = {}
    if pressure >= 0 and tension >= 0:
        quadrant_data["quadrant_name"] = "The Forge"
        quadrant_data["quadrant_description"] = "Catalytic, Agitated"
        quadrant_data["mantra_of_the_day"] = "Embrace the friction, for it sharpens your will. Transform challenge into power."
    elif pressure >= 0 and tension < 0:
        quadrant_data["quadrant_name"] = "The River"
        quadrant_data["quadrant_description"] = "Expansive, Flowing"
        quadrant_data["mantra_of_the_day"] = "Flow with the current of creation. Connect and expand your influence."
    elif pressure < 0 and tension >= 0:
        quadrant_data["quadrant_name"] = "The Void"
        quadrant_data["quadrant_description"] = "Stuck, Frustrated"
        quadrant_data["mantra_of_the_day"] = "Pause and reflect. The answers lie within the stillness, not in external action."
    else: # pressure < 0 and tension < 0
        quadrant_data["quadrant_name"] = "The Temple"
        quadrant_data["quadrant_description"] = "Calm, Receptive"
        quadrant_data["mantra_of_the_day"] = "Rest, integrate, and receive. Allow gentle insights to emerge from deep stillness."
    return quadrant_data

# --- Mocking Mechanism for Testing ---
class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(f"Mock HTTP Error: {self.status_code}", request=None, response=self)

class MockAsyncClient:
    async def get(self, url, timeout=None):
        # Simulate ARS response for testing
        if url == ARS_GENERAL_WEATHER_URL:
            # You can change these values to test different quadrants
            mock_ars_data = {"pressure": 1.5, "tension": 0.8} # Example: Forge
            return MockResponse(mock_ars_data)
        return MockResponse({}, status_code=404) # Not found for other URLs

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# --- Endpoint Definition ---
# Only register the endpoint if 'app' was successfully initialized (for actual FastAPI server)
if app:
    @app.get("/v1/public/weather_report", response_model=WeatherReportResponse)
    async def get_public_weather_report_live():
        """
        Retrieves the current collective resonant weather report (live version).
        """
        try:
            # Step 1: Call ARS /v1/general/weather endpoint
            async with httpx.AsyncClient() as client:
                ars_response = await client.get(ARS_GENERAL_WEATHER_URL, timeout=5.0)
                ars_response.raise_for_status() # Raise an exception for bad status codes
                ars_data = ars_response.json()

            pressure = ars_data.get("pressure")
            tension = ars_data.get("tension")

            if pressure is None or tension is None:
                raise ValueError("ARS response missing 'pressure' or 'tension' data.")

            # Step 2 & 3: Translate and select mantra
            report_data = get_resonant_weather_quadrant_and_mantra(pressure, tension)
            
            return WeatherReportResponse(**report_data)

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Could not connect to ARS: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error from ARS: {exc.response.text}"
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid data from ARS: {exc}"
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {exc}"
            )

# --- Direct Test Function (for running without Uvicorn) ---
async def test_get_public_weather_report():
    """
    Tests the get_public_weather_report logic directly using a mock httpx client.
    """
    print("--- Running CRE Public Service Internal Test ---")
    try:
        # Use the MockAsyncClient for testing purposes
        async with MockAsyncClient() as client:
            ars_response = await client.get(ARS_GENERAL_WEATHER_URL)
            ars_response.raise_for_status()
            ars_data = ars_response.json()

        pressure = ars_data.get("pressure")
        tension = ars_data.get("tension")

        if pressure is None or tension is None:
            raise ValueError("Mock ARS response missing 'pressure' or 'tension' data.")

        report_data = get_resonant_weather_quadrant_and_mantra(pressure, tension)
        
        # Print the simulated response
        print("""
--- Simulated CRE Service Response ---""")
        print(json.dumps(report_data, indent=2))
        print("""
--- Internal Test Complete ---""")

    except Exception as e:
        print(f"""
--- Internal Test Failed: {e} ---""")

# --- Main execution block ---
if __name__ == "__main__":
    # Run the internal test function directly
    asyncio.run(test_get_public_weather_report())
