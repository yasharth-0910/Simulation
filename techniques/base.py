from abc import ABC, abstractmethod
from typing import Dict, Tuple
import numpy as np

class OneDimensionalTechnique(ABC):
    @abstractmethod
    def preprocess(self, array: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def get_alpha_coefficients(self, cell_index: int) -> Dict[int, float]:
        pass

    @abstractmethod
    def get_beta_coefficients(self, range_start: int, range_end: int) -> Dict[int, float]:
        pass

    @abstractmethod
    def theoretical_costs(self, array_size: int) -> Tuple[int, int]:
        pass 