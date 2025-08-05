from .base import OneDimensionalTechnique
import numpy as np
from typing import Dict, Tuple

class SDDCTechnique(OneDimensionalTechnique):
    def __init__(self):
        self.tree = None
        self.array_size = None

    def preprocess(self, array: np.ndarray) -> np.ndarray:
        self.array_size = len(array)
        # Build binary tree structure
        self.tree = self._build_tree(array)
        return self._flatten_tree()

    def _build_tree(self, array: np.ndarray) -> Dict:
        """Build binary tree with prefix sums at anchors"""
        tree = {}
        n = len(array)
        
        # Base case
        if n == 1:
            tree['value'] = array[0]
            tree['prefix_sum'] = array[0]
            return tree
        
        # Split array in half
        mid = n // 2
        left = array[:mid]
        right = array[mid:]
        
        # Recursively build subtrees
        tree['left'] = self._build_tree(left)
        tree['right'] = self._build_tree(right)
        
        # Compute prefix sum at this node
        tree['prefix_sum'] = tree['left']['prefix_sum'] + tree['right']['prefix_sum']
        tree['value'] = tree['prefix_sum']
        
        return tree

    def _flatten_tree(self) -> np.ndarray:
        """Convert tree to flat array for storage"""
        result = np.zeros(self.array_size)
        self._extract_values(self.tree, result, 0)
        return result

    def _extract_values(self, node: Dict, result: np.ndarray, offset: int):
        """Extract values from tree into flat array"""
        if 'left' not in node:
            result[offset] = node['value']
            return 1
        
        left_size = self._extract_values(node['left'], result, offset)
        right_size = self._extract_values(node['right'], result, offset + left_size)
        
        return left_size + right_size

    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        """Return coefficients for update propagation"""
        coeffs = {}
        self._find_update_path(self.tree, cell_index, 0, self.array_size, coeffs)
        return coeffs

    def _find_update_path(self, node: Dict, target: int, start: int, end: int, coeffs: Dict):
        """Find path from root to target cell for updates"""
        if 'left' not in node:
            if start == target:
                coeffs[start] = 1.0
            return
        
        mid = start + (end - start) // 2
        
        # Add coefficient for current node
        coeffs[start] = 1.0
        
        # Recursively traverse to target
        if target < mid:
            self._find_update_path(node['left'], target, start, mid, coeffs)
        else:
            self._find_update_path(node['right'], target, mid, end, coeffs)

    def get_beta_coefficients(self, start: int, end: int) -> Dict[int, float]:
        """Return coefficients for range queries using tree traversal"""
        coeffs = {}
        self._find_range_coefficients(self.tree, start, end, 0, self.array_size, coeffs)
        return coeffs

    def _find_range_coefficients(self, node: Dict, start: int, end: int, 
                                node_start: int, node_end: int, coeffs: Dict):
        """Find coefficients for range [start, end] using tree traversal"""
        if 'left' not in node:
            if node_start >= start and node_start <= end:
                coeffs[node_start] = 1.0
            return
        
        mid = node_start + (node_end - node_start) // 2
        
        # Recursively traverse relevant subtrees
        if start < mid:
            self._find_range_coefficients(node['left'], start, end, node_start, mid, coeffs)
        if end >= mid:
            self._find_range_coefficients(node['right'], start, end, mid, node_end, coeffs)

    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        # Both query and update costs are logarithmic
        log_n = int(np.ceil(np.log2(array_size)))
        return (log_n, log_n) 