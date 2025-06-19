import numpy as np
import time

class SDRController:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.running = False
        self.signal = None

    def generate_waveform(self, profile):
        """Generate modulated waveform based on emotional profile."""
        duration = profile.get('duration_sec', 60)
        carrier_freq = profile['carrier_freq']
        mod_freq = profile['mod_freq']
        waveform = profile['waveform']
        pulse_rate = profile.get('pulse_rate', 1.0)
        harmonic_bleed = profile.get('harmonic_bleed', False)

        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)

        # Select base waveform
        if waveform == 'sine':
            base_wave = np.sin(2 * np.pi * mod_freq * t)
        elif waveform == 'triangle':
            base_wave = 2 * np.abs(2 * ((t * mod_freq) % 1) - 1) - 1
        elif waveform == 'square':
            base_wave = np.sign(np.sin(2 * np.pi * mod_freq * t))
        elif waveform == 'sawtooth':
            base_wave = 2 * (t * mod_freq - np.floor(t * mod_freq + 0.5))
        else:
            raise ValueError(f"Unsupported waveform: {waveform}")

        # Apply modulation to carrier
        carrier = np.sin(2 * np.pi * carrier_freq * t + pulse_rate * base_wave)

        # Optional: Add harmonic bleed
        if harmonic_bleed:
            carrier += 0.3 * np.sin(2 * np.pi * carrier_freq * 2 * t)  # 2nd harmonic
            carrier += 0.1 * np.sin(2 * np.pi * carrier_freq * 3 * t)  # 3rd harmonic

        # Normalize signal
        carrier = carrier / np.max(np.abs(carrier))
        return carrier

    def start_transmission(self, profile):
        """Start transmitting based on profile parameters."""
        print("[SDR] Generating signal...")
        self.signal = self.generate_waveform(profile)
        self.running = True
        print("[SDR] Signal ready for processing.")

    def get_signal(self):
        """Return current signal (for processing or output)."""
        if not self.running or self.signal is None:
            raise RuntimeError("Transmission not started or no signal generated.")
        return self.signal

    def stop_transmission(self):
        """Stop transmitting."""
        if self.running:
            self.running = False
            self.signal = None
            print("[SDR] Transmission halted.")

