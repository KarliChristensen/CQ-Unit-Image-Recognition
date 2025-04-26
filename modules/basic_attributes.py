# basic_attributes.py

import pyautogui
from utils.error_handling import handle_ocr_error
from utils.ocr_utils import perform_ocr
from utils.functions import is_button_present, capture_hover_popup, capture_trait_popup, is_trait_present
import autoit, time

from config import LEADERSHIP_REGION, STRENGTH_REGION, FORMATION_POTENTIAL_REGIONS, ORDERS_POTENTIAL_REGIONS, UNIT_TRAIT_POTENTIAL_REGIONS, UNIT_TRAIT_TARGET_COLORS_RGB, BOX_GREY_RGB, BOX_COLOR_TOLERANCE, UNIT_TRAIT_COLOR_TOLERANCE

# --------------------------------------------- Functions ---------------------------------------------

def basic_attributes_extraction():
    strength = extract_strength() 
    leadership = extract_leadership()
    formations = capture_formations()
    orders = capture_unit_orders()
    traits = capture_unit_traits()

    basic_data = {
        "strength": strength,
        "leadership": leadership,
        "formations": formations,
        "orders": orders,
        "traits": traits
    }
    return basic_data

# --- Unit Leadership Extraction ---   

def extract_leadership():
    leadership_region = LEADERSHIP_REGION
    screenshot_leadership = pyautogui.screenshot(region=leadership_region)
    leadership_text = perform_ocr(screenshot_leadership, threshold=True, threshold_value=180)
    if leadership_text is not None:
        return handle_ocr_error(screenshot_leadership, "leadership", expected_type=int, ocr_text=leadership_text)
    else:
        handle_ocr_error(screenshot_leadership, "leadership")
        return None

# --- Unit Strength Extraction ---   

def extract_strength():
    strength_region = STRENGTH_REGION
    screenshot_strength = pyautogui.screenshot(region=strength_region)
    strength_text = perform_ocr(screenshot_strength, threshold=True, threshold_value=180)
    if strength_text is not None:
        return handle_ocr_error(screenshot_strength, "strength", expected_type=int, ocr_text=strength_text)
    else:
        handle_ocr_error(screenshot_strength, "strength")
        return None

# --- Unit Formation Extraction ---   

def capture_formations():
    captured_formations = []
    for i, region in enumerate(FORMATION_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"formation_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_formations.append(filename)

            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.05)

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"formations_popup_{i+1}.png")
        else:
            break
    return captured_formations

# --- Unit Orders Extraction ---   

def capture_unit_orders():
    captured_orders = []
    for i, region in enumerate(ORDERS_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"order_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_orders.append(filename)

            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.05)

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"order_popup_{i+1}.png")
        else:
            break
    return captured_orders

# --- Unit Traits Extraction ---   

def capture_unit_traits():
    captured_traits = []
    first_trait_attempt = True
    for i, region in enumerate(UNIT_TRAIT_POTENTIAL_REGIONS):
        if first_trait_attempt:
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            first_trait_attempt = False

            filename = f"trait_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_traits.append(filename)

            autoit.mouse_move(center_x, center_y)
            time.sleep(0.05)

            trait_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_trait_popup(trait_region, output_path=f"trait_popup_{i+1}.png")

        elif is_trait_present(region, UNIT_TRAIT_TARGET_COLORS_RGB, UNIT_TRAIT_COLOR_TOLERANCE):
            filename = f"trait_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_traits.append(filename)

            # --- Capture Hover Pop-up for Trait ---
            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            autoit.mouse_move(center_x, center_y)
            time.sleep(0.05)

            trait_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_trait_popup(trait_region, output_path=f"trait_popup_{i+1}.png")

        else:
            break
    return captured_traits