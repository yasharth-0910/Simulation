#!/usr/bin/env python3
"""
Fix script for IDC Dashboard import issues
"""

import os
import sys
import importlib.util

def fix_imports():
    """Fix import issues by setting up proper paths"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add current directory to Python path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"✅ Added {current_dir} to Python path")
    
    # Check if all required files exist
    required_files = [
        'idc_framework.py',
        'techniques/base.py',
        'techniques/prefix_sum.py',
        'techniques/srps.py',
        'techniques/sddc.py',
        'techniques/lps.py',
        'dashboard/dashboard.py',
        'dashboard/visualization_3d.py',
        'dashboard/simple_dashboard.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
        else:
            print(f"✅ Found {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def test_imports():
    """Test that all imports work correctly"""
    try:
        # Test core imports
        from idc_framework import IterativeDataCube
        print("✅ idc_framework import successful")
        
        from techniques.prefix_sum import PrefixSumTechnique
        from techniques.srps import SRPSTechnique
        from techniques.sddc import SDDCTechnique
        from techniques.lps import LPSTechnique
        print("✅ All technique imports successful")
        
        # Test dashboard imports
        import importlib.util
        
        # Test visualization_3d import
        spec = importlib.util.spec_from_file_location(
            "visualization_3d", 
            os.path.join(os.path.dirname(__file__), "dashboard", "visualization_3d.py")
        )
        visualization_3d = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(visualization_3d)
        print("✅ 3D visualization import successful")
        
        # Test dashboard import
        spec = importlib.util.spec_from_file_location(
            "dashboard", 
            os.path.join(os.path.dirname(__file__), "dashboard", "dashboard.py")
        )
        dashboard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard)
        print("✅ Dashboard import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def create_working_dashboard():
    """Create a working dashboard that doesn't rely on complex imports"""
    dashboard_code = '''import streamlit as st
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
'''
    
    # Write the working dashboard
    with open('dashboard/working_dashboard.py', 'w') as f:
        f.write(dashboard_code)
    
    print("✅ Created working_dashboard.py")

def main():
    print("Fixing IDC Dashboard Import Issues")
    print("=" * 40)
    
    # Fix imports
    if not fix_imports():
        print("❌ Failed to fix imports")
        return
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        return
    
    # Create working dashboard
    create_working_dashboard()
    
    print("\n" + "=" * 40)
    print("✅ All fixes applied successfully!")
    print("\nTo run the dashboard, use one of these commands:")
    print("1. streamlit run dashboard/working_dashboard.py")
    print("2. streamlit run dashboard/simple_dashboard.py")
    print("3. streamlit run dashboard/dashboard.py")
    print("\nIf you encounter issues, try the working_dashboard.py first.")

if __name__ == "__main__":
    main() 