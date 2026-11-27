import pytest
from scm.scientific_validation import benchmark, conservation_residual

def test_benchmark():
    kw = dict(unit="kJ/mol", reference_origin="computational",
              dataset_version="synthetic-test-v1", mae_limit=1, max_error_limit=2)
    r = benchmark([2, 5], [1, 4], **kw)
    assert r.passed and r.mae == 1
    assert not benchmark([2, 9], [1, 4], **kw).passed
    with pytest.raises(ValueError):
        benchmark([float("nan")], [1], **kw)
    with pytest.raises(ValueError):
        benchmark([], [], **kw)

def test_conservation():
    left = [(2, {"H": 2}, 0), (1, {"O": 2}, 0)]
    assert conservation_residual(left, [(2, {"H": 2, "O": 1}, 0)]) == {"atoms": {}, "charge": 0}
    assert conservation_residual(left, [(1, {"H": 2, "O": 1}, 0)])["atoms"]
    assert conservation_residual([(1, {"Na": 1}, 0)], [(1, {"Na": 1}, 1)])["charge"] == 1
    with pytest.raises(ValueError):
        conservation_residual([(0, {"H": 1}, 0)], [(1, {"H": 1}, 0)])
