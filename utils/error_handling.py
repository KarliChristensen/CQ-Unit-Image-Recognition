import os
import cv2
import numpy as np
from config import DEBUG_PARENT_FOLDER

CURRENT_UNIT_NAME = None

def set_unit_name(unit_name):
    global CURRENT_UNIT_NAME
    CURRENT_UNIT_NAME = unit_name

def handle_ocr_error(screenshot, attribute_name, unit_name=None, expected_type=None, ocr_text=None, cv2_image=None):
    if not os.path.exists(DEBUG_PARENT_FOLDER):
        os.makedirs(DEBUG_PARENT_FOLDER)

    debug_folder_name = DEBUG_PARENT_FOLDER  # Start with the main Debug folder
    if CURRENT_UNIT_NAME:
        safe_unit_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in CURRENT_UNIT_NAME)
        debug_folder_name = os.path.join(DEBUG_PARENT_FOLDER, safe_unit_name) # Nest it

    if not os.path.exists(debug_folder_name):
        os.makedirs(debug_folder_name)

    filename = os.path.join(debug_folder_name, f"{attribute_name} - DEBUG.png")
    warning_prefix = f"Warning: Unit '{unit_name}' - {attribute_name}" if unit_name else f"Warning: {attribute_name}"

    if attribute_name == "unit_tier":
        print(f"{warning_prefix} - Invalid tier value: '{ocr_text}'. Thresholded image saved to {filename}.")
        if cv2_image is not None and isinstance(cv2_image, np.ndarray):
            cv2.imwrite(filename, cv2_image)
        else:
            print("Warning: Thresholded image (cv2_image) is None, saving original screenshot.")
            screenshot.save(filename)
        return None

    elif ocr_text is None and cv2_image is None:
        print(f"{warning_prefix} extraction failed. Image saved to {filename}.")
        if cv2_image is not None and isinstance(cv2_image, np.ndarray):
            cv2.imwrite(filename, cv2_image)
        else:
            screenshot.save(filename)
        return None
    elif expected_type == int and ocr_text is not None:
        cleaned_text = ocr_text.strip()
        if cleaned_text in ('-', '.'):
            return None
        try:
            value = int(cleaned_text)
            if value <= 0:
                print(f"{warning_prefix} value is invalid: '{value}'. Image saved to {filename}.")
                if cv2_image is not None and isinstance(cv2_image, np.ndarray):
                    cv2.imwrite(filename, cv2_image)
                else:
                    screenshot.save(filename)
                return None
            return value
        except ValueError:
            print(f"{warning_prefix} OCR returned a non-integer string: '{ocr_text}'. Image saved to {filename}.")
            if cv2_image is not None and isinstance(cv2_image, np.ndarray):
                cv2.imwrite(filename, cv2_image)
            else:
                screenshot.save(filename)
            return None
        return value # Return the valid integer if no error
    elif ocr_text is not None and attribute_name in ["basic_attributes", "attack_attributes", "defence_attributes"]:
        print(f"Warning: {attribute_name} - {ocr_text} Image saved to {filename}.")
        if cv2_image is not None and isinstance(cv2_image, np.ndarray):
            cv2.imwrite(filename, cv2_image)
        else:
            screenshot.save(filename)
        return None
    elif ocr_text is not None:
        return ocr_text.strip()
    elif expected_type is None and cv2_image is not None:
        print(f"{warning_prefix} value is invalid. Image saved to {filename}.")
        cv2.imwrite(filename, cv2_image)
        return None
    elif ocr_text is not None:
        return ocr_text.strip()
    elif expected_type is None and cv2_image is not None:
        print(f"{warning_prefix} value is invalid. Image saved to {filename}.")
        cv2.imwrite(filename, cv2_image)
        return None
    else:
        return None