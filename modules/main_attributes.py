# main_attributes.py

from utils.error_handling import handle_ocr_error
from utils.ocr_utils import perform_ocr
import pyautogui, re

from config import UNIT_NAME_REGION, UNIT_TIER_REGION, ICON_REGION, TYPE_REGION, STAR_COLOR, STAR_Y_COORDINATE, STAR_START_X_COORDINATE, STAR_X_OFFSETS, MAX_POSSIBLE_STARS, MAX_LEVEL_REGION

current_unit_name = None

# --------------------------------------------- Functions ---------------------------------------------

def main_attributes_extraction():
    current_unit_name = extract_unit_name()
    unit_tier = extract_unit_tier()
    max_level = extract_max_level()
    unit_type = extract_unit_type()
    icon_path = extract_icon()

    unit_data = {
        'unit_name': current_unit_name,
        'unit_tier': unit_tier,
        'max_level': max_level,
        'unit_type': unit_type,
        'icon_path': icon_path
    }
    return unit_data

# --------------------------------------------- Extractions ---------------------------------------------

# --- Unit Name Extraction ---

def extract_unit_name():
    unit_name_region = UNIT_NAME_REGION
    screenshot_unit_name = pyautogui.screenshot(region=unit_name_region)
    name_text = perform_ocr(screenshot_unit_name, threshold=True, threshold_value=180)
    if name_text is not None:
        normalized_text = re.sub(r'\s+', ' ', name_text).strip().replace("_", " ")
        return normalized_text.lower()
    else:
        handle_ocr_error(screenshot_unit_name, "unit_name")
        return None

# --- Unit Tier Extraction ---   
    
def extract_unit_tier():
    unit_tier_region = UNIT_TIER_REGION
    screenshot_unit_tier = pyautogui.screenshot(region=unit_tier_region)
    tier_value, _ = count_stars(screenshot_unit_tier)
    if tier_value is not None:
        if isinstance(tier_value, (int, float)) and tier_value >= 0:
            return tier_value
        else:
            handle_ocr_error(screenshot_unit_tier, "unit_tier", expected_type=float)
            return None
    else:
        handle_ocr_error(screenshot_unit_tier, "unit_tier")
        return None    
    
# --- Unit Max Level Extraction ---   

def extract_max_level():
    max_level_region = MAX_LEVEL_REGION
    screenshot_max_level = pyautogui.screenshot(region=max_level_region)
    max_level_text = perform_ocr(screenshot_max_level, threshold=True, threshold_value=180)
    if max_level_text is not None:
        return handle_ocr_error(screenshot_max_level, "max_level", expected_type=int, ocr_text=max_level_text)
    else:
        handle_ocr_error(screenshot_max_level, "max_level")
        return None
    
# --- Unit Type & Subtype Extraction ---   
    
def extract_unit_type():
    type_region = TYPE_REGION
    screenshot_type = pyautogui.screenshot(region=type_region)
    type_text = perform_ocr(screenshot_type, threshold=True, threshold_value=180)
    unit_type = None
    unit_subtype = None
    import re
    if type_text:
        normalized_text = re.sub(r'\s+', ' ', type_text).strip().replace("_", " ")
        parts = normalized_text.split(" ")
        primary_type_part = parts[0] + " " + parts[1] if len(parts) > 1 else None
        subtype_part = " ".join(parts[2:]) if len(parts) > 2 else None

        if primary_type_part:
            primary_type_lower = primary_type_part.lower().strip()
            if "melee infantry" in primary_type_lower:
                unit_type = "melee infantry"
                if subtype_part:
                    subtype_lower = subtype_part.lower().strip()
                    subtypes = ["polearm", "tower shield", "buckler shield", "special"]
                    for subtype in subtypes:
                        if subtype in subtype_lower:
                            unit_subtype = subtype
                            break
            elif "ranged infantry" in primary_type_lower:
                unit_type = "ranged infantry"
                if subtype_part:
                    subtype_lower = subtype_part.lower().strip()
                    subtypes = ["javelin", "archer", "crossbowman", "arquebusier", "special"]
                    for subtype in subtypes:
                        if subtype in subtype_lower:
                            unit_subtype = subtype
                            break
            elif "cavalry" in primary_type_lower:
                unit_type = "cavalry"
                if subtype_part:
                    subtype_lower = subtype_part.lower().strip()
                    subtypes = ["lancer", "melee", "special"]
                    for subtype in subtypes:
                        if subtype in subtype_lower:
                            unit_subtype = subtype
                            break

    else:
        handle_ocr_error(screenshot_type, "unit_type")
        print(f"Type of unit_type before return: {type(unit_type)}") 
        print(f"Returning: {{'primary': {unit_type}, 'subtype': {unit_subtype}}}")
    return {'primary': unit_type, 'subtype': unit_subtype}

# --- Icon Extraction ---

def extract_icon():
    icon_region = ICON_REGION
    screenshot_icon = pyautogui.screenshot(region=icon_region)
    screenshot_icon.save("icon.png")
    return "icon.png"

# --- Star Extraction ---

def count_stars(tier_image):
    tier_value = 0.0
    if tier_image is None:
        print("Warning: Received a None image for star counting.")
        return None, None

    pixels = tier_image.load()

    x_coordinate = STAR_START_X_COORDINATE
    offset_index = 0

    for _ in range(MAX_POSSIBLE_STARS * 2):
        try:
            pixel_color = pixels[x_coordinate, STAR_Y_COORDINATE]
            is_star_pixel = (isinstance(pixel_color, tuple) and pixel_color[:3] == STAR_COLOR) or \
                            (not isinstance(pixel_color, tuple) and pixel_color >= STAR_COLOR[0] - 5 and pixel_color <= STAR_COLOR[0] + 5)

            if is_star_pixel:
                tier_value += 0.5
            else:
                break

            x_coordinate += STAR_X_OFFSETS[offset_index % len(STAR_X_OFFSETS)]
            offset_index += 1

        except IndexError:
            print(f"Warning: Coordinates ({x_coordinate}, {STAR_Y_COORDINATE}) are outside the image bounds.")
            break

    if tier_value == 0.0:
        print("Warning: Unit tier returned as 0.0.")

    return tier_value, None