from .base import OneDimensionalTechnique
import numpy as np
from typing import Dict, Tuple, List

class LPSTechnique(OneDimensionalTechnique):
    def __init__(self, block_sizes: List[int]):
        self.block_sizes = block_sizes
        self.block_boundaries = None
        self.local_prefixes = None
        self.array_size = None

    def preprocess(self, array: np.ndarray) -> np.ndarray:
        self.array_size = len(array)
        result = np.zeros(self.array_size)
        self.local_prefixes = np.zeros(self.array_size)
        
        # Calculate block boundaries
        self.block_boundaries = self._calculate_boundaries()
        
        # Compute local prefix sums within each block
        current_pos = 0
        for i, block_size in enumerate(self.block_sizes):
            if current_pos >= self.array_size:
                break
                
            end_pos = min(current_pos + block_size, self.array_size)
            block_sum = 0
            
            for j in range(current_pos, end_pos):
                block_sum += array[j]
                self.local_prefixes[j] = block_sum
                result[j] = self.local_prefixes[j]
            
            current_pos = end_pos
        
        return result

    def _calculate_boundaries(self) -> List[int]:
        """Calculate the boundaries of each block"""
        boundaries = [0]
        current_pos = 0
        
        for block_size in self.block_sizes:
            if current_pos >= self.array_size:
                break
            current_pos = min(current_pos + block_size, self.array_size)
            boundaries.append(current_pos)
        
        return boundaries

    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        """Return coefficients for update propagation"""
        coeffs = {}
        
        # Find which block contains the cell
        block_idx = self._find_block(cell_index)
        
        # Add coefficient for the cell itself
        coeffs[cell_index] = 1.0
        
        # Add coefficients for all cells in the same block and subsequent blocks
        for i in range(block_idx, len(self.block_boundaries) - 1):
            start = self.block_boundaries[i]
            end = self.block_boundaries[i + 1]
            for j in range(start, end):
                coeffs[j] = 1.0
        
        return coeffs

    def _find_block(self, cell_index: int) -> int:
        """Find which block contains the given cell index"""
        for i in range(len(self.block_boundaries) - 1):
            if (cell_index >= self.block_boundaries[i] and 
                cell_index < self.block_boundaries[i + 1]):
                return i
        return len(self.block_boundaries) - 2  # Default to last block

    def get_beta_coefficients(self, start: int, end: int) -> Dict[int, float]:
        """Return coefficients for range queries"""
        coeffs = {}
        
        start_block = self._find_block(start)
        end_block = self._find_block(end)
        
        if start_block == end_block:
            # Same block: use local prefixes
            if start > 0:
                coeffs[start - 1] = -1.0
            coeffs[end] = 1.0
        else:
            # Different blocks: need to handle block boundaries
            if start > 0:
                coeffs[start - 1] = -1.0
            coeffs[end] = 1.0
            
            # Add coefficients for intermediate blocks
            for i in range(start_block + 1, end_block):
                block_end = self.block_boundaries[i + 1] - 1
                if block_end >= 0:
                    coeffs[block_end] = 1.0
        
        return coeffs

    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        # Query cost: depends on number of blocks involved
        # Update cost: affects current block and all subsequent blocks
        n_blocks = len(self.block_sizes)
        return (n_blocks, n_blocks)

    @classmethod
    def optimize_for_dimension(cls, dim_size: int, query_patterns: Dict) -> 'LPSTechnique':
        """Create an optimized LPS configuration for a dimension"""
        # Simple heuristic: use sqrt of dimension size as block size
        optimal_block_size = int(np.sqrt(dim_size))
        return cls([optimal_block_size] * (dim_size // optimal_block_size + 1)) 