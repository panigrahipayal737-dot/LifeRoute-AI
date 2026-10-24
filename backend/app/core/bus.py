import json
import os

BUS_FILE = "active_emergency_bus.json"

def get_live_bus():
    if os.path.exists(BUS_FILE):
        try:
            with open(BUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def set_live_bus(data):
    with open(BUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clear_live_bus():
    if os.path.exists(BUS_FILE):
        try:
            with open(BUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["status"] = "RESOLVED"
            with open(BUS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
