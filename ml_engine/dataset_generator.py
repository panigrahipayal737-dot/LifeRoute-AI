"""
Synthetic Traffic Emergency Dataset Generator (10,000 Junction Vectors)
"""
import pandas as pd
import numpy as np

def generate_traffic_dataset(num_samples: int = 10000, output_file: str = "ml_engine/traffic_emergency_dataset.csv"):
    np.random.seed(42)
    lanes = ["NORTH", "SOUTH", "EAST", "WEST"]
    
    veh_n = np.random.randint(2, 45, num_samples)
    veh_s = np.random.randint(2, 45, num_samples)
    veh_e = np.random.randint(2, 45, num_samples)
    veh_w = np.random.randint(2, 45, num_samples)
    
    wait_n = veh_n * np.random.uniform(1.2, 2.5, num_samples)
    wait_s = veh_s * np.random.uniform(1.2, 2.5, num_samples)
    wait_e = veh_e * np.random.uniform(1.2, 2.5, num_samples)
    wait_w = veh_w * np.random.uniform(1.2, 2.5, num_samples)
    
    has_ambulance = np.random.choice([0, 1], size=num_samples, p=[0.75, 0.25])
    amb_direction = [np.random.choice(lanes) if amb == 1 else "NONE" for amb in has_ambulance]
    amb_distance = [np.random.uniform(50.0, 950.0) if amb == 1 else -1.0 for amb in has_ambulance]
    
    target_green = []
    for i in range(num_samples):
        if has_ambulance[i] == 1:
            target_green.append(amb_direction[i])
        else:
            densities = [veh_n[i] + wait_n[i]*0.1, veh_s[i] + wait_s[i]*0.1, veh_e[i] + wait_e[i]*0.1, veh_w[i] + wait_w[i]*0.1]
            target_green.append(lanes[int(np.argmax(densities))])
            
    df = pd.DataFrame({
        "veh_n": veh_n, "veh_s": veh_s, "veh_e": veh_e, "veh_w": veh_w,
        "wait_n": np.round(wait_n, 1), "wait_s": np.round(wait_s, 1),
        "wait_e": np.round(wait_e, 1), "wait_w": np.round(wait_w, 1),
        "has_ambulance": has_ambulance, "amb_direction": amb_direction,
        "amb_distance_m": np.round(amb_distance, 1), "target_green": target_green
    })
    
    df.to_csv(output_file, index=False)
    print(f"Dataset generated successfully with {num_samples} samples -> {output_file}")

if __name__ == "__main__":
    generate_traffic_dataset()

