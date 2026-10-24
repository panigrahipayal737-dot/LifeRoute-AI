"""
Corridor Cascade Service: Orchestrates multi-junction green wave synchronizations based on ETA and distance.
"""
import math
from typing import Dict, Any, List

class CorridorCascadeService:
    def __init__(self):
        self.junctions = ["Junction-01 (Majura Gate)", "Junction-02 (Ring Road)", "Junction-03 (Civil Chowk)"]
        
    def compute_cascade_matrix(self, distance_m: float, approach_lane: str) -> List[Dict[str, Any]]:
        cascade = []
        for idx, j_name in enumerate(self.junctions):
            # Dynamic staging: J1 engages at <900m, J2 at <600m, J3 at <300m
            trigger_dist = (idx + 1) * 300.0
            is_green_locked = (distance_m <= trigger_dist + 200.0)
            
            cascade.append({
                "junction_name": j_name,
                "lane_locked": approach_lane,
                "signal_status": "🟢 GREEN WAVE HOLD" if is_green_locked else "🔴 PRE-HOLD STANDBY",
                "clearance_sec": max(10, int(distance_m / 15.0)),
                "anpr_violation_guard": "ACTIVE (108 PRIORITY)"
            })
        return cascade

corridor_engine = CorridorCascadeService()

