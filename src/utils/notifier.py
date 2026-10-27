# utils/notifier.py
import requests
import os

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_security_alert(self, incident: dict):
        if not self.webhook_url:
            return 

        color = 15158332 if incident["threat_score"] >= 80 else 16776960 

        squawk_code = incident.get("squawk", None)
        title_prefix = "🚨 AERO-GUARD SECURITY ALERT"

        if squawk_code in ["7500", "7600", "7700"]:
            color = 10038562 
            if squawk_code == "7500":
                title_prefix = "🚨 SQUAWK 7500: UNLAWFUL INTERFERENCE / HIJACKING"
            elif squawk_code == "7600":
                title_prefix = "⚠️ SQUAWK 7600: RADIO FAILURE"
            elif squawk_code == "7700":
                title_prefix = "🔥 SQUAWK 7700: GENERAL EMERGENCY"

        fields = [
            {"name": "Aircraft ICAO", "value": f"`{incident['icao24']}`", "inline": True},
            {"name": "Callsign", "value": f"`{incident.get('callsign', 'N/A')}`", "inline": True},
        ]

        if squawk_code:
            fields.append({"name": "Transponder Squawk", "value": f"🔴 **{squawk_code}**", "inline": True})

        fields.append({
            "name": "Threat Indicators", 
            "value": "\n".join([f"• {ind}" for ind in incident["indicators"]]), 
            "inline": False
        })

        payload = {
            "embeds": [
                {
                    "title": f"{title_prefix} (Score: {incident['threat_score']}/100)",
                    "color": color,
                    "fields": fields,
                    "footer": {
                        "text": "AeroGuard Critical Infrastructure Protection | Austrian Airspace"
                    }
                }
            ]
        }

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            if response.status_code != 204:
                print(f"[!] Failed to send Discord alert: {response.status_code}")
        except Exception as e:
            print(f"[!] Error connecting to Discord webhook: {e}")