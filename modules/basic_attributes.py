# basic_attributes.py

from utils.ocr_utils import perform_ocr
from utils.error_handling import handle_ocr_error
import pyautogui
from config import BASIC_NUMBERS_REGION

def extract_all_numbers():
    screenshot = pyautogui.screenshot(region=BASIC_NUMBERS_REGION)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm='7')
    if all_text:
        lines = all_text.strip().split('\n')
        return [line.strip() for line in lines]
    else:
        return []

def basic_attributes_extraction():
    basic_values = extract_all_numbers()
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

    if len(basic_values) == len(expected_basic_attributes):
        for i, attribute_config in enumerate(expected_basic_attributes):
            value_str = basic_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    handle_ocr_error(
                        screenshot=pyautogui.screenshot(region=BASIC_NUMBERS_REGION),
                        attribute_name=attribute_config["name"],
                        expected_type=attribute_config["type"],
                        ocr_text=value_str,
                        unit_name=None 
                    )
                    value = None
            basic_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(screenshot=pyautogui.screenshot(region=BASIC_NUMBERS_REGION), attribute_name="basic_attributes", ocr_text=f"Expected {len(expected_basic_attributes)} basic attributes, but found {len(expected_basic_attributes)}.")
        return {}

    return basic_attributes_data