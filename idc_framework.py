import numpy as np
from typing import List, Tuple, Dict
from techniques.base import OneDimensionalTechnique

class IterativeDataCube:
    def __init__(self, original_cube: np.ndarray, techniques: List[OneDimensionalTechnique]):
        self.original_cube = original_cube
        self.techniques = techniques
        self.preprocessed_cube = None
        self.construction_cost = 0

    def construct(self) -> np.ndarray:
        # Apply each technique along its dimension
        cube = self.original_cube.copy()
        for axis, technique in enumerate(self.techniques):
            # Move axis to front, apply preprocess, then move back
            cube = np.moveaxis(cube, axis, 0)
            shape = cube.shape
            cube = cube.reshape((shape[0], -1))
            for i in range(cube.shape[1]):
                cube[:, i] = technique.preprocess(cube[:, i])
            cube = cube.reshape(shape)
            cube = np.moveaxis(cube, 0, axis)
        self.preprocessed_cube = cube
        return cube

    def range_query(self, ranges: List[Tuple[int, int]]) -> float:
        """Process range query using Equation 12 from the paper"""
        if self.preprocessed_cube is None:
            self.construct()
        
        # Apply beta coefficients for each dimension
        result = 0.0
        cube_slice = self.preprocessed_cube
        
        for dim, (start, end) in enumerate(ranges):
            if start > end:
                return 0.0  # Invalid range
            
            # Get beta coefficients for this dimension
            beta_coeffs = self.techniques[dim].get_beta_coefficients(start, end)
            
            # Apply coefficients to the current slice
            temp_result = 0.0
            for idx, coeff in beta_coeffs.items():
                if 0 <= idx < cube_slice.shape[0]:
                    # Sum along all other dimensions
                    slice_sum = np.sum(cube_slice[idx])
                    temp_result += coeff * slice_sum
            
            # Update the slice for next dimension
            if dim < len(ranges) - 1:
                cube_slice = cube_slice[start:end+1]
        
        return temp_result

    def update_cell(self, indices: Tuple[int, ...], delta: float):
        """Update cell and propagate changes using alpha coefficients"""
        if self.preprocessed_cube is None:
            self.construct()
        
        # Update original cube
        self.original_cube[indices] += delta
        
        # Propagate changes using alpha coefficients for each dimension
        for dim, technique in enumerate(self.techniques):
            cell_idx = indices[dim]
            alpha_coeffs = technique.get_alpha_coefficients(cell_idx)
            
            # Apply alpha coefficients to update preprocessed cube
            for idx, coeff in alpha_coeffs.items():
                if 0 <= idx < self.preprocessed_cube.shape[dim]:
                    # Create slice indices for this dimension
                    slice_indices = [slice(None)] * len(self.preprocessed_cube.shape)
                    slice_indices[dim] = idx
                    
                    # Update the preprocessed cube
                    self.preprocessed_cube[tuple(slice_indices)] += coeff * delta

    def theoretical_costs(self) -> Tuple[int, int]:
        # Sum up costs from each technique
        query_cost = 0
        update_cost = 0
        for dim, technique in enumerate(self.techniques):
            n = self.original_cube.shape[dim]
            q, u = technique.theoretical_costs(n)
            query_cost += q
            update_cost += u
        return query_cost, update_cost

    def get_cube_info(self) -> Dict:
        """Get information about the cube and techniques"""
        return {
            'shape': self.original_cube.shape,
            'techniques': [type(tech).__name__ for tech in self.techniques],
            'theoretical_costs': self.theoretical_costs(),
            'construction_cost': self.construction_cost
        } 