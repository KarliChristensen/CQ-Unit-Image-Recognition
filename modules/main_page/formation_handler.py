# formation_handler.py

import pyautogui
from config import FORMATION_POTENTIAL_REGIONS, BOX_COLOR_TOLERANCE, BOX_GREY_RGB
from utils.functions import is_button_present, capture_hover_popup
from utils.navigation import move

def capture_unit_formations():
    captured_formations_data = []
    for i, region in enumerate(FORMATION_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            formation_data = process_formation(region, i)
            captured_formations_data.append(formation_data)
            move(region)           
        else:
            break
    return captured_formations_data

def process_formation(region, i):
    filename = f"formation_icon_{i+1}.png"
    pyautogui.screenshot(filename, region=region)
    result = capture_hover_popup(region)
    if result and result[0] is not None:
        title, text = result
        return {
            "formation title": title,
            "formation text": text,
            "modifiers": []
        }
    else:
        error_message = result[1] if result else "Unknown error during popup capture"
        print(f"Error capturing formation data for region {i+1}: {error_message}")
        return {
            "formation title": None,
            "formation text": None,
            "modifiers": [],
        }