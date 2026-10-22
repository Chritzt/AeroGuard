# routes/api.py
import requests
from typing import List
from models.models import AircraftState

class AviationAPIClient:
    BASE_URL = "https://opensky-network.org/api/states/all"

    def get_live_states(self) -> List[AircraftState]:
        # Bounding Box for Austria
        params = {
            "lamin": 46.37,
            "lamax": 49.02,
            "lomin": 9.53,
            "lomax": 17.16
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            aircraft_list = []
            states = data.get("states", []) or []
            
            for s in states:
                aircraft = AircraftState(
                    icao24=s[0],
                    callsign=s[1].strip() if s[1] else None,
                    origin_country=s[2],
                    longitude=s[5],
                    latitude=s[6],
                    baro_altitude=s[7],
                    velocity=s[9],
                    squawk=s[14] if len(s) > 14 and s[14] else None,
                    on_ground=s[8]
                )
                aircraft_list.append(aircraft)
            return aircraft_list
        except Exception as e:
            print(f"[!] Error fetching OpenSky data: {e}")
            return []