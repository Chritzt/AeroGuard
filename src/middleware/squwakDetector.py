# middleware/squwakDetector.py
from typing import List, Dict, Any

class SquawkDetector : 

    """
    Detects emergency and security squawk codes in aircraft telemetry
    """

    def detect_unusual_codes(self, aircraft_list: List[Any]) -> List[Dict[str, Any]]:
            alerts = []

            for aircraft in aircraft_list:
                if not aircraft.squawk:
                    continue

                match aircraft.squawk:
                    case "7700":
                        alerts.append({
                            "icao24": aircraft.icao24,
                            "callsign": aircraft.callsign,
                            "code": "7700",
                            "threat": "GENERAL EMERGENCY"
                        })
                    case "7600":
                        alerts.append({
                            "icao24": aircraft.icao24,
                            "callsign": aircraft.callsign,
                            "code": "7600",
                            "threat": "RADIO FAILURE (COMM LOSS)"
                        })
                    case "7500":
                        alerts.append({
                            "icao24": aircraft.icao24,
                            "callsign": aircraft.callsign,
                            "code": "7500",
                            "threat": "UNLAWFUL INTERFERENCE (HIJACKING)"
                        })
                    case _:
                        pass

            return alerts