from .base import OneDimensionalTechnique
import numpy as np
from typing import Dict, Tuple

class NoPreprocessingTechnique(OneDimensionalTechnique):
    def preprocess(self, array: np.ndarray) -> np.ndarray:
        return array.copy()

    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        # Only the cell itself is affected
        return {cell_index: 1.0}

    def get_beta_coefficients(self, start: int, end: int) -> Dict[int, float]:
        # Each cell in the range gets a coefficient of 1
        return {i: 1.0 for i in range(start, end + 1)}

    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        return (array_size, 1)
