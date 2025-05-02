# ocr_utils.py

import pytesseract
from PIL import Image
import cv2
import numpy as np
from .functions import save_element

def perform_ocr(image, threshold=False, threshold_value=150, psm=None, popup_width=None):
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        config = ''
        if psm:
            config += f'--psm {psm}'
        if popup_width:
            config += f' -c textblock_width={popup_width}'

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

def perform_ocr_type(image, threshold=False, debug=True, threshold_value=150, psm=None, popup_width=None):
    try:
        img = image.convert('L')

        if threshold:
            img_np = np.array(img)
            _, thresh_img_np = cv2.threshold(img_np, threshold_value, 255, cv2.THRESH_BINARY)
            img = Image.fromarray(thresh_img_np)

        config = ''
        if psm:
            config += f'--psm {psm}'
        if popup_width:
            config += f' -c textblock_width={popup_width}'
        if debug == True:
            save_element(img, "Threshed Image ")

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
            save_element(img, "Threshed Image ")

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