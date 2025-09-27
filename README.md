# Actuarial Credibility Tools

A Python library providing implementations of various actuarial credibility methods including:

- Classical (Limited Fluctuation) credibility
- Bühlmann and Bühlmann-Straub credibility  
- Bayesian credibility with conjugate priors

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Classical Credibility

```python
from credibility_tools import (
    classical_full_credibility_frequency,
    classical_full_credibility_pure_premium, 
    classical_partial_credibility
)

# Calculate full credibility standard
n_full = classical_full_credibility_frequency(p=0.95, k=0.05)

# Calculate credibility factor  
z = classical_partial_credibility(n=observed_claims, n_full=n_full)

# Apply credibility blend
estimate = z * observed_rate + (1 - z) * complement_rate
```

### Bühlmann Credibility

```python
from credibility_tools import BuhlmannInputs, buhlmann

data = {"risk_1": [1.2, 1.5], "risk_2": [2.1, 1.9]}
result = buhlmann(BuhlmannInputs(data=data))
```

### Bayesian Credibility

```python
from credibility_tools import bayes_poisson_gamma

# Poisson-Gamma conjugate updating
posterior = bayes_poisson_gamma(
    prior_alpha=2.0, prior_beta=100.0,
    total_counts=15, total_exposure=120
)
print(f"Posterior mean: {posterior.mean}")
print(f"Credibility weight: {posterior.credibility_Z}")
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run the CAS exam benchmarks:

```bash
python tests/harness.py
```

## License

MIT License
