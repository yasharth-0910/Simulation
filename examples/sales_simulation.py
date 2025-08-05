import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

class SalesDataSimulator:
    def __init__(self):
        self.regions = 10
        self.time_periods = 365
        self.products = 100
        self.customer_types = 3
        
    def generate_realistic_sales_cube(self, 
                                     regions: int = 10,
                                     time_periods: int = 365, 
                                     products: int = 100,
                                     customer_types: int = 3) -> np.ndarray:
        """Generate realistic sales data with:
        - Seasonal patterns in time dimension
        - Regional preferences for products  
        - Customer type behaviors
        """
        cube = np.zeros((regions, time_periods, products, customer_types))
        
        # Add realistic patterns
        
        # 1. Seasonal sales patterns (holidays, summer/winter)
        seasonal_pattern = self._generate_seasonal_pattern(time_periods)
        
        # 2. Regional product preferences
        regional_preferences = self._generate_regional_preferences(regions, products)
        
        # 3. Customer type spending patterns
        customer_patterns = self._generate_customer_patterns(customer_types)
        
        # 4. Base sales volume
        base_sales = np.random.exponential(100, (regions, products, customer_types))
        
        # Combine all patterns
        for r in range(regions):
            for t in range(time_periods):
                for p in range(products):
                    for c in range(customer_types):
                        seasonal_factor = seasonal_pattern[t]
                        regional_factor = regional_preferences[r, p]
                        customer_factor = customer_patterns[c]
                        
                        # Combine factors with some randomness
                        sales = (base_sales[r, p, c] * 
                                seasonal_factor * 
                                regional_factor * 
                                customer_factor * 
                                (0.8 + 0.4 * np.random.random()))
                        
                        cube[r, t, p, c] = max(0, sales)
        
        return cube
    
    def _generate_seasonal_pattern(self, time_periods: int) -> np.ndarray:
        """Generate seasonal sales pattern"""
        pattern = np.ones(time_periods)
        
        # Holiday peaks (Christmas, Black Friday, etc.)
        holidays = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
        for holiday in holidays:
            if holiday < time_periods:
                pattern[holiday] = 2.5  # 150% increase during holidays
        
        # Summer dip
        summer_start = 150
        summer_end = 240
        for t in range(summer_start, min(summer_end, time_periods)):
            pattern[t] *= 0.7  # 30% decrease in summer
        
        # Add some weekly patterns
        for t in range(time_periods):
            day_of_week = t % 7
            if day_of_week in [5, 6]:  # Weekend
                pattern[t] *= 1.2  # 20% increase on weekends
        
        return pattern
    
    def _generate_regional_preferences(self, regions: int, products: int) -> np.ndarray:
        """Generate regional preferences for products"""
        preferences = np.ones((regions, products))
        
        # Create some regional clusters
        for r in range(regions):
            # Each region has preferences for certain product categories
            preferred_categories = np.random.choice(products, size=products//4, replace=False)
            for p in preferred_categories:
                preferences[r, p] = 1.5 + 0.5 * np.random.random()  # 50-100% increase
        
        return preferences
    
    def _generate_customer_patterns(self, customer_types: int) -> np.ndarray:
        """Generate customer type spending patterns"""
        patterns = np.ones(customer_types)
        
        # Customer type 0: Budget-conscious (lower spending)
        patterns[0] = 0.6
        
        # Customer type 1: Regular customers (normal spending)
        patterns[1] = 1.0
        
        # Customer type 2: Premium customers (higher spending)
        patterns[2] = 1.8
        
        return patterns
    
    def generate_analyst_queries(self, cube_shape: Tuple[int, ...], num_queries: int = 1000):
        """Generate realistic OLAP queries:
        - Hierarchical drill-downs (year -> quarter -> month)
        - Regional comparisons  
        - Product category analysis
        - Customer segment analysis
        """
        queries = []
        query_types = ['hierarchical', 'comparison', 'drill_down', 'slice_dice']
        
        for _ in range(num_queries):
            query_type = np.random.choice(query_types, p=[0.4, 0.3, 0.2, 0.1])
            query = self.generate_query_by_type(query_type, cube_shape)
            queries.append(query)
        
        return queries
    
    def generate_query_by_type(self, query_type: str, cube_shape: Tuple[int, ...]) -> Dict:
        """Generate query based on type"""
        if query_type == 'hierarchical':
            # Drill-down queries
            ranges = []
            for dim_size in cube_shape:
                start = 0
                end = np.random.randint(dim_size//4, dim_size//2)
                ranges.append((start, end))
            return {'type': 'hierarchical', 'ranges': ranges}
        
        elif query_type == 'comparison':
            # Regional or temporal comparisons
            ranges = []
            for i, dim_size in enumerate(cube_shape):
                if i == 0:  # Region dimension
                    # Compare two regions
                    region1 = np.random.randint(0, dim_size//2)
                    region2 = np.random.randint(dim_size//2, dim_size)
                    ranges.append((region1, region2))
                else:
                    start = np.random.randint(0, dim_size//2)
                    end = np.random.randint(start, dim_size)
                    ranges.append((start, end))
            return {'type': 'comparison', 'ranges': ranges}
        
        elif query_type == 'drill_down':
            # Specific drill-down
            ranges = []
            for dim_size in cube_shape:
                start = np.random.randint(0, dim_size//3)
                end = np.random.randint(start + dim_size//6, start + dim_size//3)
                ranges.append((start, end))
            return {'type': 'drill_down', 'ranges': ranges}
        
        else:  # slice_dice
            # Random slice and dice
            ranges = []
            for dim_size in cube_shape:
                start = np.random.randint(0, dim_size)
                end = np.random.randint(start, min(start + dim_size//4, dim_size))
                ranges.append((start, end))
            return {'type': 'slice_dice', 'ranges': ranges}
    
    def simulate_update_patterns(self, cube_shape: Tuple[int, ...]) -> List[Dict]:
        """Simulate realistic update patterns:
        - Batch updates (daily sales reports)
        - Streaming updates (real-time transactions)
        - Corrections (adjustments to historical data)
        """
        updates = []
        
        # Batch updates (daily sales)
        for _ in range(50):
            indices = tuple(np.random.randint(0, size) for size in cube_shape)
            delta = np.random.exponential(50)  # Positive sales
            updates.append({
                'type': 'batch',
                'indices': indices,
                'delta': delta
            })
        
        # Streaming updates (real-time)
        for _ in range(20):
            indices = tuple(np.random.randint(0, size) for size in cube_shape)
            delta = np.random.normal(10, 5)  # Small real-time updates
            updates.append({
                'type': 'streaming',
                'indices': indices,
                'delta': delta
            })
        
        # Corrections
        for _ in range(10):
            indices = tuple(np.random.randint(0, size) for size in cube_shape)
            delta = np.random.normal(0, 20)  # Can be positive or negative
            updates.append({
                'type': 'correction',
                'indices': indices,
                'delta': delta
            })
        
        return updates

def main():
    print("Sales Data Simulation Demo")
    print("=" * 50)
    
    # Initialize simulator
    simulator = SalesDataSimulator()
    
    # Generate realistic sales cube
    print("Generating realistic sales data...")
    cube = simulator.generate_realistic_sales_cube()
    print(f"Sales cube shape: {cube.shape}")
    print(f"Total sales volume: {np.sum(cube):.2f}")
    
    # Create IDC with different techniques
    print("\nCreating IDC with different techniques...")
    techniques = [
        PrefixSumTechnique(),  # Region dimension
        SRPSTechnique(block_size=30),  # Time dimension (monthly blocks)
        SDDCTechnique(),  # Product dimension
        LPSTechnique([20, 20, 20, 20, 20])  # Customer dimension
    ]
    
    idc = IterativeDataCube(cube, techniques)
    
    # Construct the IDC
    print("Constructing IDC...")
    preprocessed = idc.construct()
    print("IDC construction completed!")
    
    # Generate test queries
    print("\nGenerating test queries...")
    queries = simulator.generate_analyst_queries(cube.shape, 10)
    
    # Test queries
    print("\nTesting queries:")
    for i, query in enumerate(queries[:5]):
        result = idc.range_query(query['ranges'])
        print(f"Query {i+1} ({query['type']}): {result:.2f}")
    
    # Test updates
    print("\nTesting updates:")
    updates = simulator.simulate_update_patterns(cube.shape)
    
    for i, update in enumerate(updates[:3]):
        old_result = idc.range_query([(0, 2), (0, 30), (0, 10), (0, 1)])
        idc.update_cell(update['indices'], update['delta'])
        new_result = idc.range_query([(0, 2), (0, 30), (0, 10), (0, 1)])
        print(f"Update {i+1} ({update['type']}): {new_result - old_result:.2f}")
    
    # Performance analysis
    print("\nPerformance Analysis:")
    query_cost, update_cost = idc.theoretical_costs()
    print(f"Theoretical query cost: {query_cost}")
    print(f"Theoretical update cost: {update_cost}")
    
    print("\nSales simulation completed!")

if __name__ == "__main__":
    main()
