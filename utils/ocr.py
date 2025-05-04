# ocr_utils.py

import pytesseract, os, cv2
from PIL import Image
import numpy as np

DEBUG_PARENT_FOLDER = "Debug"
OCR_DEBUG_FOLDER = os.path.join(DEBUG_PARENT_FOLDER, "OCR")

debug_perform_ocr_count = 0
debug_perform_ocr_type_count = 0
debug_perform_ocr_single_line_count = 0

def ensure_debug_folders_exist():
    if not os.path.exists(OCR_DEBUG_FOLDER):
        os.makedirs(OCR_DEBUG_FOLDER)

def perform_ocr(image, threshold=False, debug=False, threshold_value=150, psm=None):
    ensure_debug_folders_exist()
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        config = ''
        if psm:
            config += f'--psm {psm}'
        if debug == True:
            global debug_perform_ocr_count
            img.save(os.path.join(OCR_DEBUG_FOLDER, f"perform_ocr_{debug_perform_ocr_count}.png"))
            debug_perform_ocr_count += 1

        text = pytesseract.image_to_string(img, config=config)
        cleaned_text = text.strip()
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char in ['.', '-', ' '])
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return None

def perform_ocr_type(image, threshold=False, debug=False, threshold_value=150, psm=None):
    ensure_debug_folders_exist()
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        config = ''
        if psm:
            config += f'--psm {psm}'
        if debug == True:
            global debug_perform_ocr_type_count
            img.save(os.path.join(OCR_DEBUG_FOLDER, f"perform_ocr_type_{debug_perform_ocr_type_count}.png"))
            debug_perform_ocr_type_count += 1

        text = pytesseract.image_to_string(img, config=config)
        cleaned_text = text.strip()
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char in ['.', '-'])
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during OCR (type): {e}")
        return None

def perform_ocr_single_line(image, debug=False, threshold=False, threshold_value=140):
    ensure_debug_folders_exist()
    try:
        if not isinstance(image, Image.Image):
            print(f"Error: Input 'image' is not a PIL.Image object. Type: {type(image)}")
            return ""  # Or handle this error more explicitly

        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        if debug == True:
            global debug_perform_ocr_single_line_count
            img.save(os.path.join(OCR_DEBUG_FOLDER, f"perform_ocr_single_line_{debug_perform_ocr_single_line_count}.png"))
            debug_perform_ocr_single_line_count += 1

        config = '--psm 7'
        text = pytesseract.image_to_string(img, config=config)
        cleaned_text = text.strip()
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char in ['.', '-', ' ', '%'])
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during single-line OCR: {e}")
        return None