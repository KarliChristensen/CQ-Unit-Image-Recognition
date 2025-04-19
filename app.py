import keyboard
import pyautogui
import time

# --- Configuration ---
HOTKEY_CAPTURE = 'ctrl+e'
DETAILS_TAB_COORDINATES = (2582, 1353)

def capture_on_hotkey():
    print("Hotkey detected! Capturing multiple regions...")

    screenshot = pyautogui.screenshot()
    screenshot.save("background_screenshot.png")

    # Capture Unit Name
    unit_name_region = (760, 140, 465, 60)
    screenshot_unit_name = pyautogui.screenshot(region=unit_name_region)
    screenshot_unit_name.save("unit_name.png")

    # Capture Unit Stars
    unit_level_region = (760, 190, 320, 40)
    screenshot_unit_level = pyautogui.screenshot(region=unit_level_region)
    screenshot_unit_level.save("unit_level.png")

    # Capture Type
    type_region = (840, 240, 480, 40)
    screenshot_type = pyautogui.screenshot(region=type_region)
    screenshot_type.save("type_region.png")

    # Capture Leadership
    leadership_region = (980, 405, 55, 25)
    screenshot_leadership = pyautogui.screenshot(region=leadership_region)
    screenshot_leadership.save("leadership.png")

    # Capture Strength
    strength_region = (600, 400, 55, 25)
    screenshot_strength = pyautogui.screenshot(region=strength_region)
    screenshot_strength.save("strength.png")

    # Capture Maximum Level
    maxLevel_region = (790, 400, 55, 25)
    screenshot_maxLevel = pyautogui.screenshot(region=maxLevel_region)
    screenshot_maxLevel.save("maxLevel.png")

    # Capture Unit Icon
    icon_region = (599, 140, 134, 134)
    screenshot_icon = pyautogui.screenshot(region=icon_region)
    screenshot_icon.save("icon.png")
    time.sleep(0.1)

# --- Details Tab ---

def navigate_next_tab():
    print("Hotkey detected! Navigating to the details tab...")
    pyautogui.click(DETAILS_TAB_COORDINATES)

if __name__ == "__main__":
    print("Press Ctrl+E to capture multiple regions. Press ESC to stop.")
    keyboard.add_hotkey(HOTKEY_CAPTURE, capture_on_hotkey)
    keyboard.wait('esc')
    print("\nHotkey listener stopped.")