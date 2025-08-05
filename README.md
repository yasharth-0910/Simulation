# Iterative Data Cubes (IDC) Simulation

A comprehensive simulation of the Iterative Data Cubes technique from the 2001 ICDT paper "Flexible Data Cubes for Online Aggregation" by Riedewald, Agrawal, and El Abbadi.

## Project Overview

This project implements a modular Python framework for simulating and analyzing IDC techniques, validating theoretical claims, and demonstrating practical benefits for online aggregation in data warehouses.

## Features

- **Four Core 1D Techniques**: Prefix Sum (PS), Space-Efficient Relative Prefix Sum (SRPS), Space-Efficient Dynamic Data Cube (SDDC), and Local Prefix Sum (LPS)
- **Modular Framework**: Easy to extend with new 1D techniques
- **Comprehensive Testing**: Correctness validation against brute-force computation
- **Performance Benchmarking**: Actual vs theoretical cost analysis
- **Interactive Dashboard**: Streamlit-based visualization and simulation
- **Real-world Examples**: Sales data simulation with realistic patterns

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd new
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python tests/test_idc.py
   ```

## Quick Start

### Basic Usage

```python
import numpy as np
from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique

# Create a 3D cube
cube = np.random.rand(10, 15, 20)

# Choose techniques for each dimension
techniques = [
    PrefixSumTechnique(),  # Dimension 1
    SRPSTechnique(block_size=3),  # Dimension 2
    PrefixSumTechnique()   # Dimension 3
]

# Create and construct IDC
idc = IterativeDataCube(cube, techniques)
idc.construct()

# Perform range query
result = idc.range_query([(0, 5), (2, 8), (1, 10)])
print(f"Query result: {result}")

# Update a cell
idc.update_cell((0, 0, 0), 5.0)
```

### Running Tests

```bash
# Run basic tests
python tests/test_idc.py

# Run with pytest (if installed)
pytest tests/
```

### Running Benchmarks

```bash
# Run performance benchmarks
python benchmarks/benchmark_idc.py
```

### Interactive Dashboard

```bash
# Start the Streamlit dashboard
streamlit run dashboard/dashboard.py
```

### Sales Simulation Example

```bash
# Run the sales data simulation
python examples/sales_simulation.py
```

## Project Structure

```
new/
├── idc_framework.py          # Core IDC implementation
├── techniques/               # 1D technique implementations
│   ├── base.py              # Abstract base class
│   ├── prefix_sum.py        # Prefix Sum technique
│   ├── srps.py              # SRPS technique
│   ├── sddc.py              # SDDC technique
│   ├── lps.py               # LPS technique
│   └── no_preprocessing.py  # No preprocessing baseline
├── tests/                   # Test suite
│   └── test_idc.py
├── benchmarks/              # Performance benchmarks
│   └── benchmark_idc.py
├── dashboard/               # Interactive dashboard
│   └── dashboard.py
├── examples/                # Example applications
│   └── sales_simulation.py
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Core Components

### 1. IterativeDataCube Class

The main class that implements the IDC framework:

- `construct()`: Applies 1D techniques iteratively along dimensions
- `range_query(ranges)`: Processes range queries using Equation 12
- `update_cell(indices, delta)`: Updates cells and propagates changes
- `theoretical_costs()`: Calculates theoretical query and update costs

### 2. 1D Techniques

Each technique implements the `OneDimensionalTechnique` interface:

- **PrefixSumTechnique**: Fast queries (cost=2), expensive updates (cost=n)
- **SRPSTechnique**: Balanced approach with block-based optimization
- **SDDCTechnique**: Logarithmic costs for both queries and updates
- **LPSTechnique**: Custom block partitioning for specific workloads

### 3. Testing Framework

Comprehensive tests for:
- Correctness validation against brute-force computation
- Update consistency verification
- Coefficient property validation
- Performance benchmarking

## Performance Analysis

The framework provides tools to analyze:

- **Query vs Update Cost Trade-offs**: Pareto frontier analysis
- **Scaling Behavior**: Performance vs cube size and dimensionality
- **Technique Comparison**: Relative performance of different approaches
- **Real-world Workloads**: Sales data simulation with realistic patterns

## Research Validation

The implementation validates key claims from the original paper:

1. **Correctness**: IDC results match brute-force computation
2. **Generalization**: PS, SRPS, SDDC are special cases of IDC
3. **Cost Trade-offs**: Theoretical predictions match actual measurements
4. **Scalability**: Performance follows predicted patterns

## Extending the Framework

### Adding New 1D Techniques

1. Create a new class inheriting from `OneDimensionalTechnique`
2. Implement the required abstract methods:
   - `preprocess(array)`: Transform 1D array
   - `get_alpha_coefficients(cell_index)`: Update propagation coefficients
   - `get_beta_coefficients(start, end)`: Range query coefficients
   - `theoretical_costs(array_size)`: Cost predictions

Example:
```python
class MyTechnique(OneDimensionalTechnique):
    def preprocess(self, array):
        # Your preprocessing logic
        return processed_array
    
    def get_alpha_coefficients(self, cell_index):
        # Your update coefficients
        return coefficients
    
    def get_beta_coefficients(self, start, end):
        # Your query coefficients
        return coefficients
    
    def theoretical_costs(self, array_size):
        return (query_cost, update_cost)
```

### Adding New Analysis Tools

The modular structure makes it easy to add:
- New benchmark scenarios
- Additional visualization tools
- Custom workload generators
- Alternative cost models

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for research and educational purposes.

## References

- Riedewald, M., Agrawal, D., & El Abbadi, A. (2001). Flexible Data Cubes for Online Aggregation. *ICDT 2001*.

## Contact

For questions or contributions, please open an issue on the repository. 