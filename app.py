import pyautogui
import modules.main_attributes as main_attributes
import modules.basic_attributes as basic_attributes
import keyboard, json, sys
from utils.navigation import move_and_click
from config import DETAILS_TAB_COORDINATES, VETERANCY_TAB_COORDINATES, HOTKEY_START, HOTKEY_INTERRUPT_RESET, HOTKEY_TERMINATE, OUTPUT_JSON_FILES

# --------------------------------------------- First Capture ---------------------------------------------

def capture_on_hotkey():
    print("Capturing unit data...")

    try:
        main_data = main_attributes.main_attributes_extraction()
        move_and_click(DETAILS_TAB_COORDINATES),
        basic_data = basic_attributes.basic_attributes_extraction()
        move_and_click(VETERANCY_TAB_COORDINATES),

        unit_data = {
            "main_values": {
                "unit_name": main_data.get("unit_name"),
                "unit_tier": main_data.get("tier"),
                "unit_max_level": main_data.get("max_level"),
                "unit_icon_path": main_data.get("icon_path"),
                "unit_type": main_data.get("unit_type"),
            },
            "attributes": {
                "basic_attributes": {
                    "health": basic_data.get("health"),
                    "strength": basic_data.get("strength"),
                    "leadership": basic_data.get("leadership"),
                    "speed": basic_data.get("speed"),
                    "range": basic_data.get("range"),
                    "ammo": basic_data.get("ammo"),
                    "labour": basic_data.get("labour")
                },
                "attack_attributes": {
                    "piercing_armour_penetration": basic_data.get("piercing_armour_penetration"),
                    "slashing_armour_penetration": basic_data.get("slashing_armour_penetration"),
                    "blunt_armour_penetration": basic_data.get("blunt_armour_penetration"),
                    "piercing_damage": basic_data.get("piercing_damage"),
                    "slashing_damage": basic_data.get("slashing_damage"),
                    "blunt_damage": basic_data.get("blunt_damage")
                },
                "defence_attributes": {
                    "piercing_defence": basic_data.get("piercing_defence"),
                    "slashing_defence": basic_data.get("slashing_defence"),
                    "blunt_defence": basic_data.get("blunt_defence"),
                    "block": basic_data.get("block"),
                    "block_recovery": basic_data.get("block_recovery")
                },
            },
            "unit_specific": {
                "terrain_resistances": {
                    "desert": basic_data.get("desert"),
                    "plain": basic_data.get("plain"),
                    "hills": basic_data.get("hills"),
                    "steppe": basic_data.get("steppe"),
                    "urban": basic_data.get("urban")
                },
                "formations": basic_data.get("formations"),
                "orders": basic_data.get("orders"),      
                "traits": basic_data.get("traits")
            },
        }

    except Exception as e:
        print(f"Error during unit data extraction: {e}")
        return

    primary_type = unit_data.get('unit_type', {}).get('primary')

    if primary_type and primary_type in OUTPUT_JSON_FILES:
        output_filename = OUTPUT_JSON_FILES[primary_type]
        try:
            with open(output_filename, 'r+') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        found = False
                        for i, entry in enumerate(data):
                            if entry.get('unit_name') == unit_data.get('unit_name'):
                                print(f"Match found: Overwriting ({entry.get('unit_name')}) using new data'")
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

# --- Navigate to the next tab ---

# --- Basic Attributes ---

    screenshot_unit_health = pyautogui.screenshot()
    screenshot_unit_health.save("back.png")

    unit_health_region = (1400, 450, 100, 30)
    screenshot_unit_health = pyautogui.screenshot(region=unit_health_region)
    screenshot_unit_health.save("unit_health.png")
 
    unit_speed_region = (1400, 543, 100, 30)
    screenshot_unit_speed = pyautogui.screenshot(region=unit_speed_region)
    screenshot_unit_speed.save("unit_speed.png") 
  
    unit_range_region = (1400, 574, 100, 30)
    screenshot_unit_range = pyautogui.screenshot(region=unit_range_region)
    screenshot_unit_range.save("unit_range.png")
 
    unit_ammo_region = (1400, 605, 100, 30)
    screenshot_unit_ammo = pyautogui.screenshot(region=unit_ammo_region)
    screenshot_unit_ammo.save("unit_ammo.png")

    unit_labour_region = (1400, 636, 100, 30)
    screenshot_unit_labour = pyautogui.screenshot(region=unit_labour_region)
    screenshot_unit_labour.save("unit_labour.png")    
    
# --- Attack Attributes ---

    unit_piercingArmourPen_region = (1400, 750, 100, 30)
    screenshot_unit_piercingArmourPen = pyautogui.screenshot(region=unit_piercingArmourPen_region)
    screenshot_unit_piercingArmourPen.save("piercingArmourPen.png")

    unit_slashingArmourPen_region = (1400, 782, 100, 30)
    screenshot_unit_slashingArmourPen = pyautogui.screenshot(region=unit_slashingArmourPen_region)
    screenshot_unit_slashingArmourPen.save("unit_slashingArmourPen.png")

    unit_bluntArmourPen_region = (1400, 814, 100, 30)
    screenshot_unit_bluntArmourPen = pyautogui.screenshot(region=unit_bluntArmourPen_region)
    screenshot_unit_bluntArmourPen.save("unit_bluntArmourPen.png")        

    unit_piercingDam_region = (1400, 846, 100, 30)
    screenshot_unit_piercingDam = pyautogui.screenshot(region=unit_piercingDam_region)
    screenshot_unit_piercingDam.save("unit_piercingDam.png")

    unit_slashingDam_region = (1400, 878, 100, 30)
    screenshot_unit_slashingDam = pyautogui.screenshot(region=unit_slashingDam_region)
    screenshot_unit_slashingDam.save("unit_slashingDam.png")

    unit_bluntDam_region = (1400, 910, 100, 30)
    screenshot_unit_bluntDam = pyautogui.screenshot(region=unit_bluntDam_region)
    screenshot_unit_bluntDam.save("unit_bluntDam.png")

# --- Defence Attributes ---

    unit_piercingDef_region = (1400, 1020, 100, 30)
    screenshot_unit_piercingDef = pyautogui.screenshot(region=unit_piercingDef_region)
    screenshot_unit_piercingDef.save("unit_piercingDef.png")

    unit_slashingDef_region = (1400, 1052, 100, 30)
    screenshot_unit_slashingDef = pyautogui.screenshot(region=unit_slashingDef_region)
    screenshot_unit_slashingDef.save("unit_slashingDef.png")

    unit_bluntDef_region = (1400, 1084, 100, 30)
    screenshot_unit_bluntDef = pyautogui.screenshot(region=unit_bluntDef_region)
    screenshot_unit_bluntDef.save("unit_bluntDef.png")

    unit_bluntDam_region = (1400, 1016, 100, 30)
    screenshot_unit_bluntDam = pyautogui.screenshot(region=unit_bluntDam_region)
    screenshot_unit_bluntDam.save("unit_bluntDam.png")

    unit_block_region = (1400, 1048, 100, 30)
    screenshot_unit_block = pyautogui.screenshot(region=unit_block_region)
    screenshot_unit_block.save("unit_block.png")

    unit_blockRecovery_region = (1400, 1080, 100, 30)
    screenshot_unit_blockRecovery = pyautogui.screenshot(region=unit_blockRecovery_region)
    screenshot_unit_blockRecovery.save("unit_blockRecovery.png")                    

# --- Terrain ---

    unit_desert_region = (1860, 495, 80, 30)
    screenshot_unit_desert = pyautogui.screenshot(region=unit_desert_region)
    screenshot_unit_desert.save("unit_desert.png")                    

    unit_plain_region = (1860, 544, 80, 30)
    screenshot_unit_plain = pyautogui.screenshot(region=unit_plain_region)
    screenshot_unit_plain.save("unit_plain.png")                    

    unit_hills_region = (1860, 583, 80, 30)
    screenshot_unit_hills = pyautogui.screenshot(region=unit_hills_region)
    screenshot_unit_hills.save("unit_hills.png")                    

    unit_steppe_region = (1860, 622, 80, 30)
    screenshot_unit_steppe = pyautogui.screenshot(region=unit_steppe_region)
    screenshot_unit_steppe.save("unit_steppe.png")                    

    unit_urban_region = (1860, 661, 80, 30)
    screenshot_unit_urban = pyautogui.screenshot(region=unit_urban_region)
    screenshot_unit_urban.save("unit_urban.png")                    

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