import numpy as np
from typing import Tuple

class NoiseTracker:
    def __init__(self, process_noise: float = 1e-4, measurement_noise: float = 1e-2, dt: float = 1.0):
        self.x = np.array([0.0, 0.0])
        self.P = np.eye(2) * 0.1
        self.Q = np.eye(2) * process_noise
        self.R = measurement_noise
        self.dt = dt
        self.F = np.array([[1.0, self.dt], [0.0, 1.0]])
        self.H = np.array([1.0, 0.0])

    def update(self, measurement: float) -> None:
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

        innovation = measurement - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T / S

        self.x = self.x + K * innovation
        self.P = (np.eye(2) - np.outer(K, self.H)) @ self.P

    def get_compensation(self) -> float:
        return -self.x[0]

    def get_state(self) -> Tuple[float, float]:
        return self.x[0], self.x[1]
