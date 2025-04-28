# defence_attributes.py

import pyautogui
from utils.ocr_utils import perform_ocr
from utils.error_handling import handle_ocr_error
from config import DEFENCE_NUMBERS_REGION

def extract_all_defence_attributes():
    screenshot = pyautogui.screenshot(region=DEFENCE_NUMBERS_REGION)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm="5")
    if all_text:
        lines = all_text.strip().split('\n')
        return [line.strip() for line in lines]
    else:
        return []

def defence_attributes_extraction():
    defence_values = extract_all_defence_attributes()
    defence_attributes_data = {}
    expected_defence_attributes = [
        {"name": "piercing_defence", "type": int},
        {"name": "slashing_defence", "type": int},
        {"name": "blunt_defence", "type": int},
        {"name": "block", "type": int},
        {"name": "block_recovery", "type": int},
    ]

    if len(defence_values) == len(expected_defence_attributes):
        for i, attribute_config in enumerate(expected_defence_attributes):
            value_str = defence_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    handle_ocr_error(pyautogui.screenshot(
                        region=DEFENCE_NUMBERS_REGION), 
                        attribute_config["name"], 
                        expected_type=attribute_config["type"], 
                        ocr_text=value_str,
                        unit_name=None
                    )
            defence_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(screenshot=pyautogui.screenshot(region=DEFENCE_NUMBERS_REGION), attribute_name="defence_attributes", ocr_text=f"Expected {len(expected_defence_attributes)} defence attributes, but found {len(defence_values)}.")
        return {}

    return defence_attributes_data