# src/main.py
from routes.api import AviationAPIClient
from middleware.squwakDetector import SquawkDetector

def main():
    print("[*] AeroGuard Engine running...")
    
    client = AviationAPIClient()
    detector = SquawkDetector()
    
    aircrafts = client.get_live_states()
    print(f"[+] Fetched {len(aircrafts)} aircrafts.")
    
    alerts = detector.detect_unusual_codes(aircrafts)
    
    if alerts:
        print(f"[!] ALERT: Found {len(alerts)} emergency squawking aircraft!")
        for alert in alerts:
            print(f"    -> ICAO: {alert['icao24']} | Callsign: {alert['callsign']} | Code: {alert['code']} ({alert['threat']})")
    else:
        print("[+] All clear. No emergency squawks detected.")

if __name__ == "__main__":
    main()