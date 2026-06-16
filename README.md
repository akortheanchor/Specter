# 🕵️ SPECTER

**S**tealth **P**erturbation **E**ngine via **C**ircuit-based **T**unneling and **E**pidemiological **R**esilience

> *A Red-Team Quantum Adversarial Framework for Hardening Medical Imaging AI*
> Published in: **Journal of Computer Virology and Hacking Techniques** (Springer Nature)

---

![SPECTER Banner](assets/gifs/specter_banner.gif)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.44%2B-purple?logo=ibm)](https://qiskit.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange?logo=pytorch)](https://pytorch.org)
[![Stars](https://img.shields.io/github/stars/specter-medsec/SPECTER?style=social)](https://github.com/specter-medsec/SPECTER)

---

## 🔬 Overview

SPECTER is the first framework to unify:

| Component | Description | Animation |
|-----------|-------------|-----------|
| **QAPE** | Quantum Adversarial Perturbation Engine (QAOA-based attack) | ![QAPE](assets/gifs/qape_attack.gif) |
| **SIR-PACS** | Epidemiological propagation model for hospital networks | ![SIR](assets/gifs/sir_propagation.gif) |
| **QPUF-DICOM** | Quantum Physical Unclonable Function DICOM defence | ![QPUF](assets/gifs/qpuf_defence.gif) |

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| QAPE Attack Success Rate (vs AutoAttack) | **+10.2%** |
| Clean → Under-QAPE accuracy drop | **91.9% → 29.8%** |
| QPUF Detection AUC | **0.994** |
| QPUF Detection Latency @ 1024² | **< 50 ms** |
| QPUF-restored accuracy | **90.5%** |
| Epidemic R₀ (undefended PACS) | **7.0** |
| Epidemic R₀ (QPUF-hardened) | **0.53** |

---

## 🚀 Quick Start

```bash
git clone https://github.com/specter-medsec/SPECTER.git
cd SPECTER
pip install -r requirements.txt
```

### Run QAPE Attack
```python
from specter.qape import QAPEAttack

attacker = QAPEAttack(n_qubits=16, p_layers=7, epsilon=0.02)
x_adv = attacker.attack(model, x_clean, y_true)
```

### Run QPUF Defence
```python
from specter.qpuf import QPUFDefence

defender = QPUFDefence(n_qubits=64, noise_tolerance=3)
is_authentic = defender.verify_dicom("scan.dcm")
```

### Run SIR Network Simulation
```python
from specter.sir import SIRPACSModel

sir = SIRPACSModel(N=1000, beta=0.35, gamma=0.05)
trajectory = sir.simulate(days=120, initial_infected=5)
sir.plot_epidemic_curve(trajectory)
```

---

## 📁 Repository Structure

```
SPECTER/
├── specter/
│   ├── qape/          # Quantum Adversarial Perturbation Engine
│   │   ├── circuit.py         # QAOA circuit construction
│   │   ├── attack.py          # End-to-end QAPE attack
│   │   └── qubo.py            # QUBO problem formulation
│   ├── sir/           # SIR Epidemiological Model
│   │   ├── model.py           # ODE system + solver
│   │   ├── network.py         # Graph-based PACS network
│   │   └── visualise.py       # Epidemic curve plotting
│   ├── qpuf/          # Quantum PUF Defence
│   │   ├── puf.py             # QPUF construction
│   │   ├── dicom.py           # DICOM integrity protocol
│   │   └── verify.py          # Challenge-response verification
│   ├── models/        # Diagnostic AI backbone models
│   │   └── resnet_medical.py
│   └── utils/         # Shared utilities
│       ├── metrics.py
│       └── visualise.py
├── tests/             # Unit + integration tests
├── notebooks/         # Jupyter demo notebooks
├── assets/gifs/       # Animated demonstrations
├── docs/              # Extended documentation
├── requirements.txt
├── setup.py
└── README.md
```

---

## 📦 Installation

```bash
# Standard install
pip install -e .

# With quantum hardware support
pip install -e ".[quantum]"

# Full research environment
pip install -e ".[all]"
```

---

## 📖 Citation

```bibtex
@article{selvam2024specter,
  title   = {{SPECTER}: A Stealth Perturbation Engine via Circuit-based Tunneling
             and Epidemiological Resilience for Hardening Medical Imaging {AI}},
  author  = {Selvam, Rajesh Kumar and Anandakrishnan, Priya and
             Al-Rashidi, Mohammed and Vasilieva, Elena},
  journal = {Journal of Computer Virology and Hacking Techniques},
  year    = {2024},
  publisher = {Springer Nature}
}
```

---

## 📜 License

MIT License — see [LICENSE](LICENSE)

---

*"The hacker's instinct to seek the most powerful available tool, paired with the scientist's discipline of formal proofs and rigorous benchmarking."*
