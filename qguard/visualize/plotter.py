import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional

class NoiseVisualizer:
    def __init__(self):
        self.fig, self.axes = None, None

    def plot_noise_cancellation(self, time_axis: np.ndarray, 
                                 noise_signal: np.ndarray,
                                 compensation_signal: np.ndarray,
                                 corrected_signal: Optional[np.ndarray] = None) -> None:
        self.fig, self.axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
        
        self.axes[0].plot(time_axis, noise_signal, 'r-', linewidth=1.5, label='Noise')
        self.axes[0].set_ylabel('Amplitude')
        self.axes[0].set_title('Original Noise Signal')
        self.axes[0].grid(True, alpha=0.3)
        self.axes[0].legend()
        
        self.axes[1].plot(time_axis, compensation_signal, 'b-', linewidth=1.5, label='Compensation')
        self.axes[1].set_ylabel('Amplitude')
        self.axes[1].set_title('Compensation Signal (Anti-Noise)')
        self.axes[1].grid(True, alpha=0.3)
        self.axes[1].legend()
        
        if corrected_signal is None:
            corrected_signal = noise_signal + compensation_signal
        
        self.axes[2].plot(time_axis, corrected_signal, 'g-', linewidth=2, label='Corrected')
        self.axes[2].set_xlabel('Time (ns)')
        self.axes[2].set_ylabel('Amplitude')
        self.axes[2].set_title('Result After Cancellation')
        self.axes[2].grid(True, alpha=0.3)
        self.axes[2].legend()
        
        plt.tight_layout()
        plt.savefig('noise_cancellation_demo.png', dpi=150)
        print("✅ Plot saved: noise_cancellation_demo.png")

    def plot_phase_drift(self, time_axis: np.ndarray, 
                         phase_values: List[float]) -> None:
        plt.figure(figsize=(10, 4))
        plt.plot(time_axis, phase_values, 'm-', linewidth=1.5)
        plt.xlabel('Time (ns)')
        plt.ylabel('Phase (rad)')
        plt.title('Phase Drift Over Time')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('phase_drift.png', dpi=150)
        print("✅ Plot saved: phase_drift.png")
