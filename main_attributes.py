import pyautogui
import ocr_utils
import cv2
from PIL import Image
import numpy as np

# --------------------------------------------- Configuration ---------------------------------------------

UNIT_NAME_REGION = (760, 140, 465, 60)
UNIT_TIER_REGION = (760, 190, 320, 40)
LEADERSHIP_REGION = (980, 405, 55, 25)
STRENGTH_REGION = (600, 405, 55, 25)
MAX_LEVEL_REGION = (790, 405, 55, 25)
ICON_REGION = (599, 140, 134, 134)
TYPE_REGION = (840, 240, 480, 40)

# --------------------------------------------- Functions ---------------------------------------------

def count_stars(pil_image):
    tier_value = None
    try:
        if pil_image is None:
            print("Warning: Received a None image for star counting.")
            return None

        img_np = np.array(pil_image.convert('L'))
        roi = img_np

        # --- Thresholding ---
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)


        # --- Full Star Detection ---
        params_full = cv2.SimpleBlobDetector_Params()
        params_full.filterByArea = True
        params_full.minArea = 50
        params_full.maxArea = 500
        params_full.filterByColor = True
        params_full.blobColor = 0 
        detector_full = cv2.SimpleBlobDetector_create(params_full)
        full_keypoints = detector_full.detect(thresh)
        num_full_stars = len(full_keypoints)
        print(f"Detected black full stars: {num_full_stars}")

        # --- Half Star Detection ---
        params_half = cv2.SimpleBlobDetector_Params()
        params_half.filterByArea = True
        params_half.minArea = 20
        params_half.maxArea = 49
        params_half.filterByColor = True
        params_half.blobColor = 0
        detector_half = cv2.SimpleBlobDetector_create(params_half)
        half_keypoints = detector_half.detect(thresh)
        num_half_stars = len(half_keypoints)
        print(f"Detected black potential half stars: {num_half_stars}")

        # --- Value Calculation ---
        tier_value = float(num_full_stars) + (0.5 * num_half_stars)
        if tier_value <= 0:
            print(f"Warning: Full Stars:{num_full_stars} Half Stars:{num_half_stars} - Setting value to None, image saved as thresh_DEBUG.")
            cv2.imwrite("thresh_DEBUG.png", thresh)
            tier_value = None
        return tier_value

    except Exception as e:
        print(f"Warning: Error occurred during star counting - image saved as thresh_DEBUG: {e}")
        cv2.imwrite("thresh_DEBUG.png", thresh)
        return None

def main_attributes_extraction():

    unit_data = {
        'unit_name': None,
        'basic_attributes': {
            'strength': None,
            'max_level': None,
            'leadership': None,
            "tier": None,
        },
        'unit_type': {
            'primary': None,
            'subtype': None
        },
    }

# --------------------------------------------- Extractions ---------------------------------------------

    # --- Unit Name Extraction ---

    unit_name_region = (UNIT_NAME_REGION[0], UNIT_NAME_REGION[1], UNIT_NAME_REGION[2], UNIT_NAME_REGION[3])
    screenshot_unit_name = pyautogui.screenshot(region=unit_name_region)
    name_text = ocr_utils.perform_ocr(screenshot_unit_name)
    if name_text:
        import re
        normalized_text = re.sub(r'\s+', ' ', name_text).strip().replace("_", " ")
        parts = normalized_text.split(" ")
        unit_data['unit_name'] = normalized_text.lower()
    else:
        print("Warning: Unit name OCR failed or returned an empty string.")
        unit_data['unit_name'] = None

    # --- Unit Tier Extraction ---   

    unit_tier_region = (UNIT_TIER_REGION[0], UNIT_TIER_REGION[1], UNIT_TIER_REGION[2], UNIT_TIER_REGION[3])
    screenshot_unit_tier = pyautogui.screenshot(region=unit_tier_region)
    tier_value = count_stars(screenshot_unit_tier)

    
    unit_data['basic_attributes']['tier'] = tier_value

    # --- Unit Leadership Extraction ---   

    leadership_region = (LEADERSHIP_REGION[0], LEADERSHIP_REGION[1], LEADERSHIP_REGION[2], LEADERSHIP_REGION[3])
    screenshot_leadership = pyautogui.screenshot(region=leadership_region)
    screenshot_leadership.save("leadership - ERROR CHECK.png") # Save the screenshot for debugging
    leadership_text = ocr_utils.perform_ocr(screenshot_leadership)

    leadership_value = None
    if leadership_text:
        try:
            leadership_value = int(leadership_text.strip())
        except ValueError:
            print("Warning: Unit leadership OCR failed or returned an empty string.")
            leadership_value = None

    unit_data['basic_attributes']['leadership'] = leadership_value

    # --- Unit Strength Extraction ---   

    strength_region = (STRENGTH_REGION[0], STRENGTH_REGION[1], STRENGTH_REGION[2], STRENGTH_REGION[3])
    screenshot_strength = pyautogui.screenshot(region=strength_region)
    screenshot_strength.save("strength - ERROR CHECK.png") # Save the screenshot for debugging
    strength_text = ocr_utils.perform_ocr(screenshot_leadership)

    strength_value = None
    if strength_text:
        try:
            strength_value = int(strength_text.strip())
        except ValueError:
            print("Warning: Unit strength OCR failed or returned an empty string.")
            strength_value = None

    unit_data['basic_attributes']['strength'] = strength_value

    # --- Unit Max Level Extraction ---   

    max_level_region = (MAX_LEVEL_REGION[0], MAX_LEVEL_REGION[1], MAX_LEVEL_REGION[2], MAX_LEVEL_REGION[3])
    screenshot_max_level = pyautogui.screenshot(region=max_level_region)
    unit_data['basic_attributes']['max_level'] = ocr_utils.perform_ocr(screenshot_max_level)
    max_level_text = ocr_utils.perform_ocr(screenshot_max_level)

    max_level_value = None
    if max_level_text:
        try:
            max_level_value = int(max_level_text.strip())
        except ValueError:
            print("Warning: Unit max level OCR failed or returned an empty string.")
            max_level_value = None

    unit_data['basic_attributes']['max_level'] = max_level_value        

    icon_region = (ICON_REGION[0], ICON_REGION[1], ICON_REGION[2], ICON_REGION[3])
    screenshot_icon = pyautogui.screenshot(region=icon_region)
    unit_data['icon_path'] = "icon.png"
    screenshot_icon.save("icon.png")

    # --- Unit Type & Subtype Extraction ---   
    
    type_region = (TYPE_REGION[0], TYPE_REGION[1], TYPE_REGION[2], TYPE_REGION[3])
    screenshot_type = pyautogui.screenshot(region=type_region)
    type_text = ocr_utils.perform_ocr(screenshot_type)
    if type_text:
        import re

        normalized_text = re.sub(r'\s+', ' ', type_text).strip().replace("_", " ")
        parts = normalized_text.split(" ") # Split by a single space
        primary_type_part = parts[0] + " " + parts[1] if len(parts) > 1 else None # Reconstruct primary type
        subtype_part = " ".join(parts[2:]) if len(parts) > 2 else None # Capture the rest as subtype

        unit_type = None
        unit_subtype = None

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

    unit_data['unit_type'] = {
        'primary': unit_type,
        'subtype': unit_subtype
    }

    return unit_data