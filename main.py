import yaml
import sys
from sdr_controller import SDRController
from signal_processor import SignalProcessor

def load_emotional_states(file_path):
    """Load emotional state profiles from a YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Load YAML config
    config = load_emotional_states('frequency_mapper.yaml')
    states = config.get('states', {})

    print("Welcome to the DDS Emotional SDR Interface")
    print("Select an emotional state to transmit:")

    state_names = list(states.keys())

    for i, name in enumerate(state_names, start=1):
        print(f"{i}. {name} - {states[name].get('notes', 'No description')}")

    # User selection
    try:
        choice = int(input("Enter the number of your choice: ")) - 1
        state_key = state_names[choice]
        profile = states[state_key]
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    print(f"\n[✓] Selected: {state_key}")
    print(f"    ↳ Carrier: {profile['carrier_freq']} Hz")
    print(f"    ↳ Modulation: {profile['mod_freq']} Hz")
    print(f"    ↳ Waveform: {profile['waveform']}")
    print(f"    ↳ Harmonics: {'On' if profile['harmonic_bleed'] else 'Off'}")
    print(f"    ↳ Duration: {profile['duration_sec']}s")

    # Initialize SDR and processor
    sdr = SDRController()
    processor = SignalProcessor()

    try:
        # Start transmission with full profile
        sdr.start_transmission(profile)
        print("⚡ Transmission started. Press Ctrl+C to terminate.")

        # Optional: Simulate processing (or just run transmission if passive)
        duration = profile.get('duration_sec', 60)
        for _ in range(duration):
            processor.process_signal(sdr.get_signal())

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        sdr.stop_transmission()
        print("Transmission safely stopped.")

if __name__ == "__main__":
    main()
