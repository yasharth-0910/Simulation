import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from idc_framework import IterativeDataCube
from techniques.prefix_sum import PrefixSumTechnique
from techniques.srps import SRPSTechnique
from techniques.sddc import SDDCTechnique
from techniques.lps import LPSTechnique

def main():
    st.title("IDC Simulation Dashboard")
    st.write("Working dashboard with all features")
    
    # Sidebar configuration
    st.sidebar.header("Cube Configuration")
    dim1_size = st.sidebar.slider("Dimension 1 Size", 5, 20, 10)
    dim2_size = st.sidebar.slider("Dimension 2 Size", 5, 20, 10)
    dim3_size = st.sidebar.slider("Dimension 3 Size", 5, 20, 10)
    
    # Create cube and test
    cube = np.random.rand(dim1_size, dim2_size, dim3_size)
    techniques = [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique()]
    idc = IterativeDataCube(cube, techniques)
    
    # Test construction
    if st.button("Test IDC"):
        with st.spinner("Constructing IDC..."):
            idc.construct()
            st.success("IDC constructed successfully!")
            
            # Test query
            result = idc.range_query([(0, 2), (0, 2), (0, 2)])
            st.write(f"Query result: {result:.4f}")
            
            # Test costs
            query_cost, update_cost = idc.theoretical_costs()
            st.write(f"Query cost: {query_cost}, Update cost: {update_cost}")
    
    # Show cube info
    st.subheader("Cube Information")
    st.write(f"Shape: {cube.shape}")
    st.write(f"Total cells: {cube.size}")
    st.write(f"Sum of all values: {np.sum(cube):.4f}")

if __name__ == "__main__":
    main()
