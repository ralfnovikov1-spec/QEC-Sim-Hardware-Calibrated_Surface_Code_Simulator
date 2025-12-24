import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.noise_models import GOOGLE_RAINBOW
from src.surface_code import SurfaceCodeSim
from src.cosmic_ray import CosmicRayModel
from src.thermal_drift import ThermalGovernor

def run():
    print("\n--- PHASE 2: Hybrid Feature Stress Test ---")
    hw = GOOGLE_RAINBOW
    d = 5
    shots = 2000
    
    # 1. Cosmic Ray Test
    print("1. Injecting Cosmic Ray Bursts...")
    sim = SurfaceCodeSim(d, d*3, hw)
    # High flux rate for demonstration
    cosmic = CosmicRayModel(flux_rate=0.002, radius=2) 
    err = sim.run_batch(shots, cosmic_ray_model=cosmic)
    print(f"   Cosmic LER: {err/shots:.4e} (Baseline approx 1e-3)")

    # 2. Thermal Drift Test
    print("2. Simulating Thermal Runaway...")
    gov = ThermalGovernor(hw)
    history = []
    print("   Time Step | T1 (us) | LER")
    for t in range(5):
        # Simulate heating (cooling=False)
        degraded_hw = gov.step_temperature(cooling_active=False)
        sim_thermal = SurfaceCodeSim(d, d, degraded_hw)
        err_t = sim_thermal.run_batch(shots)
        print(f"   t={t}       | {degraded_hw.t1_us:.1f}    | {err_t/shots:.4e}")

if __name__ == "__main__":
    run()
