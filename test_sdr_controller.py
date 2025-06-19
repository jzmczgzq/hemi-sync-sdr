import time
import numpy as np
import matplotlib.pyplot as plt
from sdr_controller import SDRController

def test_transmission():
    frequency = 432  # Hz — test tone
    duration = 3     # seconds
    sample_rate = 48000

    sdr = SDRController(sample_rate=sample_rate)
    sdr.start_transmission(frequency)

    print(f"Transmitting {frequency} Hz for {duration} seconds...")

    # Simulate signal processing loop
    samples = []
    start = time.time()
    while time.time() - start < duration:
        signal = sdr.get_signal()
        if signal is not None:
            samples.extend(signal)
        time.sleep(0.1)

    sdr.stop_transmission()
    print("Transmission complete.")

    # Plot waveform
    if samples:
        samples = np.array(samples)
        time_axis = np.linspace(0, len(samples)/sample_rate, num=len(samples))
        plt.figure(figsize=(10, 4))
        plt.plot(time_axis, samples)
        plt.title(f"Waveform: {frequency} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    test_transmission()
