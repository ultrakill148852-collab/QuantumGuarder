import numpy as np
from typing import Optional

class PulseCompensator:
    def __init__(self, amplitude_scale: float = 1.0, max_amplitude: float = 10.0):
        self.amplitude_scale = amplitude_scale
        self.max_amplitude = max_amplitude
        self.pulse_history = []

    def generate_compensation_pulse(self, phase_error: float, duration: float = 10.0) -> dict:
        amplitude = np.clip(
            self.amplitude_scale * phase_error,
            -self.max_amplitude,
            self.max_amplitude
        )
        
        t = np.linspace(0, duration, int(duration * 10))
        pulse_shape = amplitude * np.exp(-0.5 * (t / (duration / 4)) ** 2)
        
        pulse_data = {
            'amplitude': amplitude,
            'duration': duration,
            'shape': pulse_shape,
            'time_axis': t,
            'phase_correction': phase_error
        }
        
        self.pulse_history.append(pulse_data)
        return pulse_data

    def get_total_correction(self) -> float:
        return sum(p['phase_correction'] for p in self.pulse_history)

    def clear_history(self) -> None:
        self.pulse_history.clear()
