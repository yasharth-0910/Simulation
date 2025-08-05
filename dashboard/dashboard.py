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

def create_interactive_dashboard():
    st.title("Iterative Data Cubes Simulation Dashboard")
    st.write("Interactive simulation and analysis of IDC techniques from the 2001 ICDT paper.")
    
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
                for ps in [True, False]:
                    for srps in [True, False]:
                        for sddc in [True, False]:
                            for lps in [True, False]:
                                if sum([ps, srps, sddc, lps]) == 1:  # Only one technique per dimension
                                    config = []
                                    if ps:
                                        config.append(PrefixSumTechnique())
                                    elif srps:
                                        config.append(SRPSTechnique(3))
                                    elif sddc:
                                        config.append(SDDCTechnique())
                                    elif lps:
                                        config.append(LPSTechnique([5, 5]))
                                    
                                    # Repeat for all dimensions
                                    config = config * 3
                                    
                                    cube = np.random.rand(dim1_size, dim2_size, dim3_size)
                                    idc = IterativeDataCube(cube, config)
                                    query_cost, update_cost = idc.theoretical_costs()
                                    
                                    configs.append({
                                        'technique': technique_name,
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
