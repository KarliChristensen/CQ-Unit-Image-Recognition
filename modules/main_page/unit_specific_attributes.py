# unit_specific_attributes.py

import pyautogui
from utils.error_handling import handle_ocr_error
from utils.ocr import perform_ocr
from .trait_handler import capture_unit_traits
from .formation_handler import capture_unit_formations
from .orders_handler import capture_unit_orders
from config import TERRAIN_Y_LINE, TERRAIN_X_START, TERRAIN_X_OFFSET, TERRAIN_BOX

def unit_specific_attributes_extraction():
    terrain = terrain_extraction()
    print("Terrain data extracted, moving on...")
    traits_data = capture_unit_traits()
    print("Traits data extracted, moving on...")
    formations = capture_unit_formations()
    print("Formations data extracted, moving on...")
    orders = capture_unit_orders()
    print("Orders data extracted, moving on...")

    unit_specific_data = {
        "terrain_resistances": terrain,
        "formations": formations,
        "orders": orders,
        "traits": traits_data
    }
    return unit_specific_data

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
