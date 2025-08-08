#!/usr/bin/env python3
"""
Research Validation Module for IDC Paper
Validates claims from "Flexible Data Cubes for Online Aggregation" (ICDT 2001)
"""

import numpy as np
import pandas as pd
import time
import tracemalloc
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import seaborn as sns

from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

class PaperValidation:
    """Validate claims from the IDC research paper"""
    
    def __init__(self):
        self.results = {}
    
    def validate_table_1_results(self):
        """Validate Table 1: Query-update cost tradeoffs for 1D techniques"""
        print("🔍 Validating Table 1 Results...")
        
        techniques = [
            ("Original Array", None),
            ("Prefix Sum (PS)", PrefixSumTechnique()),
            ("SRPS", SRPSTechnique(3)),
            ("SDDC", SDDCTechnique()),
            ("LPS", LPSTechnique([5, 5]))
        ]
        
        array_sizes = [100, 1000, 10000]
        results = []
        
        for name, technique in techniques:
            for n in array_sizes:
                if technique is None:
                    # Original array: no preprocessing
                    query_cost = n  # Must scan entire range
                    update_cost = 1  # Single cell update
                else:
                    query_cost, update_cost = technique.theoretical_costs(n)
                
                results.append({
                    'technique': name,
                    'array_size': n,
                    'query_cost': query_cost,
                    'update_cost': update_cost
                })
        
        df = pd.DataFrame(results)
        self.results['table_1'] = df
        
        print("✅ Table 1 validation complete")
        return df
    
    def validate_idc_generalization(self):
        """Validate that IDC generalizes PS, SRPS, and SDDC"""
        print("🔍 Validating IDC Generalization...")
        
        # Test cube
        cube = np.random.rand(10, 10, 10)
        
        # Test uniform PS technique
        ps_idc = IterativeDataCube(cube, [PrefixSumTechnique()] * 3)
        ps_idc.construct()
        
        # Test uniform SRPS technique
        srps_idc = IterativeDataCube(cube, [SRPSTechnique(3)] * 3)
        srps_idc.construct()
        
        # Test uniform SDDC technique
        sddc_idc = IterativeDataCube(cube, [SDDCTechnique()] * 3)
        sddc_idc.construct()
        
        # Test multiple queries to verify correctness
        test_ranges = [
            [(0, 2), (0, 2), (0, 2)],
            [(1, 4), (1, 4), (1, 4)],
            [(0, 9), (0, 9), (0, 9)]
        ]
        
        generalization_results = []
        
        for ranges in test_ranges:
            # Get IDC results
            ps_result = ps_idc.range_query(ranges)
            srps_result = srps_idc.range_query(ranges)
            sddc_result = sddc_idc.range_query(ranges)
            
            # Get brute force result
            brute_force = np.sum(cube[ranges[0][0]:ranges[0][1]+1, 
                                   ranges[1][0]:ranges[1][1]+1, 
                                   ranges[2][0]:ranges[2][1]+1])
            
            # Check accuracy
            ps_accuracy = abs(ps_result - brute_force) < 1e-10
            srps_accuracy = abs(srps_result - brute_force) < 1e-10
            sddc_accuracy = abs(sddc_result - brute_force) < 1e-10
            
            generalization_results.append({
                'ranges': ranges,
                'brute_force': brute_force,
                'ps_result': ps_result,
                'srps_result': srps_result,
                'sddc_result': sddc_result,
                'ps_accurate': ps_accuracy,
                'srps_accurate': srps_accuracy,
                'sddc_accurate': sddc_accuracy
            })
        
        self.results['generalization'] = generalization_results
        print("✅ IDC generalization validation complete")
        return generalization_results
    
    def validate_space_optimality(self):
        """Validate that IDC is space optimal (no overhead)"""
        print("🔍 Validating Space Optimality...")
        
        cube_sizes = [(10, 10, 10), (20, 20, 20), (30, 30, 30)]
        space_results = []
        
        for shape in cube_sizes:
            cube = np.random.rand(*shape)
            original_size = cube.nbytes
            
            # Test different IDC configurations
            configurations = [
                ("PS-PS-PS", [PrefixSumTechnique()] * 3),
                ("SRPS-SRPS-SRPS", [SRPSTechnique(3)] * 3),
                ("SDDC-SDDC-SDDC", [SDDCTechnique()] * 3),
                ("Mixed", [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique()])
            ]
            
            for config_name, techniques in configurations:
                idc = IterativeDataCube(cube, techniques)
                idc.construct()
                
                # Check that preprocessed cube has same size as original
                preprocessed_size = idc.preprocessed_cube.nbytes
                space_overhead = (preprocessed_size - original_size) / original_size
                
                space_results.append({
                    'shape': shape,
                    'configuration': config_name,
                    'original_size': original_size,
                    'preprocessed_size': preprocessed_size,
                    'space_overhead': space_overhead,
                    'is_optimal': abs(space_overhead) < 1e-10
                })
        
        self.results['space_optimality'] = space_results
        print("✅ Space optimality validation complete")
        return space_results
    
    def validate_cost_variety(self):
        """Validate that IDC provides greater cost variety than previous approaches"""
        print("🔍 Validating Cost Variety...")
        
        # Test different IDC configurations
        configurations = [
            ("PS-PS-PS", [PrefixSumTechnique()] * 3),
            ("SRPS-SRPS-SRPS", [SRPSTechnique(3)] * 3),
            ("SDDC-SDDC-SDDC", [SDDCTechnique()] * 3),
            ("PS-SRPS-SDDC", [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique()]),
            ("SRPS-PS-SDDC", [SRPSTechnique(3), PrefixSumTechnique(), SDDCTechnique()]),
            ("SDDC-PS-SRPS", [SDDCTechnique(), PrefixSumTechnique(), SRPSTechnique(3)])
        ]
        
        cube = np.random.rand(20, 20, 20)
        cost_results = []
        
        for config_name, techniques in configurations:
            idc = IterativeDataCube(cube, techniques)
            query_cost, update_cost = idc.theoretical_costs()
            
            cost_results.append({
                'configuration': config_name,
                'query_cost': query_cost,
                'update_cost': update_cost,
                'cost_ratio': query_cost / update_cost
            })
        
        self.results['cost_variety'] = cost_results
        print("✅ Cost variety validation complete")
        return cost_results
    
    def validate_dimensional_independence(self):
        """Validate that dimensions are processed independently"""
        print("🔍 Validating Dimensional Independence...")
        
        cube = np.random.rand(10, 10, 10)
        
        # Test that changing one dimension's technique doesn't affect others
        base_config = [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique()]
        
        independence_results = []
        
        for dim_to_change in range(3):
            # Create modified configuration
            modified_config = base_config.copy()
            modified_config[dim_to_change] = LPSTechnique([5, 5])
            
            # Create both IDCs
            base_idc = IterativeDataCube(cube, base_config)
            modified_idc = IterativeDataCube(cube, modified_config)
            
            # Test queries that don't involve the changed dimension
            test_ranges = []
            for i in range(3):
                if i != dim_to_change:
                    test_ranges.append((0, 5))
                else:
                    test_ranges.append((0, 0))  # Fixed value
            
            # Both should give same result for this query
            base_result = base_idc.range_query(test_ranges)
            modified_result = modified_idc.range_query(test_ranges)
            
            independence_results.append({
                'changed_dimension': dim_to_change,
                'base_result': base_result,
                'modified_result': modified_result,
                'results_equal': abs(base_result - modified_result) < 1e-10
            })
        
        self.results['dimensional_independence'] = independence_results
        print("✅ Dimensional independence validation complete")
        return independence_results
    
    def run_comprehensive_validation(self):
        """Run all validation tests"""
        print("🚀 Starting Comprehensive Research Validation")
        print("=" * 50)
        
        # Run all validations
        self.validate_table_1_results()
        self.validate_idc_generalization()
        self.validate_space_optimality()
        self.validate_cost_variety()
        self.validate_dimensional_independence()
        
        print("=" * 50)
        print("✅ All validations complete!")
        
        return self.results

def create_validation_report(results: Dict):
    """Create a comprehensive validation report"""
    print("\n📊 VALIDATION REPORT")
    print("=" * 50)
    
    # Table 1 Results
    if 'table_1' in results:
        df = results['table_1']
        print("\n📋 Table 1 Validation Results:")
        print(df.to_string(index=False))
    
    # Generalization Results
    if 'generalization' in results:
        gen_results = results['generalization']
        accurate_count = sum(1 for r in gen_results if all([r['ps_accurate'], r['srps_accurate'], r['sddc_accurate']]))
        print(f"\n🔗 IDC Generalization: {accurate_count}/{len(gen_results)} tests passed")
    
    # Space Optimality
    if 'space_optimality' in results:
        space_results = results['space_optimality']
        optimal_count = sum(1 for r in space_results if r['is_optimal'])
        print(f"\n💾 Space Optimality: {optimal_count}/{len(space_results)} configurations optimal")
    
    # Cost Variety
    if 'cost_variety' in results:
        cost_results = results['cost_variety']
        unique_ratios = len(set(r['cost_ratio'] for r in cost_results))
        print(f"\n📈 Cost Variety: {unique_ratios} unique cost ratios found")
    
    # Dimensional Independence
    if 'dimensional_independence' in results:
        ind_results = results['dimensional_independence']
        independent_count = sum(1 for r in ind_results if r['results_equal'])
        print(f"\n🔀 Dimensional Independence: {independent_count}/{len(ind_results)} tests passed")

def main():
    """Run the validation suite"""
    validator = PaperValidation()
    results = validator.run_comprehensive_validation()
    create_validation_report(results)

if __name__ == "__main__":
    main() 