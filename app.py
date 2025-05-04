import modules.main_attributes as main_attributes
import modules.basic_attributes as basic_attributes
import modules.attack_attributes as attack_attributes
import modules.defence_attributes as defence_attributes
import modules.unit_specific_attributes as unit_specific_attributes
import keyboard, json, sys, pyautogui
from utils.navigation import move_and_click

from config import DETAILS_TAB_COORDINATES, ATTRIBUTES_TAB_COORDINATES, VETERANCY_TAB_COORDINATES, HOTKEY_START, HOTKEY_INTERRUPT_RESET, HOTKEY_TERMINATE, OUTPUT_JSON_FILES

# --------------------------------------------- First Capture ---------------------------------------------

def capture_on_hotkey():
    print("Capturing unit data...")

    try:
        screenshot()
        main_data = main_attributes.main_attributes_extraction()
        print("Main data extracted, moving on...")
        move_and_click(DETAILS_TAB_COORDINATES)
        move_and_click(ATTRIBUTES_TAB_COORDINATES)
        screenshot()
        basic_data = basic_attributes.basic_attributes_extraction()
        print("Basic data extracted, moving on...")
        attack_data = attack_attributes.attack_attributes_extraction()
        print("Attack data extracted, moving on...")
        defence_data = defence_attributes.defence_attributes_extraction()
        print("Defence data extracted, moving on...")
        unit_specific_data = unit_specific_attributes.unit_specific_attributes_extraction()
        move_and_click(VETERANCY_TAB_COORDINATES)
        screenshot()

        unit_data = {
            "main_values": {
                "unit_name": main_data.get("unit_name"),
                "unit_tier": main_data.get("unit_tier"),
                "unit_max_level": main_data.get("max_level"),
                "unit_icon_path": main_data.get("icon_path"),
                "unit_type": main_data.get("unit_type"),
            },
            "attributes": {
                "basic_attributes": basic_data,
                "attack_attributes": attack_data,
                "defence_attributes": defence_data,
            },
            "unit_specific": unit_specific_data,
        }

    except Exception as e:
        print(f"Error during unit data extraction: {e}")
        return

    primary_type_dict = unit_data.get('main_values', {}).get('unit_type')
    primary_type = primary_type_dict.get('primary') if isinstance(primary_type_dict, dict) else None

    if primary_type and primary_type in OUTPUT_JSON_FILES:
        output_filename = OUTPUT_JSON_FILES[primary_type]
        try:
            with open(output_filename, 'r+') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        found = False
                        for i, entry in enumerate(data):
                            if entry.get('main_values', {}).get('unit_name') == unit_data.get('main_values', {}).get('unit_name'):
                                print(f"Match found: Overwriting ({entry.get('main_values', {}).get('unit_name')}) using new data'")
                                data[i] = unit_data
                                found = True
                                break
                        if not found:
                            data.append(unit_data)
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                    else:
                        f.seek(0)
                        json.dump([unit_data], f, indent=4)
                        f.truncate()
                except json.JSONDecodeError:
                    f.seek(0)
                    json.dump([unit_data], f, indent=4)
                    f.truncate()
        except FileNotFoundError:
            with open(output_filename, 'w') as f:
                json.dump([unit_data], f, indent=4)

        print(f"Unit data saved to '{output_filename}' (overwrote if existing).")
    else:
        print(f"Warning: Unknown or missing primary type '{primary_type}'. Unit data not saved.")

# --- Helper Functions ---

screenshot_counter = 0

def screenshot():
    global screenshot_counter
    screenshot = pyautogui.screenshot()
    screenshot_counter += 1
    filename = f"screenshot_{screenshot_counter}.png"
    screenshot.save(filename)
    return filename

def interrupt_and_reset():
    global interrupt_capture
    print("Interrupted...")
    interrupt_capture = True

def terminate_script():
    print(f"Terminateed...")
    sys.exit()

def main():
    keyboard.add_hotkey(HOTKEY_START, capture_on_hotkey)
    keyboard.add_hotkey(HOTKEY_INTERRUPT_RESET, interrupt_and_reset)
    print(f"'Script running - {HOTKEY_START} to start', {HOTKEY_INTERRUPT_RESET} to interrupt while running and to {HOTKEY_TERMINATE} to end the script'.")
    keyboard.wait()

if __name__ == "__main__":
   main()