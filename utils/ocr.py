# ocr_utils.py

import pytesseract
from PIL import Image
import cv2
import numpy as np
from .functions import save_element

debug_count = 0

def perform_ocr(image, threshold=False, debug=False, threshold_value=150, psm=None):
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
            save_element(img)


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
            save_element(img )

        text = pytesseract.image_to_string(img, config=config)
        cleaned_text = text.strip()
        cleaned_text = ''.join(char for char in cleaned_text if char.isalnum() or char in ['.', '-'])
        return cleaned_text
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
        return None

def perform_ocr_single_line(image, debug=False, threshold=False, threshold_value=140):
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)
        if debug == True:
            save_element(img)

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