import time
import requests
import random

API_ENDPOINT = "http://127.0.0.1:8000/api/v1/traffic/process-snapshot"
DIRECTIONS = ["NORTH", "SOUTH", "EAST", "WEST"]

def run_simulation():
    step = 0
    print("ðŸš¦ Autonomous Traffic & Emergency Stream Simulator Started...")
    while True:
        step += 1
        is_emergency = (step % 4 == 0)
        
        amb_dir = random.choice(DIRECTIONS) if is_emergency else "NONE"
        amb_dist = round(random.uniform(400.0, 1100.0), 1) if is_emergency else -1.0
        amb_eta = round(amb_dist / (65 * 1000 / 60), 2) if is_emergency else -1.0
        
        payload = {
            "current_green": "NORTH",
            "vehicles_n": random.randint(5, 50),
            "vehicles_s": random.randint(5, 50),
            "vehicles_e": random.randint(5, 50),
            "vehicles_w": random.randint(5, 50),
            "wait_n": random.randint(10, 60),
            "wait_s": random.randint(10, 60),
            "wait_e": random.randint(10, 60),
            "wait_w": random.randint(10, 60),
            "has_ambulance": is_emergency,
            "amb_direction": amb_dir,
            "amb_distance_m": amb_dist,
            "amb_eta_min": amb_eta
        }
        
        try:
            res = requests.post(API_ENDPOINT, json=payload, timeout=2)
            if res.status_code == 200:
                data = res.json()
                print(f"[STEP {step:03d}] {'ðŸš¨ EMERGENCY' if is_emergency else 'ðŸŸ¢ NORMAL'} | ANN Target: {data['decision']['predicted_priority']} (Conf: {data['decision']['confidence']*100:.1f}%)")
        except Exception as e:
            print(f"[Sim Error] FastAPI Server not reached: {e}")
            
        time.sleep(3.5)

if __name__ == "__main__":
    run_simulation()
