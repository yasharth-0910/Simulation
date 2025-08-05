import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import streamlit as st
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

class IDC3DVisualizer:
    def __init__(self):
        self.cube = None
        self.idc = None
        self.techniques = None
        
    def create_3d_cube_visualization(self, cube: np.ndarray, title: str = "3D Data Cube") -> go.Figure:
        """Create a 3D scatter plot of the data cube"""
        # Create coordinate arrays
        x, y, z = np.meshgrid(
            np.arange(cube.shape[0]),
            np.arange(cube.shape[1]),
            np.arange(cube.shape[2]),
            indexing='ij'
        )
        
        # Flatten arrays for plotting
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()
        values_flat = cube.flatten()
        
        # Create color scale based on values
        colors = values_flat
        
        fig = go.Figure(data=[go.Scatter3d(
            x=x_flat,
            y=y_flat,
            z=z_flat,
            mode='markers',
            marker=dict(
                size=3,
                color=colors,
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(title="Value")
            ),
            text=[f'Value: {v:.3f}<br>Position: ({x}, {y}, {z})' 
                  for x, y, z, v in zip(x_flat, y_flat, z_flat, values_flat)],
            hovertemplate='<b>%{text}</b><extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Dimension 1',
                yaxis_title='Dimension 2',
                zaxis_title='Dimension 3',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=800,
            height=600
        )
        
        return fig
    
    def create_query_highlight_visualization(self, cube: np.ndarray, ranges: List[Tuple[int, int]], 
                                          title: str = "Query Range Highlight") -> go.Figure:
        """Create 3D visualization highlighting the query range"""
        # Create coordinate arrays
        x, y, z = np.meshgrid(
            np.arange(cube.shape[0]),
            np.arange(cube.shape[1]),
            np.arange(cube.shape[2]),
            indexing='ij'
        )
        
        # Create mask for query range
        mask = np.zeros_like(cube, dtype=bool)
        mask[ranges[0][0]:ranges[0][1]+1, 
             ranges[1][0]:ranges[1][1]+1, 
             ranges[2][0]:ranges[2][1]+1] = True
        
        # Separate points inside and outside query range
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()
        values_flat = cube.flatten()
        mask_flat = mask.flatten()
        
        # Points inside query range
        inside_x = x_flat[mask_flat]
        inside_y = y_flat[mask_flat]
        inside_z = z_flat[mask_flat]
        inside_values = values_flat[mask_flat]
        
        # Points outside query range
        outside_x = x_flat[~mask_flat]
        outside_y = y_flat[~mask_flat]
        outside_z = z_flat[~mask_flat]
        outside_values = values_flat[~mask_flat]
        
        fig = go.Figure()
        
        # Add points outside query range
        if len(outside_x) > 0:
            fig.add_trace(go.Scatter3d(
                x=outside_x,
                y=outside_y,
                z=outside_z,
                mode='markers',
                marker=dict(
                    size=2,
                    color='lightgray',
                    opacity=0.3
                ),
                name='Outside Query Range',
                showlegend=True
            ))
        
        # Add points inside query range
        if len(inside_x) > 0:
            fig.add_trace(go.Scatter3d(
                x=inside_x,
                y=inside_y,
                z=inside_z,
                mode='markers',
                marker=dict(
                    size=5,
                    color='red',
                    opacity=0.8
                ),
                name='Inside Query Range',
                showlegend=True
            ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Dimension 1',
                yaxis_title='Dimension 2',
                zaxis_title='Dimension 3',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=800,
            height=600
        )
        
        return fig
    
    def create_technique_comparison_visualization(self, cube: np.ndarray, 
                                                techniques: List, 
                                                query_ranges: List[Tuple[int, int]]) -> go.Figure:
        """Create visualization comparing different techniques"""
        fig = go.Figure()
        
        technique_names = ["Prefix Sum", "SRPS", "SDDC", "LPS"]
        colors = ['red', 'blue', 'green', 'orange']
        
        for i, technique in enumerate(techniques):
            if i < len(technique_names):
                # Create IDC with this technique
                idc = IterativeDataCube(cube, [technique] * len(cube.shape))
                idc.construct()
                
                # Get query result
                result = idc.range_query(query_ranges)
                
                # Add bar for this technique
                fig.add_trace(go.Bar(
                    x=[technique_names[i]],
                    y=[result],
                    name=technique_names[i],
                    marker_color=colors[i]
                ))
        
        fig.update_layout(
            title="Query Results by Technique",
            xaxis_title="Technique",
            yaxis_title="Query Result",
            width=600,
            height=400
        )
        
        return fig
    
    def create_cost_tradeoff_3d(self, cube_sizes: List[int], techniques: List) -> go.Figure:
        """Create 3D visualization of cost trade-offs"""
        x_data = []
        y_data = []
        z_data = []
        colors = []
        
        for size in cube_sizes:
            cube = np.random.rand(size, size, size)
            for i, technique in enumerate(techniques):
                idc = IterativeDataCube(cube, [technique] * 3)
                query_cost, update_cost = idc.theoretical_costs()
                
                x_data.append(query_cost)
                y_data.append(update_cost)
                z_data.append(size)
                colors.append(i)
        
        fig = go.Figure(data=[go.Scatter3d(
            x=x_data,
            y=y_data,
            z=z_data,
            mode='markers',
            marker=dict(
                size=8,
                color=colors,
                colorscale='Viridis',
                opacity=0.8
            ),
            text=[f'Size: {z}<br>Query Cost: {x}<br>Update Cost: {y}' 
                  for x, y, z in zip(x_data, y_data, z_data)]
        )])
        
        fig.update_layout(
            title="3D Cost Trade-off Analysis",
            scene=dict(
                xaxis_title='Query Cost',
                yaxis_title='Update Cost',
                zaxis_title='Cube Size',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=800,
            height=600
        )
        
        return fig

def create_3d_dashboard_section():
    """Create the 3D visualization section for the dashboard"""
    st.subheader("3D Visualization")
    
    # Initialize visualizer
    visualizer = IDC3DVisualizer()
    
    # Create sample cube
    cube_size = st.slider("Cube Size for 3D Visualization", 5, 15, 8)
    cube = np.random.rand(cube_size, cube_size, cube_size)
    
    # 3D cube visualization
    st.write("**3D Data Cube Visualization**")
    fig_3d = visualizer.create_3d_cube_visualization(cube, f"3D Data Cube ({cube_size}x{cube_size}x{cube_size})")
    st.plotly_chart(fig_3d)
    
    # Query range visualization
    st.write("**Query Range Highlight**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start1 = st.slider("Query Start Dim 1", 0, cube_size-1, 0)
        end1 = st.slider("Query End Dim 1", 0, cube_size-1, cube_size//2)
    with col2:
        start2 = st.slider("Query Start Dim 2", 0, cube_size-1, 0)
        end2 = st.slider("Query End Dim 2", 0, cube_size-1, cube_size//2)
    with col3:
        start3 = st.slider("Query Start Dim 3", 0, cube_size-1, 0)
        end3 = st.slider("Query End Dim 3", 0, cube_size-1, cube_size//2)
    
    ranges = [(start1, end1), (start2, end2), (start3, end3)]
    fig_query = visualizer.create_query_highlight_visualization(cube, ranges)
    st.plotly_chart(fig_query)
    
    # Technique comparison
    st.write("**Technique Comparison**")
    techniques = [PrefixSumTechnique(), SRPSTechnique(3), SDDCTechnique(), LPSTechnique([2, 2])]
    fig_comp = visualizer.create_technique_comparison_visualization(cube, techniques, ranges)
    st.plotly_chart(fig_comp)
    
    # 3D cost trade-off
    st.write("**3D Cost Trade-off Analysis**")
    cube_sizes = [5, 8, 10, 12]
    fig_cost = visualizer.create_cost_tradeoff_3d(cube_sizes, techniques)
    st.plotly_chart(fig_cost) 