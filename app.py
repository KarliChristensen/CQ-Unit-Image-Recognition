import keyboard
import pyautogui
import time
import autoit

# --------------------------------------------- Configuration ---------------------------------------------

HOTKEY_START = 'ctrl+e'
HOTKEY_END = 'ctrl+s'
DETAILS_TAB_COORDINATES = (2582, 1353)
VETERANCY_TAB_COORDINATES = (2582, 1353)
MASTERY_TAB_COORDINATES = (2582, 1353)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def colors_are_similar(rgb1, rgb2, color_tolerance):
    return all(abs(c1 - c2) <= color_tolerance for c1, c2 in zip(rgb1, rgb2))

def capture_hover_popup(button_region, output_path="dynamic_popup.png", yellow_colors=None, title_color_hex="#9D9D9D", yellow_text_offset_up=25, yellow_text_offset_left=411):
    try:
        button_left, button_top, button_width, button_height = button_region
        title_color_rgb = hex_to_rgb(title_color_hex)

        if yellow_colors is None:
            yellow_colors_hex = ["#A69879", "#AA9B7C", "#95896D"]
            yellow_colors = [hex_to_rgb(hex_code) for hex_code in yellow_colors_hex]

        def is_yellow(rgb, yellow_colors_local):
            color_tolerance = 10
            for yellow in yellow_colors_local:
                if colors_are_similar(rgb, yellow, color_tolerance):
                    return True
            return False

        center_x = button_left + button_width // 2
        center_y = button_top + button_height // 2
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.05) # Give time for the pop-up to appear (adjust if needed)

        # Calculate potential start of the last yellow text line
        expected_yellow_text_x = button_left - yellow_text_offset_left
        expected_yellow_text_y_start = button_top - yellow_text_offset_up

        # Search for the yellow text in a small area
        found_yellow = False
        yellow_text_x = -1
        yellow_text_y_start = -1
        for x_offset in range(-5, 6):
            for y_offset in range(-5, 6):
                sample_x = expected_yellow_text_x + x_offset
                sample_y = expected_yellow_text_y_start + y_offset
                if 0 <= sample_x < pyautogui.size()[0] and 0 <= sample_y < pyautogui.size()[1]:
                    pixel_color = pyautogui.pixel(int(sample_x), int(sample_y))
                    if is_yellow(pixel_color, yellow_colors):
                        yellow_text_x = sample_x
                        yellow_text_y_start = sample_y
                        found_yellow = True
                        break
            if found_yellow:
                break

        if found_yellow:
            # Scan upwards for the title color from the found yellow text position
            title_top = -1
            for y in range(yellow_text_y_start - 5, max(0, yellow_text_y_start - 300), -1): # Scan upwards
                pixel_color = pyautogui.pixel(int(yellow_text_x), int(y))
                if colors_are_similar(pixel_color, title_color_rgb, color_tolerance=5): # Adjust tolerance as needed
                    title_top = y
                    break

            if title_top != -1:
                # Define the pop-up region with final adjustments
                popup_left = yellow_text_x - 5 - 10 # Add 10 pixels to the left
                popup_top = title_top - 5 - 10 # Add 10 pixels to the top
                popup_right = button_left # Use the left side of the hovered button as the right
                popup_bottom = button_top # Use the top of the hovered button as the bottom

                final_popup_left = max(0, int(popup_left))
                final_popup_top = max(0, int(popup_top))
                final_popup_right = min(pyautogui.size()[0], int(popup_right))
                final_popup_bottom = min(pyautogui.size()[1], int(popup_bottom))

                final_popup_width = final_popup_right - final_popup_left
                final_popup_height = final_popup_bottom - final_popup_top

                if final_popup_width > 0 and final_popup_height > 0:
                    screenshot = pyautogui.screenshot(region=(final_popup_left, final_popup_top, final_popup_width, final_popup_height))
                    screenshot.save(output_path)
                    print(f"Successfully captured dynamic hover pop-up to: {output_path} (text-based - final - area scan)")
                    return output_path
                else:
                    print("Could not determine the pop-up boundaries based on text (final - area scan).")
                    return None
            else:
                print("Could not find the title text to define pop-up boundaries (final - area scan).")
                return None
        else:
            print("Could not find the yellow text anchor.")
            return None

    except Exception as e:
        print(f"Error capturing dynamic hover pop-up (text-based - final - area scan): {e}")
        return None

def capture_trait_popup(button_region, output_path="trait_popup.png", title_color_hex="#CFCFCF", popup_offset_left=-356, popup_offset_up=-90, title_color_tolerance=15):
    try:
        button_left, button_top, button_width, button_height = button_region
        title_color_rgb = hex_to_rgb(title_color_hex)

        center_x = button_left + button_width // 2
        center_y = button_top + button_height // 2
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.05) # Give time for the pop-up to appear

        # Start title search from a position based on the button and offset
        search_x = button_left + popup_offset_left + 10 # Adjust starting X
        search_start_y = button_top + popup_offset_up + 10 # Adjust starting Y
        title_top = -1
        for y in range(search_start_y, max(0, search_start_y - 150), -1): # Scan upwards
            if 0 <= search_x < pyautogui.size()[0] and 0 <= y < pyautogui.size()[1]:
                pixel_color = pyautogui.pixel(int(search_x), int(y))
                if colors_are_similar(pixel_color, title_color_rgb, title_color_tolerance):
                    title_top = y
                    break

        if title_top != -1:
            # Define the pop-up region with adjustments for the offset
            popup_left = 1785
            popup_top = title_top + 10
            popup_right = 2143
            popup_bottom = button_top - 36 # Estimate height

            final_popup_left = max(0, int(popup_left))
            final_popup_top = max(0, int(popup_top))
            final_popup_right = min(pyautogui.size()[0], int(popup_right))
            final_popup_bottom = min(pyautogui.size()[1], int(popup_bottom))

            final_popup_width = final_popup_right - final_popup_left
            final_popup_height = final_popup_bottom - final_popup_top

            if final_popup_width > 0 and final_popup_height > 0:
                screenshot = pyautogui.screenshot(region=(final_popup_left, final_popup_top, final_popup_width, final_popup_height))
                screenshot.save(output_path)
                print(f"Successfully captured trait pop-up to: {output_path}")
                return output_path
            else:
                print("Could not determine the trait pop-up boundaries based on title.")
                return None
        else:
            print("Could not find the trait title text.")
            return None

    except Exception as e:
        print(f"Error capturing trait pop-up: {e}")
        return None


# --------------------------------------------- First Capture ---------------------------------------------

def capture_on_hotkey():
    print("Hotkey detected! Capturing multiple regions...")

    screenshot = pyautogui.screenshot()
    screenshot.save("full_screenshot.png")

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

    hold_duration = 0.05  

    autoit.mouse_move(DETAILS_TAB_COORDINATES[0], DETAILS_TAB_COORDINATES[1])
    autoit.mouse_down("left")
    time.sleep(hold_duration)
    autoit.mouse_up("left")
    time.sleep(0.2)  

# --------------------------------------------- Second Capture ---------------------------------------------

# --------------------------------------------- Configuration ---------------------------------------------

    BOX_GREY_HEX = "#8C8C8C"
    BOX_GREY_RGB = tuple(int(BOX_GREY_HEX[i:i+2], 16) for i in (1, 3, 5))
    BOX_COLOR_TOLERANCE = 10       
    
    FORMATION_POTENTIAL_REGIONS = [  
        (1730, 777, 63, 63),  
        (1815, 777, 63, 63),  
        (1901, 777, 63, 63),  
        (1987, 777, 63, 63),
    ]

    ORDERS_POTENTIAL_REGIONS = [  
        (2157, 775, 65, 65), 
        (2242, 775, 65, 65), 
        (2327, 775, 65, 65),
        (2412, 775, 65, 65),
    ]

    UNIT_TRAIT_POTENTIAL_REGIONS = [
        (2163, 501, 325, 25),  
        (2163, 534, 325, 25),
        (2163, 567, 325, 25),
        (2163, 600, 325, 25),
        (2163, 633, 325, 25),
    ]
    
    UNIT_TRAIT_TARGET_COLORS_RGB = [
        (133, 183, 85),  
        (159, 160, 160),
        (174, 53, 26), 
        (198, 57, 25),
    ]
    UNIT_TRAIT_COLOR_TOLERANCE = 20

    # --- !!!!Boxes are measured on the inside of the intended target ---

    captured_formations = []
    for i, region in enumerate(FORMATION_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"formation_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            print(f"Captured formation {i+1} at {region} to {filename}")
            captured_formations.append(filename)

            # --- Capture Hover Pop-up for Formation ---
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.2)

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"formations_popup_{i+1}.png")
            print(f"Captured formation pop-up: {popup_filename}")

        else:
            print(f"No more formations, moving on...")
            break
        
    print("Captured formations:", captured_formations)

    captured_orders = []
    for i, region in enumerate(ORDERS_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"order_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            print(f"Captured order {i+1} at {region} to {filename}")
            captured_orders.append(filename)

            # --- Capture Hover Pop-up for Order ---
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.2)

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"order_popup_{i+1}.png")
            print(f"Captured order pop-up: {popup_filename}")

        else:
            print(f"No more orders, moving on...")
            break

    print("Captured orders:", captured_orders)

    captured_traits = []
    first_trait_attempt = True  # Flag to handle the first trait differently
    for i, region in enumerate(UNIT_TRAIT_POTENTIAL_REGIONS):
        if first_trait_attempt:
            print("Circumventing color check for the first trait...")
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            autoit.mouse_click("left") # Click to dismiss blocking popup
            time.sleep(0.3)
            first_trait_attempt = False # Disable the flag for subsequent traits

            filename = f"trait_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            print(f"Captured trait {i+1} (circumvent) at {region} to {filename}")
            captured_traits.append(filename)

            # --- Capture Hover Pop-up for Trait ---
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.2)

            trait_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_trait_popup(trait_region, output_path=f"trait_popup_{i+1}.png")
            print(f"Captured trait pop-up: {popup_filename}")

        elif is_trait_present(region, UNIT_TRAIT_TARGET_COLORS_RGB, UNIT_TRAIT_COLOR_TOLERANCE):
            filename = f"trait_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            print(f"Captured trait {i+1} at {region} to {filename}")
            captured_traits.append(filename)

            # --- Capture Hover Pop-up for Trait ---
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.2)

            trait_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_trait_popup(trait_region, output_path=f"trait_popup_{i+1}.png")
            print(f"Captured trait pop-up: {popup_filename}")

        else:
            print(f"Unit trait {i+1} not present.")
            break
    print("Captured unit traits:", captured_traits)


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

# --- Formations ---



# --- Unit Traits ---



# --- Unit Orders ---+

def is_trait_present(region, target_colors_rgb, tolerance):
    x, y, w, h = region
    bracket_offset_x = 48
    bracket_offset_y = 14

    sample_x = x + bracket_offset_x
    sample_y = y + bracket_offset_y

    pixel_color = autoit.pixel_get_color(sample_x, sample_y)
    r = (pixel_color >> 16) & 0xFF
    g = (pixel_color >> 8) & 0xFF
    b = pixel_color & 0xFF
    current_rgb = (r, g, b)

    for target_color in target_colors_rgb:
        if all(abs(current - target) < tolerance for current, target in zip(current_rgb, target_color)):
            return True
    return False

def is_button_present(region, grey_rgb, tolerance):
    x, y, w, h = region
    for offset_y in range(h - 4, h):
        sample_points = [x + w // 4, x + w // 2, x + 3 * w // 4]
        for sample_x in sample_points:
            pixel_color = autoit.pixel_get_color(sample_x, y + offset_y)
            r = (pixel_color >> 16) & 0xFF
            g = (pixel_color >> 8) & 0xFF
            b = pixel_color & 0xFF
            if abs(r - grey_rgb[0]) < tolerance and \
               abs(g - grey_rgb[1]) < tolerance and \
               abs(b - grey_rgb[2]) < tolerance:
                return True
    return False

if __name__ == "__main__":
    keyboard.add_hotkey(HOTKEY_START, capture_on_hotkey)
    keyboard.wait('esc')
    print("\nHotkey listener stopped.")