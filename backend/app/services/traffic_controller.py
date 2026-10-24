"""
Traffic Controller Logic: Manages 4-way signal transitions and emergency override preemption.
"""
from typing import Dict, Any

class TrafficSignalController:
    def __init__(self):
        self.current_green = "NORTH"
        self.phase_timer = 25
        self.emergency_override = False

    def update_cycle(self, active_dispatch: dict = None) -> Dict[str, Any]:
        if active_dispatch and active_dispatch.get("status") == "ACTIVE":
            self.emergency_override = True
            self.current_green = active_dispatch.get("corridor_lane", "WEST")
            return {
                "phase": f"🚨 EMERGENCY OVERRIDE ({self.current_green} LOCKED)",
                "green_lane": self.current_green,
                "hold_time_sec": 999,
                "status": "GREEN_WAVE_ACTIVE"
            }
        else:
            self.emergency_override = False
            return {
                "phase": f"AUTOMATED ADAPTIVE CYCLE ({self.current_green})",
                "green_lane": self.current_green,
                "hold_time_sec": self.phase_timer,
                "status": "NORMAL_OPERATION"
            }

signal_engine = TrafficSignalController()

