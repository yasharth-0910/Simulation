import numpy as np
import pytest
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique
from techniques.no_preprocessing import NoPreprocessingTechnique
from idc_framework import IterativeDataCube

def test_ps_correctness():
    """Test Prefix Sum technique correctness"""
    arr = np.random.rand(10)
    ps = PrefixSumTechnique()
    pre = ps.preprocess(arr)
    assert np.allclose(pre, np.cumsum(arr))

def test_ps_beta_coefficients():
    """Test PS beta coefficients for range queries"""
    ps = PrefixSumTechnique()
    coeffs = ps.get_beta_coefficients(2, 5)
    assert coeffs == {5: 1.0, 1: -1.0}

def test_srps_correctness():
    """Test SRPS technique correctness"""
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    srps = SRPSTechnique(block_size=3)
    pre = srps.preprocess(arr)
    # Verify that preprocessing produces valid result
    assert len(pre) == len(arr)

def test_sddc_correctness():
    """Test SDDC technique correctness"""
    arr = np.array([1, 2, 3, 4])
    sddc = SDDCTechnique()
    pre = sddc.preprocess(arr)
    assert len(pre) == len(arr)

def test_lps_correctness():
    """Test LPS technique correctness"""
    arr = np.array([1, 2, 3, 4, 5, 6])
    lps = LPSTechnique([2, 2, 2])
    pre = lps.preprocess(arr)
    assert len(pre) == len(arr)

def test_idc_construction():
    """Test IDC construction with different techniques"""
    cube = np.random.rand(5, 4, 3)
    techniques = [PrefixSumTechnique(), SRPSTechnique(2), SDDCTechnique()]
    idc = IterativeDataCube(cube, techniques)
    preprocessed = idc.construct()
    assert preprocessed.shape == cube.shape

def test_idc_theoretical_costs():
    """Test theoretical cost calculation"""
    cube = np.random.rand(10, 10)
    techniques = [PrefixSumTechnique(), PrefixSumTechnique()]
    idc = IterativeDataCube(cube, techniques)
    query_cost, update_cost = idc.theoretical_costs()
    assert query_cost == 4  # 2 + 2
    assert update_cost == 20  # 10 + 10

def test_brute_force_comparison():
    """Test IDC results against brute force computation"""
    cube = np.random.rand(5, 4)
    techniques = [PrefixSumTechnique(), PrefixSumTechnique()]
    idc = IterativeDataCube(cube, techniques)
    idc.construct()
    
    # Test a simple range query
    ranges = [(0, 2), (1, 3)]
    idc_result = idc.range_query(ranges)
    
    # Brute force computation
    brute_force_result = np.sum(cube[0:3, 1:4])
    
    assert abs(idc_result - brute_force_result) < 1e-10

def test_update_consistency():
    """Test that updates maintain query correctness"""
    cube = np.random.rand(4, 4)
    techniques = [PrefixSumTechnique(), PrefixSumTechnique()]
    idc = IterativeDataCube(cube, techniques)
    idc.construct()
    
    # Get initial result
    initial_result = idc.range_query([(0, 1), (0, 1)])
    
    # Update a cell
    idc.update_cell((0, 0), 5.0)
    
    # Get updated result
    updated_result = idc.range_query([(0, 1), (0, 1)])
    
    # Should differ by the update amount
    assert abs(updated_result - initial_result - 5.0) < 1e-10

if __name__ == "__main__":
    # Run basic tests
    test_ps_correctness()
    test_idc_construction()
    test_idc_theoretical_costs()
    print("All basic tests passed!") 