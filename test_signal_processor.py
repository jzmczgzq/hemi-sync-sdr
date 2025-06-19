import numpy as np
from signal_processor import SignalProcessor

def generate_test_signal(freq=440.0, duration=2.0, sample_rate=48000, noise_level=0.01):
    """
    Generate a synthetic sine wave signal with optional Gaussian noise.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = np.sin(2 * np.pi * freq * t)
    noise = np.random.normal(0, noise_level, signal.shape)
    return signal + noise

def main():
    processor = SignalProcessor(sample_rate=48000)
    
    # Simulate emotional frequency: "focus" at ~15 Hz
    test_signal = generate_test_signal(freq=15.0, duration=3.0)
    
    print("🚀 Running signal processor diagnostics on simulated 'focus' frequency.")
    processor.process_signal(test_signal, save_prefix="test_output/focus_test")

if __name__ == "__main__":
    main()

