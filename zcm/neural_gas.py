"""Experimental ideal-gas neural surrogate; never replaces the exact law."""
import math

def evaluate(n, temperature, volume, weights):
    """SI inputs: mol, K, m³. Weights from the synthetic log-space benchmark."""
    if not all(math.isfinite(x) and x > 0 for x in (n, temperature, volume)):
        raise ValueError("Positive finite SI inputs required")
    x = [math.log(q) for q in (n, temperature, volume)]
    exact = 8.31446261815324 * n * temperature / volume
    if any(abs(q) > 1 for q in x):
        return {"pressure_pa": exact, "status": "calculated", "neural_pressure_pa": None}
    h = [math.tanh(sum(x[i]*weights["w"][i][j] for i in range(3))+weights["b"][j]) for j in range(16)]
    predicted = 8.31446261815324 * math.exp(sum(h[j]*weights["v"][j][0] for j in range(16))+weights["c"][0])
    return {"pressure_pa": exact, "status": "calculated", "neural_pressure_pa": predicted,
            "neural_status": "predicted", "relative_error": abs(predicted-exact)/exact}
