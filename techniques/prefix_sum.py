import numpy as np
from typing import Dict, Tuple
from .base import OneDimensionalTechnique

class PrefixSumTechnique(OneDimensionalTechnique):
    def preprocess(self, array: np.ndarray) -> np.ndarray:
        return np.cumsum(array)

    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        # For PS, all later indices are affected
        return {i: 1.0 for i in range(cell_index, -1, -1)}

    def get_beta_coefficients(self, start: int, end: int) -> Dict[int, float]:
        # Range sum = PS[end] - PS[start-1] if start > 0 else PS[end]
        coeffs = {end: 1.0}
        if start > 0:
            coeffs[start - 1] = -1.0
        return coeffs

    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        return (2, array_size) 