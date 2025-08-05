# IDC Simulation Dashboard User Guide

## 🎯 Overview

The IDC (Iterative Data Cubes) Simulation Dashboard is an interactive tool for exploring and understanding the techniques from the 2001 ICDT paper "Flexible Data Cubes for Online Aggregation". This guide explains every feature and concept in the dashboard.

## 📊 Dashboard Sections

### 1. Documentation & Concepts

The dashboard starts with comprehensive documentation organized in tabs:

#### 🎯 Core Concepts Tab
- **What is IDC?**: Explains that IDC is a technique for efficient online aggregation in data warehouses
- **Key Components**: Data cubes, 1D techniques, range queries, updates
- **Mathematical Foundation**: References to equations from the original paper

#### 📊 Cube Configuration Tab
- **Dimension Sizes**: Explains what each dimension represents
- **Real-world Examples**: How dimensions map to business concepts
- **Cube Structure**: How data is organized in multidimensional arrays

#### 🔧 Techniques Tab
- **Prefix Sum (PS)**: Fast queries, slow updates
- **SRPS**: Balanced approach with block-based optimization
- **SDDC**: Logarithmic costs for both queries and updates
- **LPS**: Custom block partitioning for specific workloads

#### 📈 Performance Tab
- **Cost Trade-offs**: Query vs update cost relationships
- **Scaling Behavior**: How performance changes with cube size
- **Technique Selection Guide**: When to use each technique

#### 🎮 Interactive Features Tab
- **Live Simulation**: How to use the interactive query and update features
- **3D Visualization**: Understanding the 3D plots
- **Performance Benchmarks**: How to interpret benchmark results

### 2. Cube Configuration (Sidebar)

#### Dimension Sizes
- **Dimension 1 Size (5-50)**: Controls the size of the first dimension
  - Example: 10 regions, 20 time periods, 100 products
  - Larger sizes = more data but slower processing
  - Recommended: Start with 10-20 for testing

- **Dimension 2 Size (5-50)**: Controls the size of the second dimension
  - Each dimension can represent different business concepts
  - Total cells = Dim1 × Dim2 × Dim3

- **Dimension 3 Size (5-50)**: Controls the size of the third dimension
  - A 10×15×20 cube has 3,000 total cells
  - Each cell contains a value (e.g., sales amount)

#### Technique Selection
- **Technique for Dimension 1**: Choose how to optimize the first dimension
  - **Prefix Sum (PS)**: Best for read-heavy workloads
  - **SRPS**: Balanced approach, good for most cases
  - **SDDC**: Best for hierarchical data
  - **LPS**: Custom optimization for specific patterns

- **Technique for Dimension 2**: Choose optimization for second dimension
  - Different dimensions may have different access patterns
  - Example: Time dimension might use SRPS for monthly blocks

- **Technique for Dimension 3**: Choose optimization for third dimension
  - Product dimension might use SDDC for hierarchical categories

### 3. Cost Trade-offs Section

#### Generate Pareto Frontier Button
- **What it does**: Creates a scatter plot showing query cost vs update cost
- **X-axis**: Query Cost (lower is better)
- **Y-axis**: Update Cost (lower is better)
- **Each point**: Represents a different technique combination
- **Interpretation**: Points closer to origin (0,0) are better

#### Understanding the Plot
- **Bottom-left**: Best overall performance
- **Top-right**: Worst overall performance
- **Trade-off**: Faster queries usually mean slower updates
- **Color coding**: Different colors represent different techniques

### 4. Performance Benchmarks Section

#### Run Performance Tests Button
- **What it does**: Measures actual performance of your configuration
- **Construction Time**: How long to build the preprocessed cube
- **Query Time**: How long to answer a range query
- **Query Result**: The actual sum from the range query
- **Theoretical Costs**: Predicted performance based on theory

#### Understanding Results
- **Construction Time**: One-time cost to set up the cube
- **Query Time**: Time for each range query (should be fast)
- **Theoretical vs Actual**: Compare predicted vs measured performance
- **Memory Usage**: Additional memory required (not shown but important)

### 5. 3D Visualization Section

#### 3D Data Cube Visualization
- **What it shows**: Interactive 3D scatter plot of your data cube
- **X-axis**: Dimension 1
- **Y-axis**: Dimension 2
- **Z-axis**: Dimension 3
- **Color**: Value at each position (darker = higher value)
- **Interaction**: Rotate, zoom, hover for details

#### Query Range Highlight
- **What it shows**: Which cells are included in your query range
- **Red points**: Cells inside the query range
- **Gray points**: Cells outside the query range
- **Sliders**: Control the start and end of each dimension
- **Purpose**: Visualize exactly what data your query is summing

#### Technique Comparison
- **What it shows**: Bar chart comparing different techniques
- **Y-axis**: Query result (should be the same for all techniques)
- **Bars**: Different colors for different techniques
- **Purpose**: Verify all techniques give correct results

#### 3D Cost Trade-off Analysis
- **What it shows**: 3D scatter plot of performance trade-offs
- **X-axis**: Query Cost
- **Y-axis**: Update Cost
- **Z-axis**: Cube Size
- **Color**: Different techniques
- **Purpose**: See how performance scales with cube size

### 6. Live Simulation Section

#### Try Different Range Queries
- **Dim 1 Start/End**: Select range in first dimension (0 to 4)
- **Dim 2 Start/End**: Select range in second dimension (0 to 4)
- **Dim 3 Start/End**: Select range in third dimension (0 to 4)
- **Execute Query Button**: Run the range query
- **Query Result**: Sum of all cells in the selected range
- **Brute Force Result**: Verification using direct computation
- **Difference**: Should be very small (verifies correctness)

#### Update Simulation
- **Update i/j/k**: Select which cell to modify (0 to 4 for each dimension)
- **Delta**: How much to add/subtract from the cell
- **Apply Update Button**: Modify the cell and see the effect
- **Updated Query Result**: How the change affects query results

## 🔍 Understanding the Concepts

### What is a Data Cube?
A data cube is a multidimensional array where each cell contains a value. Think of it like a 3D spreadsheet:
- **Example**: Sales data with dimensions: Region × Time × Product
- **Cell value**: Sales amount for that specific combination
- **Query**: Sum all sales in a rectangular region

### What are Range Queries?
A range query asks: "What is the sum of all values in this rectangular region?"
- **Example**: "Total sales for regions 0-2, time periods 1-5, products 0-3"
- **Result**: Sum of all cells in that rectangular box
- **Challenge**: Computing this efficiently for large cubes

### What are Updates?
An update modifies a single cell and must propagate the change:
- **Example**: "Add $100 to sales for region 1, day 5, product 2"
- **Challenge**: Updating the preprocessed data efficiently
- **Trade-off**: Faster queries usually mean slower updates

### What are 1D Techniques?
Each dimension can be optimized differently:
- **Prefix Sum**: Pre-computes cumulative sums (fast queries, slow updates)
- **SRPS**: Uses blocks with anchors (balanced performance)
- **SDDC**: Uses binary trees (logarithmic costs)
- **LPS**: Custom partitioning (flexible but complex)

## 🎯 Best Practices

### Choosing Dimension Sizes
- **Start small**: Use 5-10 for testing
- **Scale up**: Increase to 20-50 for realistic scenarios
- **Consider memory**: Larger cubes use more memory
- **Balance**: Too small = not realistic, too large = slow

### Choosing Techniques
- **Read-heavy**: Use Prefix Sum or SDDC
- **Update-heavy**: Use SRPS or LPS
- **Balanced**: Use SRPS or SDDC
- **Custom patterns**: Use LPS with specific configuration

### Interpreting Results
- **Correctness**: IDC results should match brute force (small difference)
- **Performance**: Construction time should scale reasonably
- **Trade-offs**: Look for Pareto optimal configurations
- **Scaling**: Performance should follow theoretical predictions

## 🚨 Troubleshooting

### Common Issues
1. **Slow performance**: Reduce dimension sizes
2. **Memory errors**: Use smaller cubes
3. **Incorrect results**: Check that techniques are implemented correctly
4. **Import errors**: Make sure all dependencies are installed

### Performance Tips
1. **Start with small cubes**: 5×5×5 or 10×10×10
2. **Use balanced techniques**: SRPS or SDDC for most cases
3. **Monitor memory**: Large cubes can use significant memory
4. **Test correctness**: Always verify against brute force

## 📚 Further Reading

- **Original Paper**: Riedewald, M., Agrawal, D., & El Abbadi, A. (2001). Flexible Data Cubes for Online Aggregation. *ICDT 2001*.
- **Online Aggregation**: Techniques for approximate query processing
- **Data Warehousing**: Multidimensional data storage and analysis
- **Performance Analysis**: Cost models and trade-off analysis

This dashboard provides a comprehensive environment for understanding and experimenting with IDC techniques. Use it to explore different configurations, understand performance trade-offs, and validate theoretical claims from the original research. 