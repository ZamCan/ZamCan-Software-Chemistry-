from zcm.cli import scientific_operation

def test_conservation_dispatch():
    result = scientific_operation("conservation", {
        "reactants": [[2, {"H":2}, 0], [1, {"O":2}, 0]],
        "products": [[2, {"H":2,"O":1}, 0]]})
    assert result["status"] == "conserved"

def test_property_dispatch():
    record = {"identity":"water", "property":"density", "unit":"kg/m3",
              "conditions":{"temperature_k":298.15,"pressure_pa":101325},
              "value":997, "standard_uncertainty":1,
              "evidence":{"source":"synthetic fixture","version":"1","origin":"computational"}}
    result = scientific_operation("compare-properties", {"a":record,"b":{**record,"value":996}})
    assert result["difference"] == 1
    assert scientific_operation("compare-properties", {"a":record,"b":{**record,"unit":"g/L"}})["status"] == "incomparable"

def test_benchmark_dispatch():
    result=scientific_operation("benchmark",dict(predictions=[1],references=[1],
        unit="J/mol",reference_origin="computational",dataset_version="fixture",
        mae_limit=0,max_error_limit=0))
    assert result["passed"]
