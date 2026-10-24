"""
Global Configuration & System Thresholds
"""
import os

class SystemConfig:
    PROJECT_NAME: str = "LifeRoute AI • Smart Traffic OS"
    VERSION: str = "3.2.0"
    API_PREFIX: str = "/api/v1"
    
    # Radar & Vision Limits
    MAX_RADAR_RANGE_METERS: float = 1000.0
    MIN_TRIGGER_DISTANCE_METERS: float = 300.0
    AVERAGE_AMBULANCE_SPEED_KMH: float = 65.0
    
    # Penalty & Enforcement
    MVA_SECTION: str = "Section 194E MVA 2019"
    CHALLAN_PENALTY_INR: int = 10000
    
    # Multi-Junction Node IDs
    JUNCTION_NODES = ["J1_WEST_APPROACH", "J2_FLYOVER_RAMP", "J3_HOSPITAL_GATE"]

config = SystemConfig()

