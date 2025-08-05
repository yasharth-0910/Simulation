from .base import OneDimensionalTechnique
import numpy as np
from typing import Dict, Tuple

class SRPSTechnique(OneDimensionalTechnique):
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.global_prefixes = None
        self.local_prefixes = None
        self.array_size = None

    def preprocess(self, array: np.ndarray) -> np.ndarray:
        self.array_size = len(array)
        n_blocks = int(np.ceil(self.array_size / self.block_size))
        
        # Initialize storage arrays
        result = np.zeros(self.array_size)
        self.global_prefixes = np.zeros(n_blocks)
        self.local_prefixes = np.zeros(self.array_size)
        
        # Compute global prefixes at block anchors
        for i in range(n_blocks):
            start_idx = i * self.block_size
            end_idx = min((i + 1) * self.block_size, self.array_size)
            
            if i == 0:
                self.global_prefixes[i] = np.sum(array[start_idx:end_idx])
            else:
                self.global_prefixes[i] = self.global_prefixes[i-1] + np.sum(array[start_idx:end_idx])
        
        # Compute local prefixes within each block
        for i in range(n_blocks):
            start_idx = i * self.block_size
            end_idx = min((i + 1) * self.block_size, self.array_size)
            
            block_sum = 0
            for j in range(start_idx, end_idx):
                block_sum += array[j]
                self.local_prefixes[j] = block_sum
                result[j] = self.local_prefixes[j]
        
        return result

    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        # For SRPS, updates affect the current block and all subsequent blocks
        block_idx = cell_index // self.block_size
        coeffs = {}
        
        # Add coefficient for the cell itself
        coeffs[cell_index] = 1.0
        
        # Add coefficients for all subsequent blocks
        for i in range(block_idx + 1, len(self.global_prefixes)):
            start_idx = i * self.block_size
            end_idx = min((i + 1) * self.block_size, self.array_size)
            for j in range(start_idx, end_idx):
                coeffs[j] = 1.0
        
        return coeffs

    def get_beta_coefficients(self, start: int, end: int) -> Dict[int, float]:
        # SRPS requires at most 4 coefficients: 2 block anchors + 2 local positions
        coeffs = {}
        
        start_block = start // self.block_size
        end_block = end // self.block_size
        
        if start_block == end_block:
            # Same block: just use local prefixes
            if start > 0:
                coeffs[start - 1] = -1.0
            coeffs[end] = 1.0
        else:
            # Different blocks: use global prefixes for blocks, local for boundaries
            if start > 0:
                coeffs[start - 1] = -1.0
            coeffs[end] = 1.0
            
            # Add global block prefixes
            for i in range(start_block + 1, end_block):
                anchor_idx = i * self.block_size - 1
                if anchor_idx >= 0:
                    coeffs[anchor_idx] = 1.0
        
        return coeffs

    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        # Query cost: at most 4 coefficients
        # Update cost: affects current block and all subsequent blocks
        n_blocks = int(np.ceil(array_size / self.block_size))
        return (4, n_blocks) 