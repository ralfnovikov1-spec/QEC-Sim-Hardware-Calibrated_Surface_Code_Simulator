from .surface_code import SurfaceCodeSim
from .noise_models import HardwareProfile
import copy

class ThermalGovernor:
    """Simulates thermodynamic instability (fridge heating up)."""
    def __init__(self, base_hardware: HardwareProfile):
        self.hardware = copy.deepcopy(base_hardware)
        self.temp_factor = 1.0 

    def step_temperature(self, cooling_active: bool):
        drift_rate = 0.05 # Noise increases 5% per step if heating
        
        if cooling_active:
            self.temp_factor = max(1.0, self.temp_factor - drift_rate * 2)
        else:
            self.temp_factor += drift_rate
            
        # Apply to T1/T2 (Higher temp = Lower Coherence)
        current_hw = copy.deepcopy(self.hardware)
        current_hw.t1_us /= self.temp_factor
        current_hw.t2_us /= self.temp_factor
        return current_hw
