"""
LifeRoute AI - 4-Way Junction Simulation Engine (CLI & Headless Mode)
"""
import time
import random

class VirtualJunction:
    def __init__(self):
        self.lanes = {"NORTH": 14, "SOUTH": 18, "EAST": 22, "WEST": 10}
        self.current_green = "NORTH"
        self.ambulance_active = False

    def step(self):
        for lane in self.lanes:
            self.lanes[lane] += random.choice([0, 1, 2])
        self.lanes[self.current_green] = max(0, self.lanes[self.current_green] - 3)

    def trigger_emergency(self, lane: str):
        self.ambulance_active = True
        self.current_green = lane
        print(f"\n[V2X PREEMPTION ENGAGED] Forced Green-Wave on {lane} Approach!")

    def display(self):
        print("\n--- 4-WAY JUNCTION STATE MATRIX ---")
        for lane, count in self.lanes.items():
            state = "🟢 GREEN" if lane == self.current_green else "🔴 RED"
            print(f"• {lane:6s}: {count:02d} Vehicles | Signal: {state}")

if __name__ == "__main__":
    sim = VirtualJunction()
    print("Initializing 4-Way Traffic Junction Simulator...")
    for _ in range(3):
        sim.step()
        sim.display()
        time.sleep(0.5)

