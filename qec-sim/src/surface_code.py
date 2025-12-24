import stim
import pymatching
import numpy as np
from .noise_models import HardwareProfile

class SurfaceCodeSim:
    def __init__(self, distance: int, rounds: int, hardware: HardwareProfile):
        self.distance = distance
        self.rounds = rounds
        self.hardware = hardware
        
        # Physics-to-Stim Translation
        self.p_1q = hardware.two_qubit_error / 10.0 
        self.p_2q = hardware.two_qubit_error
        self.p_reset = hardware.readout_error / 2.0
        self.p_meas = hardware.readout_error
        self.p_idle = hardware.get_idle_error()

    def generate_circuit(self, cosmic_ray_model=None):
        """Generates the Stim circuit, optionally injecting cosmic ray bursts."""
        circuit = stim.Circuit.generated(
            "surface_code:rotated_memory_x",
            distance=self.distance,
            rounds=self.rounds,
            after_clifford_depolarization=self.p_1q,
            after_reset_flip_probability=self.p_reset,
            before_measure_flip_probability=self.p_meas,
            before_round_data_depolarization=self.p_idle
        )

        if cosmic_ray_model:
            circuit = cosmic_ray_model.apply_to_circuit(circuit, self.distance)
            
        return circuit

    def run_batch(self, num_shots: int = 1000, cosmic_ray_model=None):
        """Runs simulation batch and returns error count."""
        circuit = self.generate_circuit(cosmic_ray_model)
        
        dem = circuit.detector_error_model(decompose_errors=True)
        decoder = pymatching.Matching.from_detector_error_model(dem)
        
        sampler = circuit.compile_detector_sampler()
        syndromes, observables = sampler.sample(shots=num_shots, separate_observables=True)
        
        predictions = decoder.decode_batch(syndromes)
        num_errors = np.sum(np.any(predictions != observables, axis=1))
        return num_errors
