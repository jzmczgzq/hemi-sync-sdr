import json
import sys
from sdr_controller import SDRController
from frequency_mapper import get_frequency
from signal_processor import SignalProcessor

def load_frequencies(file_path):
    """Load frequency mappings from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    # Load frequencies from JSON file
    frequencies = load_frequencies('frequencies.json')

    print("Welcome to the Jungian SDR!")
    print("Select a Jungian archetype to induce feelings:")
    
    # Display available archetypes
    for i, archetype in enumerate(frequencies.keys(), start=1):
        print(f"{i}. {archetype}")

    # Get user selection
    try:
        choice = int(input("Enter the number of your choice: ")) - 1
        archetype = list(frequencies.keys())[choice]
    except (ValueError, IndexError):
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Get the corresponding frequency
    frequency = get_frequency(archetype, frequencies)
    print(f"Selected Archetype: {archetype} | Frequency: {frequency} Hz")

    # Initialize SDR controller
    sdr = SDRController()
    
    # Initialize signal processor
    signal_processor = SignalProcessor()

    # Start transmission
    try:
        sdr.start_transmission(frequency)
        print("Transmission started. Press Ctrl+C to stop.")
        
        # Process signals (this could be a loop or a callback in a real application)
        while True:
            signal_processor.process_signal(sdr.get_signal())
    except KeyboardInterrupt:
        print("Stopping transmission...")
    finally:
        sdr.stop_transmission()
        print("Transmission stopped.")

if __name__ == "__main__":
    main()

