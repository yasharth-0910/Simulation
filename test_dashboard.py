#!/usr/bin/env python3
"""
Test script for IDC Dashboard components
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    try:
        from idc_framework import IterativeDataCube
        from techniques.prefix_sum import PrefixSumTechnique
        from techniques.srps import SRPSTechnique
        from techniques.sddc import SDDCTechnique
        from techniques.lps import LPSTechnique
        print("✅ All technique imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic IDC functionality"""
    try:
        import numpy as np
        from idc_framework import IterativeDataCube
        from techniques.prefix_sum import PrefixSumTechnique
        
        # Create a simple cube
        cube = np.random.rand(5, 5, 5)
        techniques = [PrefixSumTechnique(), PrefixSumTechnique(), PrefixSumTechnique()]
        idc = IterativeDataCube(cube, techniques)
        
        # Test construction
        idc.construct()
        
        # Test query
        result = idc.range_query([(0, 2), (0, 2), (0, 2)])
        
        # Test theoretical costs
        query_cost, update_cost = idc.theoretical_costs()
        
        print("✅ Basic IDC functionality works")
        print(f"   Query result: {result:.4f}")
        print(f"   Query cost: {query_cost}, Update cost: {update_cost}")
        return True
    except Exception as e:
        print(f"❌ Basic functionality error: {e}")
        return False

def test_dashboard_components():
    """Test dashboard components"""
    try:
        # Test 3D visualization import
        from dashboard.visualization_3d import create_3d_dashboard_section
        print("✅ 3D visualization import successful")
        
        # Test dashboard import
        from dashboard.dashboard import create_interactive_dashboard
        print("✅ Dashboard import successful")
        
        return True
    except Exception as e:
        print(f"❌ Dashboard component error: {e}")
        return False

def main():
    print("Testing IDC Dashboard Components")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    # Test dashboard components
    dashboard_ok = test_dashboard_components()
    
    print("\n" + "=" * 40)
    if imports_ok and basic_ok and dashboard_ok:
        print("✅ All tests passed! Dashboard should work correctly.")
        print("\nTo run the dashboard:")
        print("streamlit run dashboard/dashboard.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all files are in the correct locations")
        print("3. Restart the streamlit server if it's running")

if __name__ == "__main__":
    main() 