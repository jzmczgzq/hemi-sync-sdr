import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

class SignalProcessor:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.previous_entropy = None

    def process_signal(self, signal, save_prefix=None):
        if signal is None or len(signal) == 0:
            print("[SignalProcessor] Warning: Received empty signal.")
            return

        print("📡 Processing signal...")

        # Basic stats
        rms = np.sqrt(np.mean(signal**2))
        peak = np.max(np.abs(signal))
        spectral_entropy = self.compute_spectral_entropy(signal)

        print(f"   ↳ RMS Amplitude: {rms:.4f}")
        print(f"   ↳ Peak Amplitude: {peak:.4f}")
        print(f"   ↳ Spectral Entropy: {spectral_entropy:.4f}")

        if self.previous_entropy is not None:
            delta = abs(self.previous_entropy - spectral_entropy)
            if delta > 0.3:
                print("⚠️  Entropy shift detected — possible modulation or distortion.")
        self.previous_entropy = spectral_entropy

        # Bandwidth estimate
        bw = self.estimate_bandwidth(signal)
        print(f"   ↳ Estimated Bandwidth: {bw:.2f} Hz")

        if save_prefix:
            self.export_wav(signal, f"{save_prefix}.wav")
            self.export_iq(signal, f"{save_prefix}.iq")
            self.plot_spectrogram(signal, f"{save_prefix}_spectrogram.png")

    def compute_spectral_entropy(self, signal, bins=100):
        spectrum = np.fft.fft(signal)
        psd = np.abs(spectrum[:len(spectrum)//2])**2
        psd /= np.sum(psd)  # normalize

        psd = psd[psd > 0]
        entropy = -np.sum(psd * np.log2(psd))
        entropy /= np.log2(len(psd))
        return entropy

    def estimate_bandwidth(self, signal):
        spectrum = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), d=1.0/self.sample_rate)
        power = np.abs(spectrum)**2
        threshold = 0.01 * np.max(power)
        significant = freqs[(power > threshold) & (freqs > 0)]
        if len(significant) == 0:
            return 0.0
        return significant[-1] - significant[0]

    def plot_spectrogram(self, signal, output_path):
        plt.figure(figsize=(10, 4))
        plt.specgram(signal, Fs=self.sample_rate, NFFT=1024, noverlap=512, cmap='inferno')
        plt.title("Spectrogram")
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.colorbar(label='dB')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"📊 Spectrogram saved to {output_path}")

    def export_wav(self, signal, output_path):
        norm_signal = np.int16(signal / np.max(np.abs(signal)) * 32767)
        wavfile.write(output_path, self.sample_rate, norm_signal)
        print(f"💾 WAV exported to {output_path}")

    def export_iq(self, signal, output_path):
        # Create dummy I/Q pair from signal: I = signal, Q = 0
        iq_data = np.empty(len(signal) * 2, dtype=np.float32)
        iq_data[0::2] = signal  # I
        iq_data[1::2] = 0.0     # Q
        iq_data.tofile(output_path)
        print(f"💾 IQ data exported to {output_path} (raw float32)")
