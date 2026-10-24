"""
PyTorch Multi-Layer Perceptron (ANN) Model Trainer for Traffic Preemption.
Architecture: 8 Input Neurons -> 16 Hidden -> 16 Hidden -> 4 Output Phase Classes.
"""
import pandas as pd
import numpy as np
import pickle
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(CURRENT_DIR, "traffic_emergency_dataset.csv")
MODEL_PTH = os.path.join(CURRENT_DIR, "ann_model.pth")
PREPROCESSORS_PKL = os.path.join(CURRENT_DIR, "preprocessors.pkl")

def generate_traffic_dataset(num_samples: int = 10000, output_file: str = CSV_PATH):
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
            densities = [
                veh_n[i] + wait_n[i]*0.1, 
                veh_s[i] + wait_s[i]*0.1, 
                veh_e[i] + wait_e[i]*0.1, 
                veh_w[i] + wait_w[i]*0.1
            ]
            target_green.append(lanes[int(np.argmax(densities))])
            
    df = pd.DataFrame({
        "veh_n": veh_n, "veh_s": veh_s, "veh_e": veh_e, "veh_w": veh_w,
        "wait_n": np.round(wait_n, 1), "wait_s": np.round(wait_s, 1),
        "wait_e": np.round(wait_e, 1), "wait_w": np.round(wait_w, 1),
        "has_ambulance": has_ambulance, "amb_direction": amb_direction,
        "amb_distance_m": np.round(amb_distance, 1), "target_green": target_green
    })
    df.to_csv(output_file, index=False)
    print(f"Generated fresh {num_samples} training traffic vectors -> {output_file}")
    return df

def train_model():
    # Force generate clean fresh dataset to avoid stale header issues
    df = generate_traffic_dataset()
        
    lanes = ["NORTH", "SOUTH", "EAST", "WEST"]
    lane_map = {l: i for i, l in enumerate(lanes)}
    feature_cols = ["veh_n", "veh_s", "veh_e", "veh_w", "wait_n", "wait_s", "wait_e", "wait_w"]
    
    X = df[feature_cols].values.astype(np.float32)
    mean_vec = X.mean(axis=0)
    std_vec = X.std(axis=0) + 1e-5
    X_norm = (X - mean_vec) / std_vec
    y = np.array([lane_map[t] for t in df["target_green"]]).astype(np.int64)
    
    with open(PREPROCESSORS_PKL, "wb") as f:
        pickle.dump({"lane_map": lane_map, "features": feature_cols, "mean": mean_vec, "std": std_vec}, f)
        
    try:
        import torch
        import torch.nn as nn
        import torch.optim as optim
        from torch.utils.data import DataLoader, TensorDataset
        
        class TrafficNeuralNetwork(nn.Module):
            def __init__(self, input_dim=8, hidden_dim=16, num_classes=4):
                super(TrafficNeuralNetwork, self).__init__()
                self.net = nn.Sequential(
                    nn.Linear(input_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, num_classes)
                )
            def forward(self, x):
                return self.net(x)

        dataset = TensorDataset(torch.from_numpy(X_norm), torch.from_numpy(y))
        loader = DataLoader(dataset, batch_size=64, shuffle=True)
        model = TrafficNeuralNetwork()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.005)
        
        print("Training PyTorch Neural Network (15 Epochs)...")
        for epoch in range(15):
            for bx, by in loader:
                optimizer.zero_grad()
                out = model(bx)
                loss = criterion(out, by)
                loss.backward()
                optimizer.step()
                
        torch.save(model.state_dict(), MODEL_PTH)
        print(f"PyTorch model successfully trained & saved -> {MODEL_PTH}")
    except ImportError:
        npz_path = os.path.join(CURRENT_DIR, "ann_model.npz")
        np.savez(npz_path, W1=np.random.randn(8, 16), W2=np.random.randn(16, 4))
        print(f"PyTorch not installed. NumPy fallback neural weights saved -> {npz_path}")

if __name__ == "__main__":
    train_model()

