# basic_attributes.py

from utils.ocr import perform_ocr
from utils.error_handling import handle_ocr_error
import pyautogui
from config import BASIC_Y_START, BASIC_X_FIXED, BASIC_Y_OFFSET, BASIC_BOX

def extract_single_number(region):
    screenshot = pyautogui.screenshot(region=region)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm='7') # Changed PSM for single line/word
    if all_text:
        return all_text.strip()
    else:
        return None

def basic_attributes_extraction():
    basic_attributes_data = {}
    expected_basic_attributes = [
        {"name": "health", "type": int},
        {"name": "strength", "type": int},
        {"name": "leadership", "type": int},
        {"name": "speed", "type": float},
        {"name": "range", "type": int},
        {"name": "ammo", "type": int},
        {"name": "labour", "type": float},
    ]

    extracted_values = []
    for i, attribute_config in enumerate(expected_basic_attributes):
        x = BASIC_X_FIXED
        y = BASIC_Y_START + i * BASIC_Y_OFFSET
        region = (x, y, BASIC_BOX[0], BASIC_BOX[1])
        value_str = extract_single_number(region)
        extracted_values.append(value_str)

    if len(extracted_values) == len(expected_basic_attributes):
        for i, attribute_config in enumerate(expected_basic_attributes):
            value_str = extracted_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    screenshot_region = (
                        BASIC_X_FIXED,
                        BASIC_Y_START + i * BASIC_Y_OFFSET,
                        BASIC_BOX[0],
                        BASIC_BOX[1],
                    )
                    handle_ocr_error(
                        screenshot=pyautogui.screenshot(region=screenshot_region),
                        attribute_name=attribute_config["name"],
                        expected_type=attribute_config["type"],
                        ocr_text=value_str,
                        unit_name=None
                    )
                    value = None
            basic_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(
            screenshot=pyautogui.screenshot(region=(BASIC_X_FIXED, BASIC_Y_START, BASIC_Y_OFFSET * len(expected_basic_attributes), BASIC_BOX[1])),
            attribute_name="basic_attributes",
            ocr_text=f"Expected {len(expected_basic_attributes)} basic attributes, but could only extract {len(extracted_values)} values.",
            unit_name=None
        )
        return {}

    return basic_attributes_data