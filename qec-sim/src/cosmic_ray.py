import stim
import numpy as np

class CosmicRayModel:
    """Injects spatially correlated errors (muon strikes) into Stim circuits."""
    def __init__(self, flux_rate: float = 0.0001, radius: int = 2):
        self.flux_rate = flux_rate 
        self.radius = radius       

    def apply_to_circuit(self, circuit: stim.Circuit, distance: int):
        new_circuit = stim.Circuit()
        width = 2 * distance + 1
        
        for instruction in circuit:
            new_circuit.append(instruction)
            # After every TICK, check for cosmic ray
            if instruction.name == "TICK":
                self._inject_correlation_op(new_circuit, width)
        return new_circuit

    def _inject_correlation_op(self, circuit, width):
        # Random impact center
        center_x = np.random.randint(0, width)
        center_y = np.random.randint(0, width)
        
        targets = []
        # Find qubits within radius
        for x in range(max(0, center_x - self.radius), min(width, center_x + self.radius + 1)):
            for y in range(max(0, center_y - self.radius), min(width, center_y + self.radius + 1)):
                # Map 2D coord to 1D qubit index (approximate for surface code)
                q_idx = y * width + x
                targets.append(stim.target_x(q_idx))
                targets.append(stim.target_z(q_idx))
            
        if targets:
            # Stim instruction: With probability p, apply errors to ALL targets
            circuit.append("CORRELATED_ERROR", targets, self.flux_rate)
