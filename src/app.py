# src/app.py
import time
from routes.api import AviationAPIClient
from middleware.spoofingDetector import SpoofingDetector
from middleware.squwakDetector import SquawkDetector
from utils.notifier import DiscordNotifier
from dotenv import load_dotenv
import os

load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def main():
    print("[*] AeroGuard Engine starting continuous monitoring...")
    
    client = AviationAPIClient()
    detector = SpoofingDetector()
    squwak = SquawkDetector()
    
    while True:
        try:
            print("\n--------------------------------------------------")
            print("[*] Fetching live telemetry from OpenSky...")
            aircrafts = client.get_live_states()
            print(f"[+] Fetched {len(aircrafts)} aircrafts in Austrian airspace.")
            
            incidents = detector.check_for_anomalies(aircrafts)
            notifier = DiscordNotifier(webhook_url)
            
            if incidents:
                print(f"[!] SECURITY ALERT: Found {len(incidents)} suspicious aircraft!")
                for inc in incidents:
                    print(f"    -> ICAO: {inc['icao24']} | Callsign: {inc['callsign']} | Score: {inc['threat_score']}/100")
                    for indicator in inc["indicators"]:
                        print(f"       * {indicator}")

                    notifier.send_security_alert(inc)
            else:
                print("[+] All clear. No anomalies detected.")

            unusual_codes = squwak.detect_unusual_codes(aircrafts)

            if unusual_codes : 
                print("[!] EMERGENCY Codes detected: ")
                for inc in unusual_codes:
                    print(f"    -> ICAO: {inc['icao24']} | Callsign: {inc['callsign']} | Code: {inc['code']} | threat: {inc['threat']}/100")

                    notifier.send_security_alert(inc)
            else : 
                print("[+] All clear. No Emergencies")
                
        except Exception as e:
            print(f"[!] Error during telemetry cycle: {e}")
            
        print("[*] Waiting 10 seconds for next poll...")
        time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] AeroGuard Engine gracefully stopped by user.")