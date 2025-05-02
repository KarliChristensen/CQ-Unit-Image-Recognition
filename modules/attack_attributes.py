# attack_attributes.py

import pyautogui
from utils.ocr import perform_ocr
from utils.error_handling import handle_ocr_error
from config import ATTACK_Y_START, ATTACK_X_FIXED, ATTACK_Y_OFFSET, ATTACK_BOX

def extract_single_attack_attribute(region):
    screenshot = pyautogui.screenshot(region=region)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm='7')
    if all_text:
        return all_text.strip()
    else:
        return None

def attack_attributes_extraction():
    attack_attributes_data = {}
    expected_attack_attributes = [
        {"name": "piercing_armour_penetration", "type": int},
        {"name": "slashing_armour_penetration", "type": int},
        {"name": "blunt_armour_penetration", "type": int},
        {"name": "piercing_damage", "type": int},
        {"name": "slashing_damage", "type": int},
        {"name": "blunt_damage", "type": int},
    ]

    extracted_values = []
    for i, attribute_config in enumerate(expected_attack_attributes):
        x = ATTACK_X_FIXED 
        y = ATTACK_Y_START + i * ATTACK_Y_OFFSET
        region = (x, y, ATTACK_BOX[0], ATTACK_BOX[1])
        value_str = extract_single_attack_attribute(region)
        extracted_values.append(value_str)

    if len(extracted_values) == len(expected_attack_attributes):
        for i, attribute_config in enumerate(expected_attack_attributes):
            value_str = extracted_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    screenshot_region = (
                        ATTACK_X_FIXED ,
                        ATTACK_Y_START + i * ATTACK_Y_OFFSET,
                        ATTACK_BOX[0],
                        ATTACK_BOX[1],
                    )
                    handle_ocr_error(
                        screenshot=pyautogui.screenshot(region=screenshot_region),
                        attribute_name=attribute_config["name"],
                        expected_type=attribute_config["type"],
                        ocr_text=value_str,
                        unit_name=None
                    )
                    value = None
            attack_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(
            screenshot=pyautogui.screenshot(region=(ATTACK_X_FIXED, ATTACK_Y_START, ATTACK_Y_OFFSET * len(expected_attack_attributes), ATTACK_BOX[1])),
            attribute_name="attack_attributes",
            ocr_text=f"Expected {len(expected_attack_attributes)} attack attributes, but could only extract {len(extracted_values)} values.",
            unit_name=None
        )
        return {}

    return attack_attributes_data