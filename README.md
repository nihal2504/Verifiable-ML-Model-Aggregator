# Verifiable ML Model Aggregator (Rust & Kani)

This project implements a secure model aggregator for **Federated Learning** using **Rust**. It utilizes the **Kani Rust Verifier** to mathematically prove the system's resilience against model poisoning attacks.

## Security & Formal Verification
Unlike standard testing, this project uses **Bounded Model Checking** to prove safety invariants.
* **Proven Invariant:** All global model updates are strictly bounded between `[-1.0, 1.0]`.
* **Vulnerability Fixed:** Identified and patched an IEEE 754 **NaN (Not-a-Number) injection** vulnerability that could crash standard aggregators.

## Tech Stack
* **Language:** Rust (Aggregator Core)
* **Formal Methods:** Kani Rust Verifier
* **Machine Learning:** PyTorch (Integration Simulation)

## Verification Result
The core logic was verified using:
`!kani aggregator.rs`
**Status:** `VERIFICATION:- SUCCESSFUL`
