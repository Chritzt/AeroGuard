# middleware/spoofingDetector.py
from typing import List, Dict, Any
from collections import Counter
import math
from models.models import AircraftState

class SpoofingDetector: 
    def __init__(self):
        self.aircraft_history: Dict[str, Dict[str, float]] = {}

    def check_for_anomalies(self, aircraft_list: List[AircraftState]) -> List[Dict[str, Any]]:
        incident_map: Dict[str, Dict[str, Any]] = {}

        identity_alerts = self.check_identity_hijacking(aircraft_list)
        for alert in identity_alerts:
            icao = alert["icao24"]
            if icao not in incident_map:
                incident_map[icao] = {
                    "icao24": icao,
                    "callsign": alert["callsign"],
                    "threat_score": 0,
                    "indicators": []
                }
            incident_map[icao]["threat_score"] += 90 
            incident_map[icao]["indicators"].append("IDENTITY HIJACKING / CLONED TRANSPONDER")

        for aircraft in aircraft_list:
            icao = aircraft.icao24

            is_velo_anomaly, velo_diff = self.velo_anom_detector(aircraft)
            
            is_jump_anomaly, jump_msg = self.check_telemetry_jump(aircraft)

            if is_velo_anomaly or is_jump_anomaly:
                if icao not in incident_map:
                    incident_map[icao] = {
                        "icao24": icao,
                        "callsign": aircraft.callsign,
                        "threat_score": 0,
                        "indicators": []
                    }
                
                if is_velo_anomaly:
                    incident_map[icao]["threat_score"] += 50
                    incident_map[icao]["indicators"].append(f"UNPHYSICAL VELOCITY ({velo_diff:.1f} km/h)")

                if is_jump_anomaly:
                    incident_map[icao]["threat_score"] += 70
                    incident_map[icao]["indicators"].append(f"TELEMETRY JUMP ({jump_msg})")

        final_incidents = []
        for icao, data in incident_map.items():
            data["threat_score"] = min(data["threat_score"], 100)
            final_incidents.append(data)

        final_incidents.sort(key=lambda x: x["threat_score"], reverse=True)

        return final_incidents

    def velo_anom_detector(self, aircraft: AircraftState) -> tuple[bool, float]:
        if aircraft.velocity is None:
            return False, 0.0

        velo_kmh = aircraft.velocity * 3.6

        if velo_kmh > 1225: 
            return True, velo_kmh - 1225
        if velo_kmh < 0:    
            return True, velo_kmh

        return False, 0.0

    def check_identity_hijacking(self, aircraft_list: List[AircraftState]) -> List[Dict[str, Any]]:
        alerts = []
        icao_counts = Counter(aircraft.icao24 for aircraft in aircraft_list)
        
        for aircraft in aircraft_list:
            if icao_counts[aircraft.icao24] > 1:
                if not any(a["icao24"] == aircraft.icao24 for a in alerts):
                    alerts.append({
                        "icao24": aircraft.icao24,
                        "callsign": aircraft.callsign,
                    })
        return alerts 

    def check_telemetry_jump(self, aircraft: AircraftState) -> tuple[bool, str]:
        icao = aircraft.icao24
        curr_lat = aircraft.latitude
        curr_lon = aircraft.longitude

        if curr_lat is None or curr_lon is None:
            return False, ""

        if icao in self.aircraft_history:
            last_lat = self.aircraft_history[icao]["lat"]
            last_lon = self.aircraft_history[icao]["lon"]

            distance_km = self._calculate_distance(last_lat, last_lon, curr_lat, curr_lon)

            if distance_km > 100.0:
                self.aircraft_history[icao] = {"lat": curr_lat, "lon": curr_lon}
                return True, f"Jumped {distance_km:.1f} km"

        self.aircraft_history[icao] = {"lat": curr_lat, "lon": curr_lon}
        return False, ""

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        return R * c