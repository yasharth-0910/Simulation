import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from typing import List, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

def create_documentation_section():
    """Create comprehensive documentation section"""
    st.subheader("📚 Documentation & Concepts")
    
    # Create tabs for different documentation sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Core Concepts", 
        "📊 Cube Configuration", 
        "🔧 Techniques", 
        "📈 Performance", 
        "🎮 Interactive Features"
    ])
    
    with tab1:
        st.markdown("""
        ### 🎯 Core Concepts
        
        **What is Iterative Data Cubes (IDC)?**
        
        IDC is a technique for efficient online aggregation in data warehouses. It allows you to:
        - Perform fast range queries on multidimensional data
        - Update individual cells efficiently
        - Balance query speed vs update speed based on your needs
        
        **Key Components:**
        
        1. **Data Cube**: A multidimensional array (e.g., 3D cube with regions × time × products)
        2. **1D Techniques**: Methods applied along each dimension (PS, SRPS, SDDC, LPS)
        3. **Range Queries**: Sum all values in a rectangular region
        4. **Updates**: Modify individual cells and propagate changes
        
        **Mathematical Foundation:**
        - Uses α coefficients for update propagation (Equation 1)
        - Uses β coefficients for range queries (Equation 7)
        - Combines techniques iteratively along dimensions (Equations 2-6)
        """)
    
    with tab2:
        st.markdown("""
        ### 📊 Cube Configuration
        
        **Dimension Sizes:**
        - **Dimension 1 Size**: Number of elements in the first dimension
          - Example: 10 regions, 20 time periods, 100 products
        - **Dimension 2 Size**: Number of elements in the second dimension
        - **Dimension 3 Size**: Number of elements in the third dimension
        
        **What this means:**
        - A 10×15×20 cube has 3,000 total cells
        - Each cell contains a value (e.g., sales amount)
        - Dimensions can represent: regions, time, products, customers, etc.
        
        **Real-world example:**
        - Dimension 1: 10 sales regions
        - Dimension 2: 365 days in a year
        - Dimension 3: 100 product categories
        - Result: 365,000 cells storing daily sales by region and product
        """)
    
    with tab3:
        st.markdown("""
        ### 🔧 1D Techniques
        
        **Prefix Sum (PS):**
        - **Query Cost**: 2 (very fast)
        - **Update Cost**: n (slow for large dimensions)
        - **Best for**: Read-heavy workloads, infrequent updates
        - **How it works**: Pre-computes cumulative sums
        
        **Space-Efficient Relative Prefix Sum (SRPS):**
        - **Query Cost**: 4 (balanced)
        - **Update Cost**: √n (moderate)
        - **Best for**: Balanced workloads
        - **How it works**: Uses block-based approach with anchors
        
        **Space-Efficient Dynamic Data Cube (SDDC):**
        - **Query Cost**: log(n) (good)
        - **Update Cost**: log(n) (good)
        - **Best for**: Balanced workloads, hierarchical data
        - **How it works**: Uses binary tree structure
        
        **Local Prefix Sum (LPS):**
        - **Query Cost**: variable (customizable)
        - **Update Cost**: variable (customizable)
        - **Best for**: Custom workloads, specific patterns
        - **How it works**: Custom block partitioning
        """)
    
    with tab4:
        st.markdown("""
        ### 📈 Performance Analysis
        
        **Cost Trade-offs:**
        - **Query Cost**: How many operations to answer a range query
        - **Update Cost**: How many operations to update a cell
        - **Trade-off**: Faster queries usually mean slower updates
        
        **Performance Benchmarks:**
        - **Construction Time**: Time to build the preprocessed cube
        - **Query Time**: Time to answer a range query
        - **Memory Usage**: Additional memory required
        
        **Scaling Behavior:**
        - Small cubes (10×10×10): < 1 second construction
        - Medium cubes (50×50×50): 1-5 seconds construction
        - Large cubes (100×100×100): 10-30 seconds construction
        
        **Technique Selection Guide:**
        - **High query frequency**: Use PS or SDDC
        - **High update frequency**: Use SRPS or LPS
        - **Balanced workload**: Use SRPS or SDDC
        - **Custom patterns**: Use LPS with custom configuration
        """)
    
    with tab5:
        st.markdown("""
        ### 🎮 Interactive Features
        
        **Live Simulation:**
        - **Range Queries**: Test different rectangular regions
          - Dim 1 Start/End: Select range in first dimension
          - Dim 2 Start/End: Select range in second dimension
          - Dim 3 Start/End: Select range in third dimension
        - **Execute Query**: See the sum of all cells in the selected range
        - **Brute Force Comparison**: Verify IDC results are correct
        
        **Update Simulation:**
        - **Update i/j/k**: Select which cell to modify
        - **Delta**: How much to add/subtract from the cell
        - **Apply Update**: See how the change affects query results
        
        **Performance Analysis:**
        - **Cost Trade-offs**: Compare different techniques
        - **Benchmarks**: Measure actual performance
        - **Scaling**: See how performance changes with cube size
        """)

def create_simple_3d_section():
    """Create a simple 3D visualization section"""
    st.subheader("3D Visualization")
    
    # Create sample cube
    cube_size = st.slider("Cube Size for 3D Visualization", 5, 15, 8)
    cube = np.random.rand(cube_size, cube_size, cube_size)
    
    # Show cube statistics
    st.write("**Cube Statistics:**")
    st.write(f"- Shape: {cube.shape}")
    st.write(f"- Total cells: {cube.size}")
    st.write(f"- Sum of all values: {np.sum(cube):.4f}")
    st.write(f"- Average value: {np.mean(cube):.4f}")
    st.write(f"- Min value: {np.min(cube):.4f}")
    st.write(f"- Max value: {np.max(cube):.4f}")
    
    # Show 2D slices
    st.write("**2D Slices (for visualization):**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        slice_idx = st.slider("Slice Index (Dim 1)", 0, cube_size-1, cube_size//2)
        slice_data = cube[slice_idx, :, :]
        fig = px.imshow(slice_data, title=f"Slice at Dim1={slice_idx}")
        st.plotly_chart(fig)
    
    with col2:
        slice_idx = st.slider("Slice Index (Dim 2)", 0, cube_size-1, cube_size//2)
        slice_data = cube[:, slice_idx, :]
        fig = px.imshow(slice_data, title=f"Slice at Dim2={slice_idx}")
        st.plotly_chart(fig)
    
    with col3:
        slice_idx = st.slider("Slice Index (Dim 3)", 0, cube_size-1, cube_size//2)
        slice_data = cube[:, :, slice_idx]
        fig = px.imshow(slice_data, title=f"Slice at Dim3={slice_idx}")
        st.plotly_chart(fig)

def create_interactive_dashboard():
    st.title("Iterative Data Cubes Simulation Dashboard")
    st.write("Interactive simulation and analysis of IDC techniques from the 2001 ICDT paper.")
    
    # Add documentation section
    create_documentation_section()
    
    # Sidebar configuration
    st.sidebar.header("Cube Configuration")
    
    # Dimension sizes
    st.sidebar.subheader("Dimension Sizes")
    dim1_size = st.sidebar.slider("Dimension 1 Size", 5, 50, 10)
    dim2_size = st.sidebar.slider("Dimension 2 Size", 5, 50, 15)
    dim3_size = st.sidebar.slider("Dimension 3 Size", 5, 50, 8)
    
    # Technique selection
    st.sidebar.subheader("Technique Selection")
    technique_options = ["Prefix Sum (PS)", "SRPS", "SDDC", "LPS"]
    
    technique1 = st.sidebar.selectbox("Technique for Dimension 1", technique_options, 0)
    technique2 = st.sidebar.selectbox("Technique for Dimension 2", technique_options, 1)
    technique3 = st.sidebar.selectbox("Technique for Dimension 3", technique_options, 2)
    
    # Create techniques based on selection
    def create_technique(technique_name: str):
        if technique_name == "Prefix Sum (PS)":
            return PrefixSumTechnique()
        elif technique_name == "SRPS":
            return SRPSTechnique(block_size=3)
        elif technique_name == "SDDC":
            return SDDCTechnique()
        elif technique_name == "LPS":
            return LPSTechnique([5, 5])
    
    techniques = [
        create_technique(technique1),
        create_technique(technique2),
        create_technique(technique3)
    ]
    
    # Main dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cost Trade-offs")
        if st.button("Generate Pareto Frontier"):
            with st.spinner("Generating cost analysis..."):
                # Generate cost data for different configurations
                configs = []
                technique_names = ["Prefix Sum", "SRPS", "SDDC", "LPS"]
                technique_instances = [
                    PrefixSumTechnique(),
                    SRPSTechnique(3),
                    SDDCTechnique(),
                    LPSTechnique([5, 5])
                ]
                
                for i, (name, tech) in enumerate(zip(technique_names, technique_instances)):
                    cube = np.random.rand(dim1_size, dim2_size, dim3_size)
                    idc = IterativeDataCube(cube, [tech] * 3)
                    query_cost, update_cost = idc.theoretical_costs()
                    
                    configs.append({
                        'technique': name,
                        'query_cost': query_cost,
                        'update_cost': update_cost
                    })
                
                # Create scatter plot
                df = pd.DataFrame(configs)
                fig = px.scatter(df, x='query_cost', y='update_cost', 
                               color='technique',
                               title="Query vs Update Cost Trade-offs")
                st.plotly_chart(fig)
    
    with col2:
        st.subheader("Performance Benchmarks")
        if st.button("Run Performance Tests"):
            with st.spinner("Running benchmarks..."):
                # Create test cube
                cube = np.random.rand(dim1_size, dim2_size, dim3_size)
                idc = IterativeDataCube(cube, techniques)
                
                # Measure construction time
                import time
                start_time = time.time()
                idc.construct()
                construction_time = time.time() - start_time
                
                # Measure query time
                query_ranges = [(0, dim1_size//2), (0, dim2_size//2), (0, dim3_size//2)]
                start_time = time.time()
                result = idc.range_query(query_ranges)
                query_time = time.time() - start_time
                
                # Display results
                st.metric("Construction Time", f"{construction_time:.4f}s")
                st.metric("Query Time", f"{query_time:.4f}s")
                st.metric("Query Result", f"{result:.4f}")
                
                # Theoretical costs
                query_cost, update_cost = idc.theoretical_costs()
                st.metric("Theoretical Query Cost", query_cost)
                st.metric("Theoretical Update Cost", update_cost)
    
    # Simple 3D Visualization section
    create_simple_3d_section()
    
    # Real-time simulation
    st.subheader("Live Simulation")
    
    # Create a simple cube for demonstration
    demo_cube = np.random.rand(5, 5, 5)
    demo_techniques = [PrefixSumTechnique(), SRPSTechnique(2), SDDCTechnique()]
    demo_idc = IterativeDataCube(demo_cube, demo_techniques)
    demo_idc.construct()
    
    # Interactive query interface
    st.write("Try different range queries:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start1 = st.slider("Dim 1 Start", 0, 4, 0)
        end1 = st.slider("Dim 1 End", 0, 4, 2)
    with col2:
        start2 = st.slider("Dim 2 Start", 0, 4, 0)
        end2 = st.slider("Dim 2 End", 0, 4, 2)
    with col3:
        start3 = st.slider("Dim 3 Start", 0, 4, 0)
        end3 = st.slider("Dim 3 End", 0, 4, 2)
    
    if st.button("Execute Query"):
        ranges = [(start1, end1), (start2, end2), (start3, end3)]
        result = demo_idc.range_query(ranges)
        st.success(f"Query Result: {result:.4f}")
        
        # Show brute force comparison
        brute_force = np.sum(demo_cube[start1:end1+1, start2:end2+1, start3:end3+1])
        st.info(f"Brute Force Result: {brute_force:.4f}")
        st.info(f"Difference: {abs(result - brute_force):.10f}")
    
    # Update simulation
    st.subheader("Update Simulation")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        update_i = st.slider("Update i", 0, 4, 0)
    with col2:
        update_j = st.slider("Update j", 0, 4, 0)
    with col3:
        update_k = st.slider("Update k", 0, 4, 0)
    with col4:
        update_delta = st.number_input("Delta", value=1.0, step=0.1)
    
    if st.button("Apply Update"):
        demo_idc.update_cell((update_i, update_j, update_k), update_delta)
        st.success(f"Updated cell ({update_i}, {update_j}, {update_k}) by {update_delta}")
        
        # Show updated query result
        ranges = [(0, 2), (0, 2), (0, 2)]
        updated_result = demo_idc.range_query(ranges)
        st.info(f"Updated Query Result: {updated_result:.4f}")

def main():
    create_interactive_dashboard()

if __name__ == "__main__":
    main() 