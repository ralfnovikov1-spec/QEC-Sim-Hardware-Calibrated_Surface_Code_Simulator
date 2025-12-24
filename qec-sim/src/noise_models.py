"""
Physics-based noise models derived from published hardware specifications.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class HardwareProfile:
    name: str
    t1_us: float          # Relaxation time
    t2_us: float          # Dephasing time
    gate_time_ns: float   # 1Q gate time
    cycle_time_ns: float  # Surface code cycle time
    readout_error: float  # Measurement flip prob
    two_qubit_error: float # Entangling gate fidelity (1 - F)

    def get_idle_error(self) -> float:
        """
        Approximates decoherence as a depolarizing channel during idle steps.
        P_err ~ 1 - exp(-t/T) ≈ t/T
        """
        t = self.cycle_time_ns / 1000.0 # Convert to us
        p_t1 = 1 - np.exp(-t / self.t1_us)
        p_t2 = 1 - np.exp(-t / self.t2_us)
        return p_t1 + p_t2

# Source: Google Quantum AI, Nature 614, 676 (2023)
GOOGLE_RAINBOW = HardwareProfile(
    name="Google Rainbow (2023)",
    t1_us=19.3,
    t2_us=26.5,
    gate_time_ns=25.0,
    cycle_time_ns=1000.0,
    readout_error=0.020,
    two_qubit_error=0.010
)

# Source: IBM Quantum Summit 2023 / Heron specs
IBM_HERON = HardwareProfile(
    name="IBM Heron (2024)",
    t1_us=150.0,
    t2_us=100.0,
    gate_time_ns=40.0,
    cycle_time_ns=1200.0,
    readout_error=0.015,
    two_qubit_error=0.008 
)
