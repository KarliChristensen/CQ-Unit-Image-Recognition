import keyboard
import pyautogui
import time
import autoit

# --------------------------------------------- Configuration ------------------------------------------------

HOTKEY_CAPTURE = 'ctrl+e'
DETAILS_TAB_COORDINATES = (2582, 1353)
VETERANCY_TAB_COORDINATES = (2582, 1353)
MASTERY_TAB_COORDINATES = (2582, 1353)

# --------------------------------------------- First Capture ------------------------------------------------

def capture_on_hotkey():
    print("Hotkey detected! Capturing multiple regions...")

    screenshot = pyautogui.screenshot()
    screenshot.save("background_screenshot.png")

    unit_name_region = (760, 140, 465, 60)
    screenshot_unit_name = pyautogui.screenshot(region=unit_name_region)
    screenshot_unit_name.save("unit_name.png")

    unit_level_region = (760, 190, 320, 40)
    screenshot_unit_level = pyautogui.screenshot(region=unit_level_region)
    screenshot_unit_level.save("unit_level.png")

    type_region = (840, 240, 480, 40)
    screenshot_type = pyautogui.screenshot(region=type_region)
    screenshot_type.save("type_region.png")

    leadership_region = (980, 405, 55, 25)
    screenshot_leadership = pyautogui.screenshot(region=leadership_region)
    screenshot_leadership.save("leadership.png")

    strength_region = (600, 400, 55, 25)
    screenshot_strength = pyautogui.screenshot(region=strength_region)
    screenshot_strength.save("strength.png")

    maxLevel_region = (790, 400, 55, 25)
    screenshot_maxLevel = pyautogui.screenshot(region=maxLevel_region)
    screenshot_maxLevel.save("maxLevel.png")

    icon_region = (599, 140, 134, 134)
    screenshot_icon = pyautogui.screenshot(region=icon_region)
    screenshot_icon.save("icon.png")
    time.sleep(0.1)  

# --- Navigate to the next tab ---

    autoit.mouse_click("left", DETAILS_TAB_COORDINATES[0], DETAILS_TAB_COORDINATES[1])
    time.sleep(0.2)  

# --------------------------------------------- Second Capture ---------------------------------------------

    screenshot = pyautogui.screenshot()
    screenshot.save("attributes_background_screenshot.png")

# --------------------------------------------- Configuration ------------------------------------------------

    FORMATION_POTENTIAL_REGIONS = [  # Define the potential regions for up to 4 formations
        (1729, 776, 65, 65),  # Example: top-left x, y, width, height - ADJUST THESE!
        (1815, 776, 65, 65),  # Adjust for the position and size of the formation icons
        (1901, 776, 65, 65),  # Add more regions if needed for a max of 4
        (1987, 776, 65, 65),
    ]
    FORMATION_GREY_HEX = "#A3A3A3"
    FORMATION_GREY_RGB = tuple(int(FORMATION_GREY_HEX[i:i+2], 16) for i in (1, 3, 5))
    FORMATION_COLOR_TOLERANCE = 10       

    captured_formations = []
    for i, region in enumerate(FORMATION_POTENTIAL_REGIONS):
        if is_button_present(region, FORMATION_GREY_RGB, FORMATION_COLOR_TOLERANCE):
            filename = f"formation_{i+1}.png"
            autoit.screen_capture(filename, region[0], region[1], region[0] + region[2], region[1] + region[3])
            print(f"Captured formation {i+1} at {region} to {filename}")
            captured_formations.append(filename)
        else:
            print(f"Formation {i+1} not present.")
            break  # Stop if a formation is not found

    print("Captured formations:", captured_formations)

# --- Basic Attributes ---

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

# --- Formations ---


# --- Unit Traits ---
# --- Unit Orders ---+

def is_button_present(region, grey_rgb, tolerance):
    x, y, w, h = region
    # Sample pixels from the bottom 4 pixels of the region
    for offset_y in range(h - 4, h):
        # Sample a few points horizontally across the bottom bar
        sample_points = [x + w // 4, x + w // 2, x + 3 * w // 4]
        for sample_x in sample_points:
            pixel_color = autoit.pixel_get_color(sample_x, y + offset_y)
            r = (pixel_color >> 16) & 0xFF
            g = (pixel_color >> 8) & 0xFF
            b = pixel_color & 0xFF

            # Check if the pixel color is close to the target grey
            if abs(r - grey_rgb[0]) < tolerance and \
               abs(g - grey_rgb[1]) < tolerance and \
               abs(b - grey_rgb[2]) < tolerance:
                return True  # Grey bar found
    return False  # Grey bar not consistently found in the bottom 4 pixels

if __name__ == "__main__":
    keyboard.add_hotkey(HOTKEY_CAPTURE, capture_on_hotkey)
    keyboard.wait('esc')
    print("\nHotkey listener stopped.")