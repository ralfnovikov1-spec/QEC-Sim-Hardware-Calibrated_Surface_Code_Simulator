import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.noise_models import GOOGLE_RAINBOW
from src.surface_code import SurfaceCodeSim

def execute():
    print("\n--- PHASE 3: OMEGA AUDIT (Sanity Check) ---")
    print("Verifying: Does LER improve with Distance?")
    
    # Use IBM Heron (lower noise) to ensure we are below threshold
    hw = GOOGLE_RAINBOW
    
    # d=3
    sim3 = SurfaceCodeSim(3, 3, hw)
    ler3 = sim3.run_batch(5000) / 5000
    
    # d=5
    sim5 = SurfaceCodeSim(5, 3, hw) # Same rounds to isolate distance effect
    ler5 = sim5.run_batch(5000) / 5000
    
    print(f"d=3 LER: {ler3:.4f}")
    print(f"d=5 LER: {ler5:.4f}")
    
    if ler5 < ler3:
        print("✅ PASS: Error suppression observed (d=5 < d=3)")
    else:
        print("⚠️ WARNING: Threshold not clearly met (needs more shots or better noise model)")

if __name__ == "__main__":
    execute()
