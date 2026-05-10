import numpy as np
import sys
import os

# Ensure imports work when running this script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qguard.core.tracker import NoiseTracker
from qguard.core.compensator import PulseCompensator
from qguard.visualize.plotter import NoiseVisualizer

def run_simulation():
    print("🚀 QuantumGuarder: Real-Time Noise Cancellation Demo")
    print("Simulating phase drift and active compensation...")

    # 1. Simulation Setup
    dt = 1.0           # Time step in ns
    total_time = 200.0 # Duration in ns
    steps = int(total_time / dt)

    # 2. Initialize Components
    tracker = NoiseTracker(process_noise=1e-3, measurement_noise=1e-2, dt=dt)
    compensator = PulseCompensator(amplitude_scale=1.0, max_amplitude=5.0)
    visualizer = NoiseVisualizer()

    # 3. Data Arrays
    time_axis = np.arange(steps) * dt
    raw_noise_data = np.zeros(steps)
    compensation_data = np.zeros(steps)
    residual_data = np.zeros(steps)

    # 4. Main Control Loop
    # This loop runs at the speed of the quantum controller clock
    for t in range(steps):
        # --- SIMULATION OF PHYSICAL NOISE ---
        # In a real chip, this data comes from the readout resonator
        drift = 0.5 * np.sin(2 * np.pi * t * 0.005)  # Low-frequency drift
        jitter = np.random.normal(0, 0.1)             # High-frequency thermal noise
        measured_noise = drift + jitter
        
        # --- STEP 1: TRACK (Estimate) ---
        tracker.update(measured_noise)
        estimated_noise = tracker.get_state()[0]

        # --- STEP 2: COMPENSATE (Act) ---
        pulse = compensator.generate_compensation_pulse(
            phase_error=estimated_noise,
            duration=dt
        )
        
        # --- STEP 3: APPLY ---
        # The corrected signal is Original + Compensation
        # If compensation works, this should be close to zero
        corrected_signal = measured_noise + pulse['amplitude']

        # --- STORE RESULTS ---
        raw_noise_data[t] = measured_noise
        compensation_data[t] = pulse['amplitude']
        residual_data[t] = corrected_signal

    # 5. Visualization
    visualizer.plot_noise_cancellation(
        time_axis=time_axis,
        noise_signal=raw_noise_data,
        compensation_signal=compensation_data,
        corrected_signal=residual_data
    )
    
    print("✅ Simulation complete. Check 'noise_cancellation_demo.png'")

if __name__ == "__main__":
    run_simulation()
