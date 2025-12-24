# QEC-Sim: Hardware-Calibrated Surface Code Simulator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A high-performance quantum error correction simulator benchmarking **Rotated Surface Codes** using realistic noise models derived from published Google and IBM hardware specifications.

## 🔬 Scientific Features
1.  **Hardware-Aware Noise:** $T_1/T_2$ and gate fidelities from *Nature* (2023) and IBM Quantum Summit.
2.  **Cosmic Ray Simulation:** Spatially correlated phonon bursts using Stim's `CORRELATED_ERROR` channel.
3.  **Thermal Drift:** Time-varying coherence simulation modeling 4K stage fluctuations.
4.  **Defect Adaptation:** Graph re-weighting decoder for broken qubits.

## 🚀 Quick Start
Run the full validation suite:
\`\`\`bash
python run_suite.py
\`\`\`

## 📊 Hardware Models
| Processor | T1 (µs) | T2 (µs) | 2Q Gate Err |
| :--- | :--- | :--- | :--- |
| **Google Rainbow** | 19.3 | 26.5 | 1.0% |
| **IBM Heron** | 150.0 | 100.0 | 0.8% |

## 📚 Methodology
- **Circuit:** `stim.Circuit.generated("surface_code:rotated_memory_x")`
- **Decoder:** Minimum Weight Perfect Matching (PyMatching v2)
- **Validation:** Reproduces the $d=3$ vs $d=5$ break-even point observed in Google's *Nature* 614 paper.
