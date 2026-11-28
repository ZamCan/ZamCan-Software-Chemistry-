"""Brain-inspired orchestration, not a biological brain or trained neural model."""
from scm.everyday_chemistry import dilution, ph_from_activity, hardness_as_caco3, electrical_energy

OPERATIONS = {
    "dilution": dilution,
    "ph": ph_from_activity,
    "water-hardness": hardness_as_caco3,
    "electrical-energy": electrical_energy,
}

def reason(operation, inputs):
    """Route explicit structured requests; abstain on unsupported operations."""
    if not isinstance(operation, str):
        raise ValueError("Expected an operation name")
    if operation not in OPERATIONS:
        return {"status":"unsupported","operation":operation,
                "reason":"No registered scientific method; additional evidence or implementation required."}
    if not isinstance(inputs, dict):
        raise ValueError("Structured inputs required")
    if any(isinstance(value, bool) or not isinstance(value, (int, float))
           for value in inputs.values()):
        raise ValueError("Measurements must be numeric")
    result = OPERATIONS[operation](**inputs)
    return {"status":"calculated","operation":operation,"method_version":"1",
            "inputs":dict(inputs),"result":result,
            "validation_status":"not_independently_benchmarked",
            "trace":["select_registered_method","check_inputs","calculate","label_evidence_and_limits"],
            "experimental_confirmation":False}
