import torch

print("=== Verifiable ML Model Aggregator ===")
print("Running Secure Federated Learning Simulation (Pure PyTorch Mode)\n")

# -- 1. Setup Mock Neural Network Architecture --
# Imagine a small 2-layer Neural Network
# Layer 1: weights of shape (3, 3)
# Layer 2: biases of shape (3,)

def generate_mock_client_model(base_val, noise_scale=0.1):
    """Generates a mock model update based on a base value with some noise."""
    layer1 = torch.ones(3, 3) * base_val + torch.randn(3, 3) * noise_scale
    layer2 = torch.ones(3) * base_val + torch.randn(3) * noise_scale
    return {"layer1": layer1, "layer2": layer2}

# -- 2. Simulate Client Nodes --
# We have 5 clients participating in Federated Learning
print("[*] Receiving updates from 5 Client Nodes...")

clients = [
    generate_mock_client_model(0.1),  # Client 1: Normal
    generate_mock_client_model(0.3),  # Client 2: Normal
    generate_mock_client_model(-0.2), # Client 3: Normal
]

# Client 4: Malicious actor trying to introduce NaN poisoning
poisoned_model_nan = generate_mock_client_model(0.0)
poisoned_model_nan["layer1"][1, 1] = float('nan')
clients.append(poisoned_model_nan)

# Client 5: Malicious actor trying a weight-scaling attack (massive outlier)
poisoned_model_outlier = generate_mock_client_model(1000.0)
clients.append(poisoned_model_outlier)

print("[!] Included potentially malicious updates (NaNs and Outlier weights).")

# -- 3. Verified Aggregation Logic (Simulating Rust Kani Constraints) --

def secure_fedavg(client_models):
    """
    Safely calculates the average of models across all clients.
    Mirrors the constraints formally verified by Kani (in aggregator.rs):
    - Replaces NaNs with 0.0
    - Clamps updates between -1.0 and 1.0
    """
    print("\n[*] Initializing Secure FedAvg Aggregation...")
    
    # Store aggregated sum for averaging
    aggregated_global_model = {"layer1": torch.zeros(3, 3), "layer2": torch.zeros(3)}
    num_clients = len(client_models)
    
    for i, model in enumerate(client_models):
        for layer_name in model.keys():
            tensor = model[layer_name]
            
            # Constraint 1: Handle NaNs (Poison mitigation)
            clean_tensor = torch.nan_to_num(tensor, nan=0.0)
            
            # Constraint 2: Bounded Values [-1.0, 1.0] (Overflow mitigation)
            bounded_tensor = torch.clamp(clean_tensor, min=-1.0, max=1.0)
            
            # Add to global model
            aggregated_global_model[layer_name] += bounded_tensor
            
    # Compute the mean
    for layer_name in aggregated_global_model.keys():
        aggregated_global_model[layer_name] /= num_clients
        
    return aggregated_global_model

# -- 4. Execution and Output --
global_model = secure_fedavg(clients)

print("\n=== Final Global Model Weights ===")
print("Layer 1:\n", global_model["layer1"])
print("Layer 2:\n", global_model["layer2"])
print("\n[SUCCESS] Aggregation complete: No NaNs propagated, and all weights survived within strict mathematical bounds!")