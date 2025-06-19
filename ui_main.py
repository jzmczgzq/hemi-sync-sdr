import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import time
from sdr_controller import SDRController
from signal_processor import SignalProcessor
from frequency_mapper import get_frequency

class SDRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jungian SDR Emotional Frequency Transmitter")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Load frequency data
        try:
            with open("frequencies.json", "r") as f:
                self.frequencies = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load frequencies.json:\n{e}")
            self.destroy()
            return

        # Load experiment data
        try:
            with open("experiment_data.json", "r") as f:
                self.experiment_data = json.load(f)
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to load experiment_data.json:\n{e}")
            self.experiment_data = {}

        self.sdr = SDRController()
        self.processor = SignalProcessor()
        self.transmit_thread = None
        self.transmitting = False

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for archetypes
        ttk.Label(self, text="Select Archetype:").pack(pady=(10,0))
        self.archetype_var = tk.StringVar()
        archetypes = list(self.frequencies.keys())
        self.archetype_menu = ttk.Combobox(self, textvariable=self.archetype_var, values=archetypes, state="readonly")
        self.archetype_menu.pack(pady=(0,10))
        if archetypes:
            self.archetype_var.set(archetypes[0])

        # Start / Stop buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Start Transmission", command=self.start_transmission)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="Stop Transmission", command=self.stop_transmission, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Status text box
        ttk.Label(self, text="Status:").pack()
        self.status_text = tk.Text(self, height=10, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Experiment results
        ttk.Label(self, text="Experiment Results:").pack()
        self.exp_results = tk.Text(self, height=6, state=tk.DISABLED)
        self.exp_results.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

        # Populate experiment results text
        self.update_experiment_results()

    def update_experiment_results(self):
        self.exp_results.config(state=tk.NORMAL)
        self.exp_results.delete(1.0, tk.END)
        for archetype, data in self.experiment_data.items():
            self.exp_results.insert(tk.END, f"{archetype}:\n")
            for key, val in data.items():
                self.exp_results.insert(tk.END, f"  {key}: {val}\n")
            self.exp_results.insert(tk.END, "\n")
        self.exp_results.config(state=tk.DISABLED)

    def start_transmission(self):
        archetype = self.archetype_var.get()
        frequency = get_frequency(archetype, self.frequencies)
        if frequency is None:
            messagebox.showerror("Error", "Selected archetype frequency not found.")
            return

        self.log(f"Starting transmission for {archetype} at {frequency} Hz")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.transmitting = True

        def transmit_loop():
            try:
                self.sdr.start_transmission(frequency)
                while self.transmitting:
                    signal = self.sdr.get_signal()
                    self.processor.process_signal(signal)
                    time.sleep(1)
            except Exception as e:
                self.log(f"Error during transmission: {e}")
            finally:
                self.sdr.stop_transmission()
                self.log("Transmission stopped.")

        self.transmit_thread = threading.Thread(target=transmit_loop, daemon=True)
        self.transmit_thread.start()

    def stop_transmission(self):
        self.log("Stopping transmission...")
        self.transmitting = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def log(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def on_close(self):
        if self.transmitting:
            self.transmitting = False
            self.sdr.stop_transmission()
        self.destroy()

if __name__ == "__main__":
    app = SDRApp()
    app.mainloop()
