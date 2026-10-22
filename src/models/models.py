# models/models.py
from pydantic import BaseModel
from typing import Optional

class AircraftState(BaseModel):
    icao24: str               
    callsign: Optional[str]   
    origin_country: str       
    longitude: Optional[float]
    latitude: Optional[float]
    baro_altitude: Optional[float] 
    velocity: Optional[float]      
    squawk: Optional[str]          
    on_ground: bool