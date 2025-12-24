import sys
import os
import matplotlib.pyplot as plt
# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.noise_models import GOOGLE_RAINBOW, IBM_HERON
from src.surface_code import SurfaceCodeSim

def run():
    print("\n--- PHASE 1: Standard Hardware Benchmark ---")
    distances = [3, 5, 7]
    shots = 5000
    
    for hw in [GOOGLE_RAINBOW, IBM_HERON]:
        print(f"\nTesting {hw.name}:")
        x, y = [], []
        for d in distances:
            # Rounds = 3*d is a standard stress test
            sim = SurfaceCodeSim(d, rounds=d*3, hardware=hw)
            errs = sim.run_batch(shots)
            ler = errs / shots
            print(f"  d={d}: LER = {ler:.4e}")
            x.append(d)
            y.append(ler)
        plt.semilogy(x, y, 'o-', label=hw.name)
        
    plt.xlabel("Code Distance (d)")
    plt.ylabel("Logical Error Rate")
    plt.title("Google Rainbow vs. IBM Heron (Simulated)")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig("results/benchmark_standard.png")
    print("✅ Results plotted to results/benchmark_standard.png")

if __name__ == "__main__":
    run()
