# Benchmark suite for Iterative Data Cubes

import numpy as np
import time
import tracemalloc
import pandas as pd
from typing import List, Dict, Tuple
from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

class PerformanceBenchmark:
    def __init__(self):
        self.results = []

    def benchmark_query_costs(self, configurations: List[Dict], query_workloads: List) -> pd.DataFrame:
        """Measure actual vs theoretical query costs"""
        results = []
        
        for config in configurations:
            cube = np.random.rand(*config['cube_shape'])
            techniques = config['techniques']
            idc = IterativeDataCube(cube, techniques)
            
            for workload in query_workloads:
                # Measure actual performance
                start_time = time.time()
                memory_start = tracemalloc.get_traced_memory()[0]
                
                for query in workload:
                    result = idc.range_query(query['ranges'])
                
                elapsed_time = time.time() - start_time
                memory_used = tracemalloc.get_traced_memory()[0] - memory_start
                
                # Compare with theoretical predictions
                theoretical_cost = idc.theoretical_costs()[0]
                
                results.append({
                    'config': config,
                    'actual_time': elapsed_time,
                    'memory_used': memory_used, 
                    'theoretical_cost': theoretical_cost,
                    'queries_per_second': len(workload) / elapsed_time if elapsed_time > 0 else 0
                })
        
        return pd.DataFrame(results)

    def benchmark_update_costs(self, configurations: List[Dict], update_patterns: List) -> pd.DataFrame:
        """Measure actual vs theoretical update costs"""
        results = []
        
        for config in configurations:
            cube = np.random.rand(*config['cube_shape'])
            techniques = config['techniques']
            idc = IterativeDataCube(cube, techniques)
            idc.construct()
            
            for pattern in update_patterns:
                start_time = time.time()
                
                for update in pattern:
                    idc.update_cell(update['indices'], update['delta'])
                
                elapsed_time = time.time() - start_time
                
                theoretical_cost = idc.theoretical_costs()[1]
                
                results.append({
                    'config': config,
                    'actual_time': elapsed_time,
                    'updates_per_second': len(pattern) / elapsed_time if elapsed_time > 0 else 0,
                    'theoretical_cost': theoretical_cost
                })
        
        return pd.DataFrame(results)

    def scaling_analysis(self, dimension_sizes: List[int], techniques: List[str]) -> pd.DataFrame:
        """Analyze how performance scales with cube size and dimensionality"""
        results = []
        
        for size in dimension_sizes:
            for technique_name in techniques:
                # Create cube with given size
                cube = np.random.rand(size, size)
                
                # Create technique instances
                if technique_name == "PS":
                    techniques_list = [PrefixSumTechnique(), PrefixSumTechnique()]
                elif technique_name == "SRPS":
                    techniques_list = [SRPSTechnique(block_size=int(np.sqrt(size))), 
                                    SRPSTechnique(block_size=int(np.sqrt(size)))]
                elif technique_name == "SDDC":
                    techniques_list = [SDDCTechnique(), SDDCTechnique()]
                elif technique_name == "LPS":
                    techniques_list = [LPSTechnique([size//2, size//2]), 
                                    LPSTechnique([size//2, size//2])]
                
                idc = IterativeDataCube(cube, techniques_list)
                
                # Measure construction time
                start_time = time.time()
                idc.construct()
                construction_time = time.time() - start_time
                
                # Measure query time
                query_ranges = [(0, size//2), (0, size//2)]
                start_time = time.time()
                result = idc.range_query(query_ranges)
                query_time = time.time() - start_time
                
                # Get theoretical costs
                query_cost, update_cost = idc.theoretical_costs()
                
                results.append({
                    'size': size,
                    'technique': technique_name,
                    'construction_time': construction_time,
                    'query_time': query_time,
                    'theoretical_query_cost': query_cost,
                    'theoretical_update_cost': update_cost
                })
        
        return pd.DataFrame(results)

def generate_test_workloads(cube_shape: Tuple[int, ...], num_queries: int = 100) -> List:
    """Generate test query workloads"""
    workloads = []
    
    for _ in range(5):  # 5 different workloads
        workload = []
        for _ in range(num_queries):
            # Generate random range query
            ranges = []
            for dim_size in cube_shape:
                start = np.random.randint(0, dim_size)
                end = np.random.randint(start, dim_size)
                ranges.append((start, end))
            workload.append({'ranges': ranges})
        workloads.append(workload)
    
    return workloads

def generate_update_patterns(cube_shape: Tuple[int, ...], num_updates: int = 50) -> List:
    """Generate test update patterns"""
    patterns = []
    
    for _ in range(3):  # 3 different patterns
        pattern = []
        for _ in range(num_updates):
            # Generate random update
            indices = tuple(np.random.randint(0, size) for size in cube_shape)
            delta = np.random.randn() * 0.1
            pattern.append({'indices': indices, 'delta': delta})
        patterns.append(pattern)
    
    return patterns

def main():
    print("Starting IDC Benchmark Suite...")
    
    # Initialize benchmark
    benchmark = PerformanceBenchmark()
    
    # Test configurations
    configurations = [
        {
            'cube_shape': (10, 10),
            'techniques': [PrefixSumTechnique(), PrefixSumTechnique()],
            'name': 'PS_10x10'
        },
        {
            'cube_shape': (20, 20),
            'techniques': [SRPSTechnique(4), SRPSTechnique(4)],
            'name': 'SRPS_20x20'
        },
        {
            'cube_shape': (15, 15),
            'techniques': [SDDCTechnique(), SDDCTechnique()],
            'name': 'SDDC_15x15'
        }
    ]
    
    # Generate workloads
    cube_shape = (10, 10)
    query_workloads = generate_test_workloads(cube_shape, 50)
    update_patterns = generate_update_patterns(cube_shape, 20)
    
    # Run benchmarks
    print("Running query cost benchmarks...")
    query_results = benchmark.benchmark_query_costs(configurations, query_workloads)
    
    print("Running update cost benchmarks...")
    update_results = benchmark.benchmark_update_costs(configurations, update_patterns)
    
    print("Running scaling analysis...")
    scaling_results = benchmark.scaling_analysis([5, 10, 15, 20], ["PS", "SRPS", "SDDC", "LPS"])
    
    # Print results
    print("\n=== Query Performance Results ===")
    print(query_results.groupby('config')['queries_per_second'].mean())
    
    print("\n=== Update Performance Results ===")
    print(update_results.groupby('config')['updates_per_second'].mean())
    
    print("\n=== Scaling Analysis ===")
    print(scaling_results.groupby(['size', 'technique'])['query_time'].mean())
    
    print("\nBenchmark suite completed!")

if __name__ == "__main__":
    main()
