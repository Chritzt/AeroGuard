#src/app.py
from routes.api import AviationAPIClient

def main():
    print("[*] AeroGuard Engine initializing...")
    
    client = AviationAPIClient()
    
    raw_data = client.fetch_flight_data()
    
    print(f"[+] Fetched {len(raw_data)} items from API.")
    # TODO: Hier übergeben wir die Daten später an die Anomaly/Threat Engine

if __name__ == "__main__":
    main()