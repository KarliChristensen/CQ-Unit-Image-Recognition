# attack_attributes.py

import pyautogui
from utils.ocr_utils import perform_ocr
from utils.error_handling import handle_ocr_error
from config import ATTACK_NUMBERS_REGION

def extract_all_attack_attributes():
    screenshot = pyautogui.screenshot(region=ATTACK_NUMBERS_REGION)
    all_text = perform_ocr(screenshot, threshold=True, threshold_value=180, psm="6")
    if all_text:
        lines = all_text.strip().split('\n')
        return [line.strip() for line in lines]
    else:
        return []

def attack_attributes_extraction():
    attack_values = extract_all_attack_attributes()
    attack_attributes_data = {}
    expected_attack_attributes = [
        {"name": "piercing_armour_penetration", "type": int},
        {"name": "slashing_armour_penetration", "type": int},
        {"name": "blunt_armour_penetration", "type": int},
        {"name": "piercing_damage", "type": int},
        {"name": "slashing_damage", "type": int},
        {"name": "blunt_damage", "type": int},
    ]

    if len(attack_values) == len(expected_attack_attributes):
        for i, attribute_config in enumerate(expected_attack_attributes):
            value_str = attack_values[i]
            value = None
            if value_str and value_str != '-':
                try:
                    value = attribute_config["type"](value_str)
                except ValueError:
                    handle_ocr_error(
                        screenshot=pyautogui.screenshot(region=ATTACK_NUMBERS_REGION),
                        attribute_name=attribute_config["name"],
                        expected_type=attribute_config["type"],
                        ocr_text=value_str,
                        unit_name=None  
                    )
                    value = None  
            attack_attributes_data[attribute_config["name"]] = value
    else:
        handle_ocr_error(screenshot=pyautogui.screenshot(region=ATTACK_NUMBERS_REGION), attribute_name="attack_attributes", ocr_text=f"Expected {len(expected_attack_attributes)} attack attributes, but found {len(expected_attack_attributes)}.")
        return {}
    
    return attack_attributes_data