# unit_specific_attributes.py

import autoit, pyautogui, time
from utils.functions import is_button_present, capture_hover_popup
from utils.error_handling import handle_ocr_error
from utils.ocr import perform_ocr
from utils.navigation import move
from .trait_handler import capture_unit_traits
from .formation_handler import capture_unit_formations
from config import FORMATION_POTENTIAL_REGIONS, BOX_GREY_RGB, BOX_COLOR_TOLERANCE, ORDERS_POTENTIAL_REGIONS, TERRAIN_Y_LINE, TERRAIN_X_START, TERRAIN_X_OFFSET, TERRAIN_BOX

def unit_specific_attributes_extraction():
    terrain = terrain_extraction()
    traits_data = capture_unit_traits()
    formations = capture_unit_formations()
    orders = capture_unit_orders()

    unit_specific_data = {
        "terrain_resistances": terrain,
        "formations": formations,
        "orders": orders,
        "traits": traits_data
    }
    return unit_specific_data

# --- Formation Extraction ---

# --- Orders Extraction ---

def capture_unit_orders():
    captured_orders = []
    for i, region in enumerate(ORDERS_POTENTIAL_REGIONS):
        if is_button_present(region, BOX_GREY_RGB, BOX_COLOR_TOLERANCE):
            filename = f"order_{i+1}.png"
            pyautogui.screenshot(filename, region=region)
            captured_orders.append(filename)

            center_x = region[0] + region[2] // 2
            center_y = region[1] + region[3] // 2
            move((center_x, center_y))

            button_region = (region[0], region[1], region[2], region[3])
            popup_filename = capture_hover_popup(button_region, output_path=f"order_popup_{i+1}.png")
        else:
            break
    return captured_orders

# --- Terrain Extraction ---

def extract_terrain_attribute(attribute_name, x_offset_multiplier, expected_type=str):
    region = (
        TERRAIN_Y_LINE,
        TERRAIN_X_START + TERRAIN_X_OFFSET * x_offset_multiplier,
        TERRAIN_BOX[0],
        TERRAIN_BOX[1]
    )
    screenshot = pyautogui.screenshot(region=region)
    text = perform_ocr(screenshot, threshold=True, threshold_value=180)
    if text is not None:
        normalized_text = text.strip().lower()
        return handle_ocr_error(screenshot, attribute_name, expected_type=expected_type, ocr_text=normalized_text)
    else:
        return handle_ocr_error(screenshot, attribute_name)

def terrain_extraction():
    terrain_attributes_data = {}
    terrain_attributes_config = [
        {"name": "desert", "offset": 0, "type": str},
        {"name": "plain", "offset": 1, "type": str},
        {"name": "hills", "offset": 2, "type": str},
        {"name": "steppe", "offset": 3, "type": str},
        {"name": "urban", "offset": 4, "type": str},
    ]

    for attribute in terrain_attributes_config:
        value = extract_terrain_attribute(attribute["name"], attribute["offset"], attribute["type"])
        terrain_attributes_data[attribute["name"]] = value

    return terrain_attributes_data
