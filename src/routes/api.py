import requests

class AviationAPIClient:
    BASE_URL = "https://opensky-network.org/api/states/all"

    def fetch_flight_data(self):
        # Box for Austria
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
            
            # All Planes in Austria
            return data.get("states", []) or []
            
        except Exception as e:
            print(f"[!] Error fetching OpenSky data: {e}")
            return []