#!/usr/bin/env python3
"""
IDC Simulation Demo
A simple demonstration of the Iterative Data Cubes framework
"""

import numpy as np
import time
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

def main():
    print("=" * 60)
    print("Iterative Data Cubes (IDC) Simulation Demo")
    print("=" * 60)
    
    # Create a test cube
    print("\n1. Creating test data cube...")
    cube = np.random.rand(8, 10, 6)
    print(f"   Cube shape: {cube.shape}")
    print(f"   Total elements: {cube.size}")
    print(f"   Sum of all elements: {np.sum(cube):.4f}")
    
    # Test different technique combinations
    print("\n2. Testing different technique combinations...")
    
    configurations = [
        {
            'name': 'All Prefix Sum',
            'techniques': [PrefixSumTechnique(), PrefixSumTechnique(), PrefixSumTechnique()]
        },
        {
            'name': 'Mixed Techniques',
            'techniques': [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique()]
        },
        {
            'name': 'All SRPS',
            'techniques': [SRPSTechnique(2), SRPSTechnique(3), SRPSTechnique(2)]
        }
    ]
    
    for config in configurations:
        print(f"\n   Testing: {config['name']}")
        
        # Create IDC
        idc = IterativeDataCube(cube, config['techniques'])
        
        # Measure construction time
        start_time = time.time()
        idc.construct()
        construction_time = time.time() - start_time
        
        # Get theoretical costs
        query_cost, update_cost = idc.theoretical_costs()
        
        print(f"     Construction time: {construction_time:.4f}s")
        print(f"     Theoretical query cost: {query_cost}")
        print(f"     Theoretical update cost: {update_cost}")
        
        # Test a simple query
        ranges = [(0, 3), (1, 5), (0, 2)]
        start_time = time.time()
        result = idc.range_query(ranges)
        query_time = time.time() - start_time
        
        # Brute force comparison
        brute_force = np.sum(cube[0:4, 1:6, 0:3])
        
        print(f"     Query time: {query_time:.6f}s")
        print(f"     Query result: {result:.4f}")
        print(f"     Brute force: {brute_force:.4f}")
        print(f"     Difference: {abs(result - brute_force):.10f}")
        
        # Test update
        old_result = idc.range_query([(0, 1), (0, 1), (0, 1)])
        idc.update_cell((0, 0, 0), 5.0)
        new_result = idc.range_query([(0, 1), (0, 1), (0, 1)])
        print(f"     Update effect: {new_result - old_result:.4f}")
    
    # Performance comparison
    print("\n3. Performance comparison...")
    
    # Create larger cube for scaling test
    large_cube = np.random.rand(20, 20, 20)
    print(f"   Large cube shape: {large_cube.shape}")
    
    techniques_list = [
        ("Prefix Sum", [PrefixSumTechnique(), PrefixSumTechnique(), PrefixSumTechnique()]),
        ("SRPS", [SRPSTechnique(5), SRPSTechnique(5), SRPSTechnique(5)]),
        ("SDDC", [SDDCTechnique(), SDDCTechnique(), SDDCTechnique()]),
        ("LPS", [LPSTechnique([10, 10]), LPSTechnique([10, 10]), LPSTechnique([10, 10])])
    ]
    
    results = []
    for name, techniques in techniques_list:
        print(f"\n   Testing {name}...")
        
        idc = IterativeDataCube(large_cube, techniques)
        
        # Construction time
        start_time = time.time()
        idc.construct()
        construction_time = time.time() - start_time
        
        # Query time
        ranges = [(0, 9), (0, 9), (0, 9)]
        start_time = time.time()
        result = idc.range_query(ranges)
        query_time = time.time() - start_time
        
        # Theoretical costs
        query_cost, update_cost = idc.theoretical_costs()
        
        results.append({
            'technique': name,
            'construction_time': construction_time,
            'query_time': query_time,
            'query_cost': query_cost,
            'update_cost': update_cost
        })
        
        print(f"     Construction: {construction_time:.4f}s")
        print(f"     Query: {query_time:.6f}s")
        print(f"     Query cost: {query_cost}, Update cost: {update_cost}")
    
    # Summary
    print("\n4. Summary...")
    print("   Technique comparison:")
    for result in results:
        print(f"     {result['technique']:12} | "
              f"Construction: {result['construction_time']:6.4f}s | "
              f"Query: {result['query_time']:8.6f}s | "
              f"Costs: ({result['query_cost']:2d}, {result['update_cost']:2d})")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'python tests/test_idc.py' for comprehensive testing")
    print("2. Run 'python benchmarks/benchmark_idc.py' for detailed benchmarks")
    print("3. Run 'streamlit run dashboard/dashboard.py' for interactive dashboard")
    print("4. Run 'python examples/sales_simulation.py' for real-world example")

if __name__ == "__main__":
    main() 