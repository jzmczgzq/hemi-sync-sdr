import json
import os

def load_json(file_path):
    """Load JSON data from file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """Save JSON data to file with pretty formatting."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def validate_choice(choice, options):
    """Check if choice is within valid options."""
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            return idx
    except ValueError:
        pass
    return None

def print_menu(title, options):
    """Print numbered menu with title."""
    print(f"\n=== {title} ===")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def confirm_prompt(message):
    """Prompt user for yes/no confirmation."""
    while True:
        choice = input(f"{message} (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'.")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
