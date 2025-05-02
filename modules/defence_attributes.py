# defence_attributes.py

import pyautogui
from utils.ocr import perform_ocr
from utils.error_handling import handle_ocr_error
from config import DEFENCE_Y_START, DEFENCE_X_FIXED, DEFENCE_Y_OFFSET, DEFENCE_BOX

def extract_single_defence_attribute(region):
    screenshot = pyautogui.screenshot(region=region)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm='7')
    if all_text:
        return all_text.strip()
    else:
        return None

def defence_attributes_extraction():
    defence_attributes_data = {}
    expected_defence_attributes = [
        {"name": "piercing_defence", "type": int},
        {"name": "slashing_defence", "type": int},
        {"name": "blunt_defence", "type": int},
        {"name": "block", "type": int},
        {"name": "block_recovery", "type": int},
    ]

    extracted_values = []
    for i, attribute_config in enumerate(expected_defence_attributes):
        x = DEFENCE_X_FIXED
        y = DEFENCE_Y_START + i * DEFENCE_Y_OFFSET
        region = (x, y, DEFENCE_BOX[0], DEFENCE_BOX[1])
        value_str = extract_single_defence_attribute(region)
        extracted_values.append(value_str)

    if len(extracted_values) == len(expected_defence_attributes):
        for i, attribute_config in enumerate(expected_defence_attributes):
            value_str = extracted_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    screenshot_region = (
                        DEFENCE_X_FIXED,
                        DEFENCE_Y_START + i * DEFENCE_Y_OFFSET,
                        DEFENCE_BOX[0],
                        DEFENCE_BOX[1],
                    )
                    handle_ocr_error(
                        screenshot=pyautogui.screenshot(region=screenshot_region),
                        attribute_name=attribute_config["name"],
                        expected_type=attribute_config["type"],
                        ocr_text=value_str,
                        unit_name=None
                    )
                    value = None
            defence_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(
            screenshot=pyautogui.screenshot(region=(DEFENCE_X_FIXED, DEFENCE_Y_START, DEFENCE_Y_OFFSET * len(expected_defence_attributes), DEFENCE_BOX[1])),
            attribute_name="defence_attributes",
            ocr_text=f"Expected {len(expected_defence_attributes)} defence attributes, but could only extract {len(extracted_values)} values.",
            unit_name=None
        )
        return {}

    return defence_attributes_data